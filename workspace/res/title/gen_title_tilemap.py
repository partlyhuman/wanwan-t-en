import struct, sys

def gen_title_tilemap(filename):
    with open(filename, "wb") as f:
        num_rows = 10
        tiles_per_row = 28
        num_padding = 32 - tiles_per_row
        counter = 0

        for row in range(num_rows):
            for _ in range(tiles_per_row):
                long = counter
                if row < 3:
                    long += 0x1000
                f.write(struct.pack(">H", long))
                counter += 1
            for _ in range(num_padding):
                f.write(struct.pack(">H", 0))

if __name__ == "__main__":
    gen_title_tilemap(sys.argv[1])
