# ascii-image

A Python package and CLI to convert an input image into ASCII art.

## Features

- Convert any supported image (JPG, PNG, etc.) to grayscale ASCII text.
- Export ASCII output to a text file.
- Export tile luminance values to CSV for analysis.
- Control width (`cols`) and output density (`scale`) from the CLI.

## Install

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

After install, the CLI command is available as `ascii-image`.

## CLI Usage

```bash
ascii-image -MF <input_image_path> -C <columns> -S <scale> -OF <output_txt_path> [-BW <true|false>]
```

### CLI Arguments

- `-MF`, `--imagefile` (required): Path to input image.
- `-C`, `--cols` (required): Number of columns in ASCII output.
- `-S`, `--scale` (required): Scale value used to calculate row height.
- `-OF`, `--outfile` (required): Path to output text file.
- `-BW`, `--blacktowhite` (optional): Invert grayscale mapping.
  Accepted truthy values include `true`, `1`, `yes`, `y`.

## Examples

### 1. Basic conversion

```bash
ascii-image \
  -MF images/imports/saturn.jpg \
  -C 80 \
  -S 35 \
  -OF images/exports/saturn.jpg.txt
```

### 2. Inverted grayscale mapping

```bash
ascii-image \
  -MF images/imports/saturn.jpg \
  -C 80 \
  -S 35 \
  -OF images/exports/saturn_invert.jpg.txt \
  -BW y
```

## Output Files

For `-OF images/exports/saturn.jpg.txt`, the CLI generates:

- `images/exports/saturn.jpg.txt` (ASCII text art)
- `images/exports/saturn.jpg.txt.csv` (numeric luminance matrix)

## Programmatic Usage

```python
from ascii_image.gray_scale import AsciiImage
from ascii_image.ascii_img_generator import AsciiImageConverter, load_image_into_gscale

image = load_image_into_gscale("images/imports/saturn.jpg")
ascii_img_info = AsciiImage(
    image=image,
    columns=80,
    scale=35,
    more_levels=True,
    black_to_white=True,
)

converter = AsciiImageConverter(
    image=ascii_img_info,
    gray_scale_value=ascii_img_info.convert_to_ascii,
)

ascii_lines = converter.convert_image_to_ascii()
converter.save_to_file(ascii_lines, "images/exports/saturn_programmatic.txt")
converter.to_dataframe().to_csv("images/exports/saturn_programmatic.txt.csv", index=False, header=False)
```

## Notes

- If `cols` is too large for the input image, conversion will stop with: `Image too small for specified cols!`.
- The CLI creates parent directories for output paths automatically.