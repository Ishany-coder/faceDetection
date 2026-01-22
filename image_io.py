#!/usr/bin/env python3
"""
Image I/O CLI Tool
A simple command-line tool to read images and output them.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image


def load_image(input_path: str) -> Image.Image:
    """Load an image from the given path."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {input_path}")
    return Image.open(path)


def save_image(image: Image.Image, output_path: str) -> None:
    """Save an image to the given path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    print(f"Saved: {output_path}")


def process_images(input_paths: list[str], output_dir: str, show: bool = False) -> None:
    """Process multiple images: load and save them to output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for input_path in input_paths:
        try:
            image = load_image(input_path)

            if show:
                image.show()

            # Generate output filename
            input_name = Path(input_path).name
            out_file = output_path / input_name
            save_image(image, str(out_file))

        except Exception as e:
            print(f"Error processing {input_path}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Image I/O Tool - Read images and output them"
    )
    parser.add_argument(
        "input",
        nargs="+",
        help="Input image path(s)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for processed images"
    )
    parser.add_argument(
        "-s", "--show",
        action="store_true",
        help="Display each image before saving"
    )

    args = parser.parse_args()
    process_images(args.input, args.output, args.show)


if __name__ == "__main__":
    main()
