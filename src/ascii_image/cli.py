import argparse
from pathlib import Path

from pandas import DataFrame
from PIL import Image

from .ascii_img_generator import AsciiImageConverter, load_image_into_gscale
from .gray_scale import AsciiImage


def _parse_bool(value: str) -> bool:
	return str(value).lower() in ["true", "1", "yes", "y"]


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Convert an image into ASCII art")
	parser.add_argument("-C", "--cols", type=int, help="Number of columns", required=True)
	parser.add_argument("-S", "--scale", type=int, help="Scale", required=True)
	parser.add_argument(
		"-BW",
		"--blacktowhite",
		default=False,
		type=_parse_bool,
		help="Convert gradient black to white",
		required=False,
	)
	parser.add_argument(
		"-MF",
		"--imagefile",
		type=str,
		help="Path of the image",
		required=True,
	)
	parser.add_argument("-OF", "--outfile", type=str, help="Path of the txt output", required=True)
	return parser


def main() -> None:
	parser = build_parser()
	args: argparse.Namespace = parser.parse_args()
	cols: int = args.cols
	scale: int = args.scale
	black_to_white: bool = args.blacktowhite
	img_file: str = args.imagefile
	out_file: str = args.outfile
	Path(out_file).parent.mkdir(parents=True, exist_ok=True)

	image: Image.Image = load_image_into_gscale(image_file=img_file)
	ascii_img_info = AsciiImage(
		image=image,
		columns=cols,
		scale=scale,
		more_levels=True,
		black_to_white=black_to_white,
	)

	converter = AsciiImageConverter(
		image=ascii_img_info,
		gray_scale_value=ascii_img_info.convert_to_ascii,
	)
	ascii_img: list[str] = converter.convert_image_to_ascii()
	df: DataFrame = converter.to_dataframe()
	df.to_csv(f"{out_file}.csv", index=False, header=False)
	converter.save_to_file(ascii_img, out_file)


if __name__ == "__main__":
	main()