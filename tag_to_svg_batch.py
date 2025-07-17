import os
import sys
import argparse
import subprocess

def batch_convert(input_folder, output_folder, tag_family, start_id, end_id, scale):
    os.makedirs(output_folder, exist_ok=True)

    for tag_id in range(start_id, end_id + 1):
        input_file = os.path.join(input_folder, f"{tag_family}_{tag_id:05d}.png")
        output_file = os.path.join(output_folder, f"{tag_family}_{tag_id:05d}.svg")

        cmd = [
            sys.executable, "tag_to_svg.py",
            input_file,
            output_file,
            f"--size={scale}"
        ]

        print(f"🔄 Converting {input_file} → {output_file}")
        subprocess.run(cmd, check=True)

    print(f"\n✅ Converted tags {start_id}–{end_id} to SVGs at {scale} in {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch convert AprilTag PNGs to SVGs using tag_to_svg.py")
    parser.add_argument("--input", required=True, help="Folder containing PNG tags")
    parser.add_argument("--output", required=True, help="Folder to store SVG outputs")
    parser.add_argument("--start", type=int, required=True, help="Start tag ID (inclusive)")
    parser.add_argument("--end", type=int, required=True, help="End tag ID (inclusive)")
    parser.add_argument("--scale", required=True, help="Tag size, e.g., 25mm")
    parser.add_argument("--family", default="tag36_11", help="Tag family prefix (default: tag36_11)")

    args = parser.parse_args()

    batch_convert(
        input_folder=args.input,
        output_folder=args.output,
        tag_family=args.family,
        start_id=args.start,
        end_id=args.end,
        scale=args.scale
    )
