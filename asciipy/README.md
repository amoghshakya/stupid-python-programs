# asciipy (asciify)

A simple script to convert images to ASCII art.

## Installation

1. Clone this repository

   ```sh
   git clone https://github.com/amoghshakya/asciipy.git
   cd asciipy
   ```

2. Install dependencies

   Using [uv](https://github.com/astral-sh/uv):

   ```sh
   uv sync
   ```

   Or with `pip`:

   ```sh
   pip install .
   ```

## Usage

```text
usage: main.py [-h] [--width WIDTH] [--ratio RATIO] [--invert] image_path

Convert an image to ASCII art.

positional arguments:
  image_path     Path to the input image file.

options:
  -h, --help     show this help message and exit
  --width WIDTH  Width of ASCII output.
  --ratio RATIO  Character aspect ratio
  --invert       Invert ASCII chars.
```

```sh
$ python main.py image.jpeg --width 60 --invert
# or with uv
$ uv run main.py image.jpeg --width 60 --invert
```
