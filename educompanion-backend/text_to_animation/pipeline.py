"""
Text-to-Animation: End-to-end prototype
File: text_to_animation_full_project.py

This single-file prototype implements a workable pipeline to convert
handwritten note images (or typed images) into a short animated explainer
video. It uses easyocr for OCR, Hugging Face transformers for summarization,
gTTS for text-to-speech, and MoviePy + PIL for simple animated slides.

This is intended as a practical, runnable MVP — not a production system.

Requirements (install with pip):
    pip install easyocr torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install transformers sentencepiece
    pip install gtts moviepy pillow opencv-python streamlit

If you don't have a GPU, install CPU versions of torch. Transformer
summarization may be slow on CPU. For faster development, use smaller
models (e.g., 'sshleifer/distilbart-cnn-12-6').

Usage examples:
    python text_to_animation_full_project.py --input_image notes.jpg --out_video out.mp4

Or run the Streamlit demo:
    streamlit run text_to_animation_full_project.py -- --streamlit

Sections in this file:
- Imports & config
- OCR: extract_text_from_image()
- NLP: clean_text() and summarize_text()
- TTS: text_to_speech()
- Animation: create_slides_from_summary() and make_video_from_slides()
- Pipeline: run_pipeline()
- Streamlit app (if run with --streamlit)

"""

import os
import io
import sys
import time
import argparse
from typing import List

# OCR
import easyocr
import cv2
from PIL import Image, ImageDraw, ImageFont

# NLP
from transformers import pipeline

# TTS
from gtts import gTTS

# Video
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

# Model Cache for performance optimization
from .model_cache import get_fast_summarizer, get_fast_ocr_reader, preload_all_models
from .intelligent_animator import create_intelligent_animation, ContentAnalyzer
from .pdf_utils import convert_pdf_to_images, is_pdf_file

# Streamlit
try:
    import streamlit as st
except Exception:
    st = None

# ------------------------- Configuration -------------------------
OCR_LANGS = ['en']  # adjust if notes have other languages
# Performance optimized models - choose based on speed vs quality needs
SUMMARIZER_MODEL = 'sshleifer/distilbart-cnn-12-6'  # Fast, good quality (recommended)
# SUMMARIZER_MODEL = 'facebook/bart-large-cnn'  # Slower but higher quality
# SUMMARIZER_MODEL = 't5-small'  # Very fast, decent quality
FONT_PATH = None  # optional: path to a .ttf font for rendering text on slides
TMP_DIR = 'ttm_tmp'
os.makedirs(TMP_DIR, exist_ok=True)

# ------------------------- OCR -------------------------
def get_easyocr_reader():
    """Get cached OCR reader for better performance"""
    return get_fast_ocr_reader(OCR_LANGS, gpu=False)


def extract_text_from_image(image_path: str) -> str:
    """Run EasyOCR on image and return concatenated text."""
    reader = get_easyocr_reader()
    results = reader.readtext(image_path, detail=0)
    # results is a list of strings in reading order approximation
    text = "\n".join(results)
    return text

# ------------------------- NLP / Summarization -------------------------
def get_summarizer():
    """Get cached summarization pipeline for better performance"""
    return get_fast_summarizer(SUMMARIZER_MODEL)


def clean_text(text: str) -> str:
    # Very small cleaning: remove repetitive whitespace
    return "\n".join([line.strip() for line in text.splitlines() if line.strip()])


