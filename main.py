import argparse
from PIL import Image

from gray_scale import AsciiImage
from ascii_img_generator import load_image_into_gscale, convert_image_to_ascii


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--cols', type=int, help='no of columns', required=True)
    parser.add_argument('-S', '--scale', type=int, help='Scale', default=True, required=True)
    parser.add_argument(
        '-BW', 
        '--blacktowhite', 
        default=False, 
        type=lambda x: (str(x).lower() in ['true', '1', 'yes', 'y']), 
        help='flag image gradient', 
        required=False
    )
    parser.add_argument('-MF', '--imagefile', type=str, help='path of the image', required=True)
    parser.add_argument('-OF', '--outfile', type=str, help='path of the output', required=True)

    args: argparse.Namespace = parser.parse_args()
    cols: int = args.cols
    scale: int = args.scale
    black_to_while: bool = args.blacktowhite
    img_file: str = args.imagefile
    out_file: str = args.outfile
    
    image: Image.Image = load_image_into_gscale(image_file=img_file)
    ascii_img = AsciiImage(
        image=image,
        columns=cols,
        scale=scale,
        more_levels=True,
        black_to_while=black_to_while
    )

    str_image: list[str] = convert_image_to_ascii(image=ascii_img)

    with open(out_file, mode='w') as f:
        for row in str_image:
            f.write(f'{row}\n')


if __name__ == "__main__":
    # Sample command ...
    """
    python with_ascii/main.py \
        -MF "with_ascii/images/imports/statue-of-liberty-02.png" \
        -C 80 \
        -S 35 \
        -OF "with_ascii/images/imports/statue-of-liberty-02-bw.txt" \
        -BW y
    """
    main()
