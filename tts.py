#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "piper-tts",
# ]
# ///

"""Convert text to speech using Piper TTS"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to speech using Piper TTS"
    )
    parser.add_argument(
        "--text_file",
        required=True,
        help="Path to input text file"
    )
    parser.add_argument(
        "--output_file",
        required=True,
        help="Path to output WAV file"
    )
    parser.add_argument(
        "--model_path",
        help="Path to Piper model file (.onnx) (default: en_US-hfc_female-medium.onnx in script directory)"
    )

    args = parser.parse_args()

    # Read input text
    text_file = Path(args.text_file)
    if not text_file.exists():
        print(f"Error: Text file '{args.text_file}' not found", file=sys.stderr)
        sys.exit(1)

    text = text_file.read_text(encoding="utf-8")

    # Determine model path
    if args.model_path:
        model_path = Path(args.model_path)
    else:
        script_dir = Path(__file__).parent
        model_path = script_dir / "en_US-hfc_female-medium.onnx"

    if not model_path.exists():
        print(f"Error: Model file '{model_path}' not found", file=sys.stderr)
        sys.exit(1)

    # Import piper here after argument validation
    try:
        from piper import PiperVoice
        import wave
    except ImportError:
        print("Error: piper-tts is not installed", file=sys.stderr)
        sys.exit(1)

    # Generate speech
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    voice = PiperVoice.load(str(model_path))

    # Collect audio chunks and write to WAV file
    audio_chunks = []
    for chunk in voice.synthesize(text):
        audio_chunks.append(chunk)

    # Write WAV file
    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(voice.config.sample_rate)

        for chunk in audio_chunks:
            wav_file.writeframes(chunk.audio_int16_bytes)

    print(f"Successfully generated speech: {output_path}")


if __name__ == "__main__":
    main()
