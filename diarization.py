import whisperx
import torch
import os
import time
from dotenv import load_dotenv
from pyannote.audio import Pipeline
from omegaconf.listconfig import ListConfig
from omegaconf.base import ContainerMetadata
from typing import Any
import gc

# Disable symlinks for Hugging Face cache to avoid Windows privilege issues
os.environ['HF_HUB_DISABLE_SYMLINKS'] = '1'
os.environ['SB_CACHE_STRATEGY'] = 'local'

# Patch torch.load to use weights_only=False due to compatibility issues with pyannote models
original_load = torch.load
def patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = patched_load

torch.serialization.add_safe_globals([ListConfig, ContainerMetadata, Any])
load_dotenv()

# -------
# Configuration (defaults)
# -------
DEFAULT_CONFIGS = {
    "HUGGINGFACE_TOKEN": os.getenv("Huggingface_TOKEN"),
    "DEVICE": "cuda" if torch.cuda.is_available() else "cpu",
    "MODEL_NAME": "medium",
    "SPEAKER_COUNT": None,
    "MAX_SPEAKERS": 10,
    "BATCH_SIZE": 6,
    "LANGUAGE": None,
    "COMPUTE_TYPE": "int8"
}
# -------

def clean_memory(model):
    """
    Clean up GPU memory after model usage.
    """
    del model
    gc.collect()
    torch.cuda.empty_cache()

def transcription_with_diarization(audio_file, configs=DEFAULT_CONFIGS):
    device = configs["DEVICE"]
    model_name = configs["MODEL_NAME"]
    batch_size = configs["BATCH_SIZE"]
    language = configs["LANGUAGE"]
    compute_type = configs["COMPUTE_TYPE"]
    huggingface_token = configs["HUGGINGFACE_TOKEN"]
    speaker_count = configs["SPEAKER_COUNT"]
    max_speakers = configs["MAX_SPEAKERS"]
    
    print(f"Loading WhisperX model '{model_name}' on device '{device}'...")
    model = whisperx.load_model(model_name, device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result_transcriptions = model.transcribe(audio, batch_size=batch_size, language=language)

    # If language was None, use detected language for alignment
    if language is None:
        language = result_transcriptions["language"]
        print(f"Detected language: {language}")

    clean_memory(model)

    print(f"Loading alignment model and metadata...")
    model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
    result_aligned = whisperx.align(result_transcriptions["segments"], model_a, metadata, audio, device, interpolate_method='linear')

    clean_memory(model_a)

    print(f"Loading speaker diarization pipeline...")
    try:
        diarize_model = whisperx.diarize.DiarizationPipeline(model_name="pyannote/speaker-diarization", use_auth_token=huggingface_token)
    except OSError as e:
        if "1314" in str(e):
            print("Symlink creation failed due to Windows privileges. Please enable Developer Mode or run as administrator.")
            print("See: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development")
            raise
        else:
            raise
    diarize_segments = diarize_model(audio_file, num_speakers=speaker_count, max_speakers=max_speakers)

    clean_memory(diarize_model)

    final_result = whisperx.assign_word_speakers(diarize_segments, result_aligned)
    final_result = final_result["word_segments"]

    return final_result

def format_transcription(final_result):
    formatted_output = []
    current_speaker = None
    current_text = ""
    current_start = None
    current_end = None
    
    for segment in final_result:
        speaker = segment.get("speaker", "Unknown")
        if speaker != current_speaker:
            if current_speaker is not None:
                formatted_output.append({
                    "start": current_start,
                    "end": current_end,
                    "text": current_text.strip(),
                    "speaker": current_speaker
                })
            current_speaker = speaker
            current_text = segment["word"] + " "
            current_start = segment["start"]
            current_end = segment["end"]
        else:
            current_text += segment["word"] + " "
            current_end = segment["end"]
    
    # Add the last segment
    if current_speaker is not None:
        formatted_output.append({
            "start": current_start,
            "end": current_end,
            "text": current_text.strip(),
            "speaker": current_speaker
        })
    
    return formatted_output

def main():
    start_time = time.time()
    final_result = transcription_with_diarization(AUDIO_FILE)
    formatted_output = format_transcription(final_result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for segment in formatted_output:
            f.write(f"[{segment['start']:.2f}-{segment['end']:.2f}] Speaker {segment['speaker']}: {segment['text']}\n")
    end_time = time.time()

    print(f"Transcription and diarization completed in {end_time - start_time:.2f} seconds.")
    print(f"Results saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()