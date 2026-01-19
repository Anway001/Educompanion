import os
import re
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from transformers import pipeline
import torch
import pytesseract
from PIL import Image
import io
import pytube
import whisper

# =====================================================================
# CONFIGURATION
# =====================================================================
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INIT] Summarizer running on {DEVICE}")

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=0 if DEVICE == "cuda" else -1
)

whisper_model = whisper.load_model("base")

# Optional (Windows): specify path if Tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =====================================================================
# TEXT CLEANING
# =====================================================================
def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s.,;:!?()\-\n]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# =====================================================================
# TEXT EXTRACTION HELPERS
# =====================================================================
def extract_text_pypdf2(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    print(f"[PyPDF2] Extracted text from page {i+1}")
                text += page_text
    except Exception as e:
        print(f"[ERROR] PyPDF2 extraction failed: {e}")
    return clean_text(text)

def extract_text_tesseract(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for i, page in enumerate(doc):
            print(f"[OCR] Processing page {i+1}/{len(doc)}...")
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            page_text = pytesseract.image_to_string(img, lang="eng")
            text += page_text + "\n"
    except Exception as e:
        print(f"[ERROR] OCR extraction failed: {e}")
    return clean_text(text)

def extract_text_from_file(file_path):
    print(f"[LOG] Extracting text from: {file_path}")
    text = extract_text_pypdf2(file_path)
    if len(text.split()) < 50:
        print("[LOG] PyPDF2 extracted too little text. Switching to OCR...")
        text = extract_text_tesseract(file_path)
    if not text.strip():
        print("[ERROR] No readable text found after both methods.")
        return None
    print(f"[LOG] Extracted {len(text.split())} words of text.")
    return text

# =====================================================================
# YOUTUBE TRANSCRIPTION
# =====================================================================
def transcribe_youtube(youtube_url):
    """Download audio from YouTube and transcribe using Whisper"""
    try:
        yt = pytube.YouTube(youtube_url)
        print(f"[LOG] Downloading audio for: {yt.title}")

        # Get mp4 audio stream explicitly
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not audio_stream:
            raise ValueError("No mp4 audio stream found.")

        audio_path = os.path.join(UPLOAD_FOLDER, f"{yt.video_id}.mp4")
        audio_stream.download(filename=audio_path)
        print(f"[LOG] Audio downloaded to {audio_path}")

        print("[LOG] Transcribing audio with Whisper...")
        result = whisper_model.transcribe(audio_path)
        os.remove(audio_path)

        text = clean_text(result.get("text", ""))
        print(f"[LOG] Transcription complete, {len(text.split())} words extracted.")

        if not text.strip():
            raise ValueError("No speech detected in the video.")

        return text

    except Exception as e:
        print(f"[ERROR] YouTube transcription failed: {e}")
        return None

# =====================================================================
# SUMMARIZATION
# =====================================================================
def summarize_text(text):
    if not text or len(text.split()) < 60:
        print("[LOG] Text too short or empty. Returning original.")
        return text
    try:
        truncated = text[:4000]
        print(f"[LOG] Summarizing text ({len(truncated)} chars)...")
        summary = summarizer(truncated, max_length=250, min_length=80, do_sample=False)
        return summary[0]["summary_text"].strip()
    except Exception as e:
        print(f"[ERROR] Summarization failed: {e}")
        return None

# =====================================================================
# MAIN HANDLER
# =====================================================================
def handle_summarization(file=None, text=None, youtube_url=None):
    print("\n--- Starting Summarization Workflow ---")
    
    extracted_text = None
    
    if youtube_url:
        extracted_text = transcribe_youtube(youtube_url)
        if not extracted_text:
            return {"error": "Failed to transcribe YouTube video."}, 500
    elif file:
        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        print(f"[LOG] File saved to {upload_path}")
        extracted_text = extract_text_from_file(upload_path)
        os.remove(upload_path)
        print(f"[LOG] Temporary file removed: {upload_path}")
    else:
        extracted_text = text or ""

    if not extracted_text:
        return {"error": "No readable text found."}, 400

    summarized = summarize_text(extracted_text)
    if not summarized:
        return {"error": "Summarization failed."}, 500

    summary_filename = f"summary_{os.getpid()}.txt"
    summary_path = os.path.join(GENERATED_FOLDER, summary_filename)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summarized)

    print(f"[SUCCESS] Summary saved -> {summary_path}")
    return {"summary": summarized, "file_path": summary_path}, 200
