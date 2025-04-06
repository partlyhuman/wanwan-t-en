#!/usr/bin/env python3
import struct
import sys

def hex_to_15bit_rgb(hex_color):
    """Convert #rrggbb hex to 15-bit RGB format: 0RRRRRGGGGGBBBBB"""
    r = int(hex_color[1:3], 16) >> 3
    g = int(hex_color[3:5], 16) >> 3
    b = int(hex_color[5:7], 16) >> 3
    value = (r << 10) | (g << 5) | b
    return value

def convert_palette_file(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    colors = [hex_to_15bit_rgb(line) for line in lines]

    with open(output_path, 'wb') as out:
        out.write(struct.pack('>H', len(colors)))
        for color in colors:
            out.write(struct.pack('>H', color))

    print(f"Wrote {len(colors)} colors to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_palette.txt> <output_palette.bin>")
        sys.exit(1)

    convert_palette_file(sys.argv[1], sys.argv[2])
