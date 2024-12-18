from PIL import Image
from typing import Callable

from gray_scale import AsciiImage, get_gray_scale_value


type GrayScaleVal = Callable[[float, bool, bool], str]


def load_image_into_gscale(image_file: str) -> Image.Image:
    image: Image.Image = Image.open(image_file).convert('L')
    return image


def convert_image_to_ascii(image: AsciiImage, gray_scale_value: GrayScaleVal = get_gray_scale_value) -> list[str]:
    W, H = image.image.size[0], image.image.size[1]
    print("input image dims: %d x %d" % (W, H))

    w, h= W/image.columns, W/image.scale
    rows: int = int(H/h)

    print("cols: %d, rows: %d" % (image.columns, rows))
    print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if image.columns > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    ascii_img: list[str] = []
    for r in range(rows):
        y1: int = int(r * h)
        y2: int = H if r == rows - 1 else int((r + 1) * h)  # correct last tile
        
        ascii_img.append("")

        for c in range(image.columns):
            x1: int = int(c * w)
            x2: int = W if c == image.columns - 1 else int((c + 1) * w)  # correct last tile

            avg = int(image.get_average_gscale_value(x1, y1, x2, y2))  # get average luminance

            gsval: str = gray_scale_value(
                avg, 
                black_to_while=image.black_to_while, 
                more_levels=image.more_levels
            )
            ascii_img[r] += gsval
    
    return ascii_img


if __name__ == "__main__":
    ""