import argparse

from asciipy import convert_image_to_ascii


def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    _ = parser.add_argument(
        "image_path", type=str, help="Path to the input image file."
    )
    _ = parser.add_argument(
        "--width", type=int, default=80, help="Width of ASCII output."
    )
    _ = parser.add_argument("--ratio", type=float, help="Character aspect ratio")
    _ = parser.add_argument("--invert", action="store_true", help="Invert ASCII chars.")

    args = parser.parse_args()

    ascii_art = convert_image_to_ascii(
        args.image_path,
        new_width=args.width,
        invert=args.invert,
        char_ratio=args.ratio if args.ratio else 0.55,
    )
    print(ascii_art)


if __name__ == "__main__":
    main()
