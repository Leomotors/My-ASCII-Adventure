import PIL
import math


def ImgToASCII(image: PIL.Image.Image, chars: str, target_width: int) -> dict:
    width, height = image.size
    target_height = int(target_width * height / width)
    resized_image = image.resize((target_width, target_height))
    print(target_height, target_width)
    resized_image.convert("L")
    pixels = resized_image.getdata()
    ascii_string = "".join(
        [chars[math.floor(pixel/(256/len(chars)))] for pixel in pixels])
    return {
        "data": [c for c in ascii_string],
        "dimension" : (target_height, target_width)
    }
