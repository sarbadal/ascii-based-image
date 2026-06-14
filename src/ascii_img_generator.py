import pandas as pd
from PIL import Image
from typing import Callable

from gray_scale import AsciiImage, get_gray_scale_value


GrayScaleVal = Callable[[int|float, bool, bool], str]


def load_image_into_gscale(image_file: str) -> Image.Image:
    image: Image.Image = Image.open(image_file).convert('L')
    return image


def image_to_array(image: AsciiImage) -> list[list[int]]:
    width, height = image.image.size[0], image.image.size[1]
    w, h = width / image.columns, width / image.scale
    rows: int = int(height / h)

    if image.columns > width or rows > height:
        print("Image too small for specified cols!")
        exit(0)

    luminance = []
    for r in range(rows):
        y1: int = int(r * h)
        y2: int = height if r == rows - 1 else int((r + 1) * h)  # correct last tile

        luminance_row: list[int] = []
        for c in range(image.columns):
            x1: int = int(c * w)
            x2: int = width if c == image.columns - 1 else int((c + 1) * w)  # correct last tile

            avg = int(image.get_average_gscale_value(x1, y1, x2, y2))  # get average luminance
            luminance_row.append(avg)

        luminance.append(luminance_row)

    return luminance


def to_dataframe(image: AsciiImage) -> pd.DataFrame:
    img_array: list[list[int]] = image_to_array(image=image)
    columns = list(range(len(img_array[0])))
    return pd.DataFrame.from_records(img_array, columns=columns)


def convert_image_to_ascii(image: AsciiImage, gray_scale_value = get_gray_scale_value) -> list[str]:
    img_array: list[list[int]] = image_to_array(image=image)
    ascii_img: list[str] = []
    for r, row in enumerate(img_array):
        for col_luminance_val in row:
            ascii_img.append("")
            gsval: str = gray_scale_value(
                col_luminance_val,
                black_to_while=image.black_to_while,
                more_levels=image.more_levels
            )
            ascii_img[r] += gsval

    return ascii_img


if __name__ == "__main__":
    ""