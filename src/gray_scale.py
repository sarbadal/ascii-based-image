from enum import StrEnum
from dataclasses import dataclass
from PIL import Image
import numpy as np


class GrayScaleStr(StrEnum):
    GRAY_SCALE_70_BLACK_TO_WHITE = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'.  '
    GRAY_SCALE_70_WHITE_TO_BLACK = '  .\'`^"\\,:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    GRAY_SCALE_10_BLACK_TO_WHITE = '@%#*+=-:. '
    GRAY_SCALE_10_WHITE_TO_BLACK = '  .:-=+*#%@'


@dataclass
class AsciiImage:
    image: Image.Image
    columns: int
    scale: int | float
    more_levels: bool = True
    black_to_while: bool = True

    def get_cropped_image(self, x1: int, y1: int, x2: int, y2: int) -> Image.Image:
        image: Image.Image = self.image.crop((x1, y1, x2, y2))
        return image

    def get_average_gscale_value(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """ Given PIL Image, return average value of grayscale value. """
        image: Image.Image = self.get_cropped_image(x1, y1, x2, y2)
        img: np.ndarray[int] = np.array(image)
        w, h = img.shape
        return np.average(img.reshape(w * h))


def get_gray_scale_value(value: int|float, black_to_while: bool = True, more_levels: bool = True) -> str:
    """ Read and return the ascii letter based on the value. """
    max_level_idx = int((value * 69) / 255)
    min_level_idx = int((value * 9) / 255)
    if black_to_while:
        if more_levels:
            return GrayScaleStr.GRAY_SCALE_70_BLACK_TO_WHITE[max_level_idx]
        return GrayScaleStr.GRAY_SCALE_10_BLACK_TO_WHITE[min_level_idx]
    
    if more_levels:
        return GrayScaleStr.GRAY_SCALE_70_WHITE_TO_BLACK[max_level_idx]
    return GrayScaleStr.GRAY_SCALE_10_WHITE_TO_BLACK[min_level_idx]


if __name__ == "__main__":
    print(get_gray_scale_value(20))
