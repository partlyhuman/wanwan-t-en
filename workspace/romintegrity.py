#!/usr/bin/env python3

import struct, sys, os

ROM_BASE = 0x0E000000

# check_start, check_end, check_expect
def read_header(data):
	return struct.unpack(">LLL", data[0:12])

def checksum(data):
	check_start, check_end, _ = read_header(data)
	check_start -= ROM_BASE
	check_end -= ROM_BASE
	if check_start < 0 or check_start >= len(data):
		raise ValueError("Invalid start address")
	if check_end < 0 or check_end >= len(data):
		raise ValueError("Invalid end address")
	if check_end < check_start or (check_start&1) != 0 or (check_end&1) != 0:
		raise ValueError("Invalid range")
	#print("Expected checksum: {0:08X}".format(check_expect))
	s = 0
	for i in range(check_start, check_end+1, 2):
		s = (s+struct.unpack(">H", data[i:i+2])[0])&0xFFFFFFFF
	return s

def check(data):
	_, _, check_expect = read_header(data)
	try:
		return check_expect == checksum(data)
	except:
		return false

if __name__ == "__main__":
	if len(sys.argv) == 3 and (sys.argv[1] == "-u" or sys.argv[1] == "--update"):
		if os.path.exists(sys.argv[2]):
			with open(sys.argv[2], "r+b") as f:
				data = f.read()
				sum = checksum(data)
				f.seek(8)
				f.write(struct.pack(">L", sum))
				print("Updated checksum to %08X" % sum)
				# print("Verifying...")
				# if not check(data):
				#   print("FAIL")
		exit()


	if len(sys.argv) == 2:
		if os.path.exists(sys.argv[1]):
			with open(sys.argv[1], "rb") as f:
				data = f.read()
				print("Checking", f.name)
			if check(data):
				print("ROM is valid!")
			else:
				print("ROM is INVALID!")
		else:
			print("File not found")
	else:
		print(sys.argv[0], "[-u/--update] <rom file>")
		print("Verifies the checksum, unless '--update' is used, then writes the correct checksum")
	print()
	