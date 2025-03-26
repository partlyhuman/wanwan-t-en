import struct
import sys

original_start = 0xCC

def modify_binary_file(filename, offset):
    with open(filename, "r+b") as f:
        # Skip first two uint16s (4 bytes)
        f.seek(4)

        while True:
            # Read the next 16-bit integer
            data = f.read(2)
            if not data:
                break  # End of file

            value = struct.unpack(">H", data)[0]
            if value != 0:
                new_value = (value - original_start + offset) & 0xFFFF
                f.seek(-2, 1)
                f.write(struct.pack(">H", new_value))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python %s <filename> <offset>" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    offset = int(sys.argv[2])
    
    modify_binary_file(filename, offset)
