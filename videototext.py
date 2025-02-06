import os
import sys
import subprocess
from pathlib import Path
from tqdm import tqdm
from mlx_whisper import transcribe

# Define directories
VIDEO_DIR = Path('videos')
AUDIO_DIR = Path('audio')
TRANSCRIPTIONS_DIR = Path('transcriptions')

# Create directories if they don't exist
VIDEO_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
TRANSCRIPTIONS_DIR.mkdir(exist_ok=True)

def convert_video_to_audio(input_video_path, output_audio_path):
    """
    Convert video file to audio using ffmpeg.
    
    Args:
        input_video_path (str): Path to input video file
        output_audio_path (str): Path to output audio file
    """
    try:
        # Convert video to audio using ffmpeg
        command = [
            'ffmpeg', '-i', input_video_path,
            '-vn',  # Disable video
            '-acodec', 'pcm_s16le',  # Audio codec
            '-ar', '16000',  # Sample rate
            '-ac', '1',  # Mono audio
            '-y',  # Overwrite output file
            output_audio_path
        ]
        
        subprocess.run(command, check=True, capture_output=True)
        print(f"  Successfully converted '{input_video_path}' to audio")
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting video to audio: {e}")
        print(f"ffmpeg output: {e.output.decode()}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: ffmpeg command not found. Please ensure ffmpeg is installed and in your system's PATH.")
        sys.exit(1)

def transcribe_audio(audio_path):
    """
    Transcribes audio using Whisper model in MLX.
    
    Args:
        audio_path (str): Path to the audio file (must be .wav)
    
    Returns:
        str: The transcribed text.
    """
    try:
        # Define path to local model
        model_path = "/Users/jackberger/.lmstudio/models/mlx-community/whisper-large-v3-turbo"
        
        # Transcribe audio
        result = transcribe(audio_path, path_or_hf_repo=model_path)
        return result['text'].strip()
        
    except Exception as e:
        print(f"Error during transcription of '{audio_path}': {e}")
        return None

def main():
    # Get all video files in videos directory
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    video_files = [f for ext in video_extensions for f in VIDEO_DIR.glob(f'*{ext}')]
    
    if not video_files:
        print(f"No video files found in {VIDEO_DIR}. Please place your videos there.")
        return

    print(f"Found {len(video_files)} video(s) in {VIDEO_DIR}:")
    for video in video_files:
        print(f"  - {video.name}")

    print("\nStarting video to audio conversion and transcription process...")
    for input_video_path in tqdm(video_files, desc="Processing videos"):
        # Create output paths
        base_name = input_video_path.stem
        output_audio_path = AUDIO_DIR / f"{base_name}.wav"
        output_transcription_path = TRANSCRIPTIONS_DIR / f"{base_name}.txt"

        print(f"\nProcessing '{input_video_path.name}':")
        print(f"  Converting video to audio...")
        convert_video_to_audio(str(input_video_path), str(output_audio_path))

        print(f"  Transcribing audio using Whisper...")
        transcription = transcribe_audio(str(output_audio_path))

        if transcription:
            # Save transcription to file
            with open(output_transcription_path, 'w') as f:
                f.write(transcription)
            print(f"  Transcription saved to {output_transcription_path}")
        else:
            print(f"  Failed to transcribe '{input_video_path.name}'")

if __name__ == "__main__":
    main()
