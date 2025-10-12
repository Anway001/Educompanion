import os
import fitz  # PyMuPDF
import pyttsx3
from pydub import AudioSegment
import ollama
import re
import multiprocessing
from PyPDF2 import PdfReader
from transformers import pipeline
import easyocr
import torch
import random

# =========================================================================
# 1. Configuration and Initialization
# =========================================================================
print("Initializing models and configuration...")

UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

print("Loading EasyOCR model...")
ocr_reader = easyocr.Reader(['en'], gpu=(DEVICE == "cuda"))

print("Loading summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if DEVICE == "cuda" else -1)

voice_ids = {"HOST": None, "GUEST": None}

def setup_tts_voices():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        english_voices = [v for v in voices if v.languages and 'en' in v.languages[0].lower()]
        
        print(f"[SETUP] Found {len(english_voices)} English voices available.")

        if len(english_voices) >= 2:
            selected_voices = random.sample(english_voices, 2)
            voice_ids["HOST"] = selected_voices[0].id
            voice_ids["GUEST"] = selected_voices[1].id
            print("[SETUP] Randomly selected two distinct English voices.")
        elif len(english_voices) == 1:
            voice_ids["HOST"] = english_voices[0].id
            voice_ids["GUEST"] = english_voices[0].id
            print("[SETUP] WARNING: Only one English voice found. Using it for both speakers.")
        else:
            print("[SETUP] CRITICAL: No English voices found! Falling back to any available voices.")
            if len(voices) >= 2:
                voice_ids["HOST"] = voices[0].id
                voice_ids["GUEST"] = voices[1].id
            elif len(voices) == 1:
                 voice_ids["HOST"] = voice_ids["GUEST"] = voices[0].id
            else:
                raise RuntimeError("No TTS voices found on this system.")
        
        engine.stop()
        print(f"TTS voices selected -> HOST: {voice_ids['HOST']}, GUEST: {voice_ids['GUEST']}")

    except Exception as e:
        print(f"[CRITICAL] Failed to initialize TTS engine or find voices: {e}")


setup_tts_voices()
print("\nInitialization Complete.\n")

# =========================================================================
# 2. Helper Functions
# =========================================================================

def _extract_text_pypdf2(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"[LOG] PyPDF2 extraction failed: {e}")
    return text.strip()

def _extract_text_ocr(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            result = ocr_reader.readtext(img_bytes, detail=0, paragraph=True)
            text += " ".join(result) + "\n"
    except Exception as e:
        print(f"[LOG] OCR extraction failed: {e}")
    return text.strip()

def extract_text_from_file(file_path):
    print(f"[LOG] STEP 1: Starting text extraction from {file_path}")
    if file_path.lower().endswith('.pdf'):
        text = _extract_text_pypdf2(file_path)
        if text: return text
        print("[LOG] No text found directly. Falling back to OCR...")
        return _extract_text_ocr(file_path)
    elif file_path.lower().endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f: return f.read().strip()
        except Exception as e:
            print(f"[LOG] ERROR reading TXT file: {e}")
            return None
    else:
        print(f"[LOG] Unsupported file type: {file_path}")
        return None

def summarize_text(text):
    if not text or len(text.split()) < 60:
        print("[LOG] Text is too short, skipping summarization.")
        return text
    try:
        max_chars = 4000 
        truncated_text = text[:max_chars]
        print(f"[LOG] Summarizing text (truncated to {max_chars} chars)...")
        summary = summarizer(truncated_text, max_length=200, min_length=50, do_sample=False)
        summary_text = summary[0]['summary_text']
        print(f"[LOG] Summarization complete. New length: {len(summary_text)}")
        return summary_text
    except Exception as e:
        print(f"[LOG] Summarization failed: {e}. Using original text.")
        return text

def generate_podcast_script_with_llm(notes_text, length='medium'):
    print(f"[LOG] STEP 2: Generating podcast script with LLM (Target length: {length})...")
    length_to_words = {
        'short': 400, 'medium': 900, 'long': 2000
    }
    target_words = length_to_words.get(length, 900)
    prompt = f"""
    You are a podcast script writer. Your ONLY job is to create a script.
    You MUST create a conversational script between a "HOST" and a "GUEST" from the notes below.
    RULES:
    1.  The script's total word count MUST be approximately {target_words} words.
    2.  Every single line MUST start with either `HOST:` or `GUEST:`.
    3.  Do NOT write any introduction or text that does not follow this format.
    NOTES:
    ---
    {notes_text}
    ---
    """
    try:
        response = ollama.generate(model="llama3", prompt=prompt)
        print("[LOG] LLM script generation successful.")
        return response['response']
    except Exception as e:
        print(f"[LOG] ERROR: LLM script generation failed: {e}")
        return None

def parse_script(script_text):
    print("[LOG] STEP 3: Parsing the generated script...")
    print(f"\n--- LLM Raw Output Start ---\n{script_text}\n--- LLM Raw Output End ---\n")
    cleaned_script = script_text.replace('**', '').replace('*', '')
    pattern = re.compile(r'^\s*(HOST|GUEST)\s*:\s*(.*)', re.IGNORECASE | re.MULTILINE)
    matches = pattern.findall(cleaned_script)
    parsed_script = [(speaker.upper(), dialogue.strip()) for speaker, dialogue in matches if dialogue.strip()]
    if parsed_script:
        print(f"[LOG] Parsing successful. Found {len(parsed_script)} lines.")
        return parsed_script
    else:
        print("[LOG] ERROR: Parsing failed.")
        return None

def _worker_synthesize(text, voice_id, temp_wav_path):
    try:
        engine = pyttsx3.init()
        engine.setProperty('voice', voice_id)
        engine.setProperty('rate', 155)
        engine.save_to_file(text, temp_wav_path)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS Worker failed: {e}")


# MODIFIED: This function now uses absolute paths to be safer for multiprocessing.
def create_multi_speaker_podcast(script, output_path):
    print("[LOG] STEP 4: Starting audio generation and assembly (Multiprocessing Mode)...")
    final_podcast = AudioSegment.silent(duration=500)
    silence_between_speakers = AudioSegment.silent(duration=800)
    
    # NEW: Get the absolute path of the directory where you are running the script (your project's root)
    project_root = os.getcwd()
    
    # The temp directory path is now built from the project's root
    temp_dir = os.path.join(project_root, GENERATED_FOLDER, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for i, (speaker, text) in enumerate(script):
            voice_id = voice_ids.get(speaker, voice_ids['HOST'])
            
            # MODIFIED: Create a full, absolute path for the temporary .wav file
            temp_wav_filename = f"temp_{i}_{os.getpid()}.wav"
            temp_wav_path = os.path.join(temp_dir, temp_wav_filename)
            
            print(f"[LOG] Generating audio for {speaker} (line {i+1}/{len(script)})...")
            
            process = multiprocessing.Process(target=_worker_synthesize, args=(text, voice_id, temp_wav_path))
            process.start()
            process.join(timeout=60)
            if process.is_alive():
                process.terminate()
                raise TimeoutError("TTS generation for a line took too long.")

            if os.path.exists(temp_wav_path):
                speech_segment = AudioSegment.from_wav(temp_wav_path)
                final_podcast += speech_segment + silence_between_speakers
                os.remove(temp_wav_path)
            else:
                # This error means the worker process failed to save the file.
                raise FileNotFoundError(f"TTS failed to create temp file: {temp_wav_path}")
        
        final_podcast.export(output_path, format="mp3", bitrate="192k")
    except Exception as e:
        print(f"[LOG] ERROR during audio creation: {e}")
        raise
    finally:
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)


# =========================================================================
# 3. Main Controller Logic
# =========================================================================
def handle_podcast_generation(notes_text=None, file=None, length='medium'):
    print("\n--- Starting New Podcast Generation Workflow ---")
    
    # NEW: Get the absolute path for the main file paths as well
    project_root = os.getcwd()
    
    if file:
        # Construct absolute path for saving the upload
        upload_path = os.path.join(project_root, UPLOAD_FOLDER, file.filename)
        print(f"[LOG] Saving uploaded file to {upload_path}")
        file.save(upload_path)
        extracted_text = extract_text_from_file(upload_path)
        os.remove(upload_path)
        notes_text = extracted_text
    
    if not notes_text or not notes_text.strip():
        return {"error": "Failed to get text from input source."}, 400

    summarized_notes = summarize_text(notes_text)
    script_text = generate_podcast_script_with_llm(summarized_notes, length)
    if not script_text: return {"error": "Failed to generate podcast script."}, 500
    
    parsed_script = parse_script(script_text)
    if not parsed_script: return {"error": "Failed to parse the generated script."}, 500

    base_filename = "podcast_output"
    if file:
        base_filename = os.path.splitext(file.filename)[0]
        base_filename = re.sub(r'[^a_zA_Z0-9_-]', '', base_filename)

    podcast_file_name = f"{base_filename}_{os.getpid()}.mp3"
    # Construct absolute path for the final output file
    podcast_path = os.path.join(project_root, GENERATED_FOLDER, podcast_file_name)
    
    try:
        create_multi_speaker_podcast(parsed_script, podcast_path)
    except Exception as e:
        print(f"--- Workflow Failed at audio creation: {e} ---")
        return {"error": f"Failed to create podcast audio: {str(e)}"}, 500
    
    print(f"--- Workflow Complete: Podcast generated at {podcast_path} ---")
    return {"path": podcast_path, "filename": podcast_file_name}, 200