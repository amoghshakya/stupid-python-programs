from PIL import Image

# Define the ASCII characters from lightest to darkest
ASCII_CHARS = " .:-=+*#%@"


def scale_image(
    image: Image.Image, new_width: int = 80, char_ratio: float = 0.55
) -> Image.Image:
    """
    Resizes an image preserving the aspect ratio.
    Args:
        image (PIL.Image): The image to resize.
        new_width (int): The desired width in characters.
        char_ratio (float): The aspect ratio of characters (height/width).
    Returns:
        PIL.Image: The resized image.
    """
    width, height = image.size
    aspect_ratio = height / width

    # Adjust height according to character aspect ratio
    # The height is calculated to maintain the visual aspect ratio
    new_height = int(aspect_ratio * new_width * char_ratio)

    # This returns Image.Image
    return image.resize((new_width, new_height))  # pyright: ignore[reportUnknownMemberType]


def to_grayscale(image: Image.Image) -> Image.Image:
    """Convert an image to grayscale."""
    return image.convert("L")


def map_pixels_to_ascii(image: Image.Image, invert: bool = False) -> str:
    """
    Maps each pixel to an ASCII character based on its brightness.
    Args:
        image (PIL.Image): The grayscale image.
        invert (bool): Whether to invert the ASCII characters.
    Returns:
        str: The resulting ASCII string.
    """

    # pixels will be a sequence of pixel values (0-255)
    pixels = image.getdata()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    chars = ASCII_CHARS[::-1] if invert else ASCII_CHARS
    scale = len(chars) - 1

    ascii_str = "".join(
        chars[pixel * scale // 255] for pixel in pixels if isinstance(pixel, int)
    )
    return ascii_str


def convert_image_to_ascii(
    image_path: str,
    new_width: int = 80,
    invert: bool = False,
    char_ratio: float = 0.55,
) -> str:
    """
    Convert an image to ASCII art.
    Args:
        image_path (str): Path to the input image file.
        new_width (int): The desired width in characters.
        invert (bool): Whether to invert the ASCII characters.
        char_ratio (float): The aspect ratio of characters (height/width).
    Returns:
        str: The resulting ASCII art string.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}. {e}")
        return ""

    image = scale_image(image, new_width, char_ratio)
    image = to_grayscale(image)

    ascii_str = map_pixels_to_ascii(image, invert=invert)

    img_width = image.width
    ascii_img = "\n".join(
        ascii_str[i : i + img_width] for i in range(0, len(ascii_str), img_width)
    )

    return ascii_img
