import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
from datetime import datetime
import threading
import time

#----
# Configuration
#----

SAMPLE_RATE = 44100  # Sample rate for recording (common for most devices)
CHANNELS = 1        # Mono audio

def dynamic_name():
    return datetime.now().strftime("recorded_audio_%Y%m%d_%H%M%S.wav")

def list_input_devices():
    print("Available audio input devices:")
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"{idx}: {device['name']}")
    
    return devices

def record_audio_dual(filename=None, mic_device=None, loopback_device=None):
    FILENAME = filename if filename else dynamic_name()

    devices = list_input_devices()
    
    # If devices not specified, prompt user
    if mic_device is None:
        try:
            mic_device = int(input("Enter microphone device ID: "))
        except ValueError:
            print("Invalid input. Using default.")
            mic_device = None
    
    if loopback_device is None:
        try:
            loopback_device = int(input("Enter loopback device ID (e.g., Stereo Mix): "))
        except ValueError:
            print("Invalid input. Using default.")
            loopback_device = None

    # Get default sample rates for devices
    mic_rate = devices[mic_device]['default_samplerate'] if mic_device is not None else SAMPLE_RATE
    loopback_rate = devices[loopback_device]['default_samplerate'] if loopback_device is not None else SAMPLE_RATE
    
    # Use the higher rate or a common one
    actual_rate = max(mic_rate, loopback_rate, 44100)
    print(f"Using sample rate: {actual_rate} Hz")

    mic_data = []
    loopback_data = []
    stop_recording = threading.Event()

    def mic_callback(indata, frames, time, status):
        if status:
            print(f"Mic status: {status}")
        mic_data.append(indata.copy())

    def loopback_callback(indata, frames, time, status):
        if status:
            print(f"Loopback status: {status}")
        loopback_data.append(indata.copy())

    # Create streams with device-specific rates
    mic_stream = sd.InputStream(
        samplerate=mic_rate,
        channels=CHANNELS,
        callback=mic_callback,
        dtype='int16',
        device=mic_device
    )

    loopback_stream = sd.InputStream(
        samplerate=loopback_rate,
        channels=CHANNELS,
        callback=loopback_callback,
        dtype='int16',
        device=loopback_device
    )

    with mic_stream, loopback_stream:
        print("Recording started from microphone and loopback.\n")
        print("Press ENTER to stop recording.")
        input()  # Wait for user to press Enter
        print("Recording stopped.")

    # Mix the recordings (resample if needed)
    if mic_data and loopback_data:
        mic_recording = np.concatenate(mic_data, axis=0)
        loopback_recording = np.concatenate(loopback_data, axis=0)
        
        # Resample to common rate if different
        if mic_rate != actual_rate:
            from scipy.signal import resample
            mic_recording = resample(mic_recording.astype(float), int(len(mic_recording) * actual_rate / mic_rate)).astype(np.int16)
        if loopback_rate != actual_rate:
            from scipy.signal import resample
            loopback_recording = resample(loopback_recording.astype(float), int(len(loopback_recording) * actual_rate / loopback_rate)).astype(np.int16)
        
        # Ensure same length
        min_len = min(len(mic_recording), len(loopback_recording))
        mic_recording = mic_recording[:min_len]
        loopback_recording = loopback_recording[:min_len]
        
        # Mix (average)
        mixed_recording = (mic_recording.astype(np.float32) + loopback_recording.astype(np.float32)) / 2
        mixed_recording = mixed_recording.astype(np.int16)
        
        wav.write(FILENAME, int(actual_rate), mixed_recording)
        print(f"Mixed audio saved to {FILENAME}")
        return FILENAME
    else:
        print("No data recorded.")
        return None

if __name__ == "__main__":
    record_audio_dual()
