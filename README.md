# Video-to-Audio Transcription Tool

Converts your damn videos to audio (.wav) and transcribes them using mlx_whisper. Drop your videos in the `videos/` folder, and you'll get WAV files in `audio/` and text files in `transcriptions/`.

## Requirements

- Python 3.7+
- **ffmpeg** (must be in your PATH)
- Python packages: `tqdm`, `mlx_whisper`
- Uses the FUCKING package manager [uv](https://astral.sh/uv) for dependency management and running scripts

## Setup

1. Clone this repo.
2. Install dependencies with uv:
   ```bash
   uv add tqdm mlx_whisper
