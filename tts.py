#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "piper-tts",
# ]
# ///

import argparse
from pathlib import Path

from piper import PiperVoice


def text_to_speech(text_file: str, output_file: str, model_path: str):
    with open(text_file, "r") as f:
        text = f.read()

    print(f"Reading text: {text}")

    print(f"Loading voice model: {model_path}")
    voice_model = PiperVoice.load(model_path)

    print(f"Synthesizing speech to {output_file}...")
    with open(output_file, "wb") as f:
        voice_model.synthesize(text, f)

    print(f"Speech saved to {output_file}")


if __name__ == "__main__":
    default_model = Path(__file__).parent / "en_US-hfc_female-medium.onnx"

    parser = argparse.ArgumentParser(
        description="Convert text to speech using Piper TTS"
    )
    parser.add_argument("--text_file", required=True, help="Path to input text file")
    parser.add_argument("--output_file", required=True, help="Path to output WAV file")
    parser.add_argument(
        "--model_path",
        default=str(default_model),
        help="Path to Piper model file (.onnx) (default: en_US-hfc_female-medium.onnx in script directory)",
    )

    args = parser.parse_args()

    text_to_speech(args.text_file, args.output_file, args.model_path)