def summarize_text(text: str, max_length=130, min_length=30) -> str:
    summarizer = get_summarizer()
    # HuggingFace summarizers expect reasonably long input; chunk if needed
    # Simple chunker by characters
    CHUNK_SIZE = 1000
    if len(text) <= CHUNK_SIZE:
        out = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return out[0]['summary_text']

    chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    summaries = []
    for c in chunks:
        s = summarizer(c, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(s[0]['summary_text'])
    combined = ' '.join(summaries)
    # optionally summarize again
    out = summarizer(combined, max_length=max_length, min_length=min_length, do_sample=False)
    return out[0]['summary_text']

# ------------------------- TTS -------------------------

def text_to_speech(text: str, out_path: str, lang='en') -> str:
    """Use gTTS to create an mp3 audio file from text and return path."""
    tts = gTTS(text=text, lang=lang)
    tts.save(out_path)
    return out_path

# ------------------------- Animation / Video generation -------------------------

def split_summary_to_slides(summary: str, max_chars=200) -> List[str]:
    """Split summary into smaller slide-sized text chunks."""
    words = summary.split()
    slides = []
    cur = []
    cur_len = 0
    for w in words:
        if cur_len + len(w) + 1 > max_chars:
            slides.append(' '.join(cur))
            cur = [w]
            cur_len = len(w)
        else:
            cur.append(w)
            cur_len += len(w) + 1
    if cur:
        slides.append(' '.join(cur))
    return slides


def create_slide_image(text: str, out_path: str, size=(1280, 720), bgcolor=(255,255,255)) -> str:
    """Render a single slide with text using PIL and save to out_path."""
    W, H = size
    img = Image.new('RGB', size, color=bgcolor)
    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        if FONT_PATH and os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, 36)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Simple text wrapping
    margin = 40
    max_w = W - 2*margin
    words = text.split()
    lines = []
    cur = ''
    for w in words:
        test = cur + (' ' if cur else '') + w
        # Use textbbox instead of deprecated textsize
        bbox = draw.textbbox((0, 0), test, font=font)
        wsize = bbox[2] - bbox[0]  # width = right - left
        if wsize <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    y = margin
    # Calculate line height using textbbox instead of deprecated textsize
    bbox = draw.textbbox((0, 0), 'A', font=font)
    line_h = (bbox[3] - bbox[1]) + 8  # height = bottom - top + spacing
    for line in lines:
        draw.text((margin, y), line, fill=(0,0,0), font=font)
        y += line_h
        if y > H - margin:
            break

    img.save(out_path)
    return out_path


def make_video_from_slides(slide_paths: List[str], audio_path: str, out_video_path: str, slide_duration=4):
    """Create a video from slide images, apply simple crossfade transitions and merge audio."""
    clips = []
    for sp in slide_paths:
        clip = ImageClip(sp).set_duration(slide_duration)
        clips.append(clip)

    video = concatenate_videoclips(clips, method='compose')

    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        # Ensure video length >= audio length; if video shorter, extend last slide
        if video.duration < audio.duration:
            diff = audio.duration - video.duration
            last = clips[-1].fx(lambda c: c).set_duration(clips[-1].duration + diff)
            clips[-1] = last
            video = concatenate_videoclips(clips, method='compose')
        video = video.set_audio(audio)

    # write the file
    video.write_videofile(out_video_path, fps=24, codec='libx264', audio_codec='aac')
    return out_video_path

# ------------------------- Pipeline -------------------------

