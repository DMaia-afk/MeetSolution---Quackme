# MeetSolution

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)


MeetSolution is a comprehensive tool for recording, transcribing, and summarizing meeting audio using advanced AI technologies. It leverages WhisperX for speaker diarization and transcription, and integrates with Ollama for generating structured summaries of meetings.

### Why Choose WhisperX and Ollama?
MeetSolution prioritizes cost-effective, open-source AI solutions:
- **WhisperX**: Free and open-source, runs locally without API costs. Provides high-accuracy transcription and diarization at no recurring expense, unlike paid cloud services (e.g., OpenAI Whisper API charges per minute).
- **Ollama**: Enables local LLM inference with models like deepseek-r1:8b, eliminating subscription fees for summarization. Once set up, it's free to use indefinitely, avoiding token-based pricing from services like OpenAI GPT.

This approach ensures zero operational costs after initial hardware investment, making MeetSolution ideal for budget-conscious users or organizations handling frequent meetings.

## Features

- Audio Recording: Record from microphone and system loopback simultaneously.
- Speaker Diarization: Automatically identify and label speakers.
- Transcription: Generate accurate transcriptions with timestamps.
- Summarization: Create structured summaries in English, extracting key info.
- Configurable Settings: Adjust model, language, device, and more.
- File Management: Auto-save transcriptions and summaries with descriptive names.

## Quick Start

1. Clone & Install:
   ```bash
   git clone https://github.com/DMaia-afk/MeetSolution---Quackme.git
   cd MeetSolution---Quackme
   pip install -r requirements.txt
   ```

2. Run:
   ```bash
   python main.py
   ```

