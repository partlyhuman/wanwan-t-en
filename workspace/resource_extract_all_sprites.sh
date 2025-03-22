#!/bin/bash

# Check if the input file and resources file are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 resources_file input_file"
    exit 1
fi

RESOURCES_FILE="$1"
INPUT_FILE="$2"

# Create the output directory if it doesn't exist
mkdir -p res

while IFS=',' read -r bitmap palette; do
    # Trim any whitespace
    bitmap=$(echo "$bitmap" | xargs)
    palette=$(echo "$palette" | xargs)

    echo "Processing bitmap $bitmap with palette $palette"

    # Extract the bitmap and palette resources
    python3 ../resource_tool/resource_tool.py extract-resource "$RESOURCES_FILE" "$bitmap" "res/$bitmap.bin"
    python3 ../resource_tool/resource_tool.py extract-resource "$RESOURCES_FILE" "$palette" "res/$palette.bin"

    # Decode the image
    python3 ../resource_tool/resource_tool.py decode-image -i true -c true "res/$bitmap.bin" "res/$palette.bin" "$bitmap.png"

done < "$INPUT_FILE"