def run_pipeline(input_file: str, output_video: str):
    """Main pipeline: PDF/Image -> text -> summary -> animated video with dynamic visualizations."""
    # Initialize performance optimizations
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Preload models if configured
        if config.get('performance', {}).get('preload_models', False):
            print("🚀 Using preloaded models for faster processing...")
            preload_all_models(config)
    except Exception as e:
        print(f"Warning: Could not load config for optimization: {e}")

    print('1) Processing input file...')
    start_time = time.time()

    # Handle PDF files
    if is_pdf_file(input_file):
        print(f'📄 Detected PDF file: {input_file}')
        try:
            # Convert PDF to images
            pdf_images = convert_pdf_to_images(input_file, dpi=300)
            print(f'✅ Converted PDF to {len(pdf_images)} images')

            # Extract text from each page
            all_text = []
            for i, image_path in enumerate(pdf_images):
                print(f'🔍 Processing page {i+1}/{len(pdf_images)}...')
                page_text = extract_text_from_image(image_path)
                if page_text.strip():
                    all_text.append(f"--- Page {i+1} ---\n{page_text}")
                else:
                    print(f'⚠️ No text found on page {i+1}')

            raw_text = "\n\n".join(all_text)
            print(f'✅ Extracted text from {len(pdf_images)} PDF pages')

        except Exception as e:
            print(f'❌ PDF processing failed: {e}')
            raise
    else:
        # Handle image files directly
        print(f'🖼️ Processing image file: {input_file}')
        raw_text = extract_text_from_image(input_file)

    raw_text = clean_text(raw_text)
    print(f'OCR completed in {time.time() - start_time:.2f}s')
    print('OCR result (first 500 chars):')
    print(raw_text[:500])

    print('\n2) Summarization...')
    start_time = time.time()
    summary = summarize_text(raw_text)
    print(f'Summarization completed in {time.time() - start_time:.2f}s')
    print('Summary:')
    print(summary)

    print('\n3) Analyzing content and creating intelligent animation...')
    start_time = time.time()
    
    # Use intelligent animation system
    try:
        # Combine raw text and summary for better content analysis
        full_content = raw_text + "\n\n" + summary
        
        # Create intelligent animation based on content type
        video_path = create_intelligent_animation(full_content, output_video)
        print(f'Intelligent animation completed in {time.time() - start_time:.2f}s')
        print(f'✅ Animated video created: {video_path}')
        return
        
    except Exception as e:
        print(f"⚠️ Intelligent animation failed ({e}), falling back to standard slides...")
    
    # Fallback to standard slide-based video
    print("📄 Creating standard slide presentation...")
    
    print('\n4) TTS...')
    start_time = time.time()
    audio_path = os.path.join(TMP_DIR, 'tts_output.mp3')
    text_to_speech(summary, audio_path)
    print(f'TTS completed in {time.time() - start_time:.2f}s')

    print('\n5) Slide generation...')
    start_time = time.time()
    slides = split_summary_to_slides(summary, max_chars=220)
    slide_paths = []
    for i, s in enumerate(slides):
        p = os.path.join(TMP_DIR, f'slide_{i}.png')
        create_slide_image(s, p)
        slide_paths.append(p)
    print(f'Slide generation completed in {time.time() - start_time:.2f}s')

    print('\n6) Video rendering...')
    start_time = time.time()
    make_video_from_slides(slide_paths, audio_path, output_video, slide_duration=4)
    print(f'Video rendering completed in {time.time() - start_time:.2f}s')

    print(f'\n✅ Pipeline complete. Output video: {output_video}')

# ------------------------- Streamlit demo -------------------------

def streamlit_app():
    st.title('Handwritten Notes → Animated Explainer (Prototype)')
    st.markdown('Upload an image of handwritten notes and get a short animated explainer video.')

    uploaded = st.file_uploader('Upload note image (jpg/png/pdf page)', type=['png','jpg','jpeg'])
    if uploaded is None:
        st.info('Upload an image to start')
        return

    # Save uploaded file
    in_path = os.path.join(TMP_DIR, 'user_upload.png')
    with open(in_path, 'wb') as f:
        f.write(uploaded.getbuffer())

    if st.button('Run pipeline'):
        with st.spinner('Processing (OCR -> Summarize -> TTS -> Video)...'):
            out_vid = os.path.join(TMP_DIR, 'output_demo.mp4')
            run_pipeline(in_path, out_vid)
        st.success('Done!')
        st.video(out_vid)

# ------------------------- CLI & entry -------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_image', type=str, help='Path to input note image')
    parser.add_argument('--out_video', type=str, default='out.mp4')
    parser.add_argument('--streamlit', action='store_true', help='Run streamlit app (if specified)')
    args, unknown = parser.parse_known_args()

    if args.streamlit:
        # When streamlit runs this file, it passes control differently; run the app
        if st is None:
            print('Streamlit not installed. Install with: pip install streamlit')
            sys.exit(1)
        streamlit_app()
        return

    if not args.input_image:
        print('Provide --input_image path or use --streamlit')
        sys.exit(1)

    run_pipeline(args.input_image, args.out_video)

if __name__ == '__main__':
    main()