3. Enjoy! Navigate the menus to record, transcribe, and summarize.

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for audio processing. Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH.
- **Ollama**: For summarization. Install from [Ollama website](https://ollama.com/) and pull the `deepseek-r1:8b` model:
  ```
  ollama pull deepseek-r1:8b
  ```
- **Hugging Face Account**: For speaker diarization. Get a token from [Hugging Face](https://huggingface.co/settings/tokens).

### Windows-Specific Requirements

On Windows, MeetSolution must be run in **PowerShell** (not Command Prompt) due to the need for symbolic links (symlinks). The underlying libraries (such as PyAnnote and WhisperX) download and cache AI models that require symlinks for proper functionality. PowerShell supports symlinks natively, while Command Prompt has limited support, which can lead to errors during model loading or transcription.

- Ensure you are using PowerShell for all commands and script execution.
- If you encounter symlink-related errors, verify that your user account has permissions to create symlinks (run PowerShell as Administrator if needed).

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/DMaia-afk/MeetSolution---Quackme.git
   cd MeetSolution---Quackme
   ```

2. **Create a virtual environment**:
   ```
   python -m venv env
   ```

3. **Activate the environment**:
   - Windows: `.\env\Scripts\activate`
   - Linux/Mac: `source env/bin/activate`

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not available, install manually:
   ```
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # Adjust for your CUDA version
   pip install whisperx pyannote.audio langchain-ollama langchain-core python-dotenv colorama sounddevice soundfile scipy numpy
   ```

5. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   Huggingface_TOKEN=your_huggingface_token_here
   ```

## Configuration

Access the settings menu to adjust:
- **Hugging Face Token**: Update your API token.
- **Device**: Choose CPU or CUDA (auto-detected).
- **Model Name**: Default is "medium" (options: tiny, base, small, medium, large).
- **Language**: Set to "pt" for Portuguese or "en" for English (None for auto-detection).
- **Batch Size**: Adjust based on GPU memory.
- **Compute Type**: int8, float16, or float32.

Changes are applied in real-time.

## Audio Recording Setup

MeetSolution can record from both microphone and system audio (loopback) simultaneously for comprehensive meeting capture.

### Windows Loopback Setup

1. **Enable Stereo Mix**:
   - Right-click the speaker icon in the taskbar → **Open Sound settings**.
   - Under **Input**, check if "Stereo Mix" or "What U Hear" is available. If not:
     - Right-click in the Input section → **Show disabled devices**.
     - Enable "Stereo Mix" or similar.
   - If not present, install/update audio drivers or use third-party tools like VB-Audio Virtual Cable.

2. **Test Recording**:
   - In MeetSolution, when prompted for "loopback device ID", select the Stereo Mix device.
   - Play audio on your computer and record a test to ensure it's captured.

### Linux/Mac Setup

- Linux: Use `pactl` or PulseAudio to set up loopback.
- Mac: Use "Soundflower" or "BlackHole" for virtual audio routing.

For detailed guides, search for "enable stereo mix [your OS]".

## Cloud Alternatives for Reduced Hardware Usage

MeetSolution is designed to run locally for privacy and offline capabilities, but if you want to minimize hardware requirements (e.g., no GPU needed), you can replace local components with cloud APIs. Note that this requires internet and may incur costs.

### Replacing WhisperX with OpenAI Whisper API
WhisperX uses local Whisper models for transcription and diarization. For a cloud alternative:
- Use OpenAI's Whisper API for transcription (no diarization included).
- For diarization, integrate with services like AssemblyAI or Google Cloud Speech-to-Text, which support speaker diarization.
- Modify `diarization.py` to call these APIs instead of local models.
- Pros: No local GPU/CPU intensive processing.
- Cons: Requires API keys, internet, potential latency, and costs per minute of audio.

### Replacing Ollama with OpenAI API
Ollama runs LLMs locally. For a cloud alternative:
- Use OpenAI's GPT models (e.g., GPT-4) via LangChain's `langchain-openai`.
- Update `summarizer.py` to use `ChatOpenAI` instead of `Ollama`.
- Set your OpenAI API key in `.env` as `OPENAI_API_KEY`.
- Pros: No local model storage or computation.
- Cons: Requires API key, internet, and pay-per-token usage.

To implement these changes, fork the repository and modify the respective files. For guidance, check the LangChain documentation or contact the maintainers.

## Limitations

While MeetSolution offers powerful local processing for privacy and offline use, running AI models like WhisperX and Ollama on local hardware has significant limitations:

- **Hardware Requirements**: Requires a capable GPU (e.g., NVIDIA with CUDA support) for efficient transcription and summarization. On CPU-only systems, processing can be extremely slow (hours for long audio files) or fail due to memory constraints.
- **Memory Usage**: Large models (e.g., Whisper "large" or Ollama's deepseek-r1:8b) can consume 8-16GB+ of RAM/VRAM, limiting usability on low-end machines.
- **Processing Time**: Local inference is slower than cloud APIs, especially for long meetings, and may not handle real-time or batch processing well. The processing time often grows exponentially with audio length due to hardware limitations:  
  **Time ∝ Audio Length ^ k** (where k > 1, e.g., for diarization, k ≈ 2-3 depending on model complexity). For example, a 10-minute audio might take 5 minutes, but a 1-hour audio could take hours or fail on low-end hardware.
- **Model Updates**: Local models don't auto-update and may become outdated compared to cloud services.
- **Scalability**: Not suitable for high-volume or concurrent usage without powerful hardware.
- **Compatibility**: May not work on all systems due to driver issues (e.g., CUDA versions) or OS limitations (e.g., Windows symlinks).

For users with limited hardware, consider the cloud alternatives above to offload computation while maintaining functionality.

## Performance Optimizations

To address the exponential growth in processing time due to hardware limitations, MeetSolution includes built-in RAM cleanup mechanisms. When transcription or summarization processes finish, the application automatically clears cached models and intermediate data from memory. This prevents RAM accumulation that could otherwise slow down subsequent processing or cause failures on low-end hardware. For example:
- Models are unloaded after use.
- Temporary variables are explicitly deleted.
- Garbage collection is triggered to free up resources.

These optimizations help maintain consistent performance across multiple runs, especially for longer audio files, by ensuring fresh memory allocation for each task.

## Project Structure

```
MeetSolution/
├── main.py                 # Main application with CLI menus
├── diarization.py          # Transcription and diarization logic
├── record.py               # Audio recording functions
├── summarizer.py           # Summarization using Ollama
├── all_tests/              # Test files (transcriptions, audio samples)
├── env/                    # Virtual environment (ignored)
├── .env                    # Environment variables (ignored)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Troubleshooting

- **Module not found**: Ensure the virtual environment is activated and dependencies are installed.
- **CUDA issues**: If using GPU, ensure PyTorch is installed with CUDA support.
- **Audio recording fails**: Check microphone permissions and FFmpeg installation.
- **Ollama not responding**: Ensure Ollama is running and the model is pulled.
- **Hugging Face errors**: Verify your token in `.env`.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -am 'Add feature'`.
4. Push: `git push origin feature-name`.
5. Submit a pull request.

## License

This unlicensed project

## Acknowledgments

- [WhisperX](https://github.com/m-bain/whisperX) for transcription and diarization.
- [PyAnnote](https://github.com/pyannote/pyannote-audio) for speaker diarization.
- [Ollama](https://ollama.com/) for local LLM inference.
- [LangChain](https://www.langchain.com/) for prompt management.
- Special thanks to the creators of the ["Board Meeting Example" video](https://www.youtube.com/watch?v=WBXJEJCsULw&t=8s) used for testing MeetSolution's transcription and summarization capabilities.</content>
<parameter name="filePath">c:\Users\Dmaia-AFK\Desktop\Estudos\Python\Quackme - MeetSolution\README.md
