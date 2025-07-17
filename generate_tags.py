import os
import argparse
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


def generate_grid(input_folder, output_pdf, tag_size_mm, columns, rows):
    PAGE_WIDTH, PAGE_HEIGHT = A4
    c = canvas.Canvas(output_pdf, pagesize=A4)

    grid_width = columns * tag_size_mm * mm
    grid_height = rows * tag_size_mm * mm

    start_x = (PAGE_WIDTH - grid_width) / 2
    start_y = (PAGE_HEIGHT - grid_height) / 2

    for idx in range(rows * columns):
        row = rows - 1 - (idx // columns)
        col = idx % columns
        tag_file = os.path.join(input_folder, f"tag36_11_{idx:05d}.svg")

        if not os.path.exists(tag_file):
            print(f"⚠️ Missing: {tag_file}")
            continue

        drawing = svg2rlg(tag_file)
        scale = (tag_size_mm * mm) / max(drawing.width, drawing.height)
        drawing.width *= scale
        drawing.height *= scale
        for obj in drawing.contents:
            obj.scale(scale, scale)

        x = start_x + col * tag_size_mm * mm
        y = start_y + row * tag_size_mm * mm
        renderPDF.draw(drawing, c, x, y)

    c.save()
    print(f"✅ Saved grid PDF: {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an AprilTag PDF grid from SVGs")
    parser.add_argument("--input", required=True, help="Folder with SVG tag files")
    parser.add_argument("--output", required=True, help="Output PDF filename")
    parser.add_argument("--scale", type=float, required=True, help="Physical size of each tag in mm")
    parser.add_argument("--columns", type=int, default=8, help="Number of columns (default: 8)")
    parser.add_argument("--rows", type=int, default=6, help="Number of rows (default: 6)")

    args = parser.parse_args()

    generate_grid(
        input_folder=args.input,
        output_pdf=args.output,
        tag_size_mm=args.scale,
        columns=args.columns,
        rows=args.rows
    )
