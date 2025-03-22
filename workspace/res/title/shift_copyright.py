import struct
import sys

def modify_binary_file(filename, offset):
    with open(filename, "r+b") as f:
        # Skip first two uint16s (4 bytes)
        f.seek(4)

        while True:
            # Read the next 16-bit integer
            data = f.read(2)
            if not data:
                break  # End of file

            value = struct.unpack(">H", data)[0]  # Big-endian uint16

            if value != 0:
                new_value = (value + offset - 0xCC) & 0xFFFF  # Ensure it stays 16-bit
                f.seek(-2, 1)  # Move back 2 bytes to overwrite
                f.write(struct.pack(">H", new_value))  # Write modified value

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python modify_binary.py <filename> <offset>")
        sys.exit(1)

    filename = sys.argv[1]
    offset = int(sys.argv[2])
    
    modify_binary_file(filename, offset)
