#!env python3
import sys
import csv

def process_csv_files(play_order_file, strings_file):
    # Step 1: Create a dictionary from play_order.csv
    play_order_dict = {}
    with open(play_order_file, 'r') as play_order_csv:
        play_order_reader = csv.reader(play_order_csv)
        for line_number, row in enumerate(play_order_reader):
            key = row[0]
            try:
                key_dec = int(key, 16)
            except ValueError:
                print(f"Error: Unable to parse '{key}' as a hexadecimal number in line {line_number} of {play_order_file}")
                sys.exit(1)
                
            if key_dec not in play_order_dict:
                play_order_dict[key_dec] = line_number

    # Step 2: Process strings.csv
    with open(strings_file, 'r') as strings_csv:
        strings_reader = csv.reader(strings_csv)
        
        # Get the header
        header = next(strings_reader)

        # Find the index of the game_order column
        game_order_index = header.index('game_order') if 'game_order' in header else None

        # Print the modified header
        modified_header = header + ['game_order'] if game_order_index is not None else header
        print(','.join(modified_header))

        for row in strings_reader:
            # Parse the hexadecimal number in the first column
            origin_hex = row[0]
            try:
                origin_dec = int(origin_hex, 16)
            except ValueError:
                print(f"Error: Unable to parse '{origin_hex}' as a hexadecimal number in {strings_file}")
                sys.exit(1)

            # Check if origin_dec is in the dictionary
            game_order = str(play_order_dict.get(origin_dec, ''))

            # Update the row with the modified game_order column
            if game_order_index is not None:
                row[game_order_index] = game_order

            # Emit the modified row to stdout
            print(','.join(row))

if __name__ == "__main__":
    # Check if two arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python script.py play_order.csv strings.csv")
        sys.exit(1)

    play_order_file = sys.argv[1]
    strings_file = sys.argv[2]

    process_csv_files(play_order_file, strings_file)
