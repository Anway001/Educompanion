import pyttsx3
import traceback

def _worker_synthesize(text, voice_id, temp_wav_path):
    """
    Worker function to synthesize text to speech.
    Must be top-level or in a separate module to work with multiprocessing on Windows.
    This file should NOT import heavy libraries (tensorflow, torch, etc.) to keep spawning fast.
    """
    try:
        # Initialize engine inside the process
        engine = pyttsx3.init()
        engine.setProperty('voice', voice_id)
        # engine.setProperty('rate', 165) # Adjusted speed if needed, keeping default or logic from controller
        engine.save_to_file(text, temp_wav_path)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS Worker failed: {e}")
        traceback.print_exc()
