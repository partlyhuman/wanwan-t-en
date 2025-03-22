#!/bin/bash
original_rom=wanwan.bin
emu_bin=../../../../Rupi.exe
emu_bios=../../../../bios.bin
emu_soundbios=../../../../soundbios.bin
emu_pcm=../../../../Sound/wanwan-samples/source/*.wav

pybin=python3
if ! command -v python3; then pybin=python; fi

# Prep work
if [[ ! -f clean_regions.csv ]]; then $pybin wanwan_strings.py regions "$original_rom" clean_strings.csv clean_regions.csv 0x6E000-0x70000; fi

file_strings=strings_tl_en_ph.csv
file_patches=patches.csv

echo "Downloading $file_strings ..."
SHEET_ID=16VfRlw3tT8lfHdTGLZBywaU1xhUOR0CMpO7sVkpgD18
SHEET_GID=2097974
curl -s --clobber -L -o "$file_strings" "https://docs.google.com/spreadsheets/d/$SHEET_ID/export?format=csv&id=$SHEET_ID&gid=$SHEET_GID"

echo "Downloading $file_patches ..."
SHEET_ID=16VfRlw3tT8lfHdTGLZBywaU1xhUOR0CMpO7sVkpgD18
SHEET_GID=301960430
curl -s --clobber -L -o "$file_patches" "https://docs.google.com/spreadsheets/d/$SHEET_ID/export?format=csv&id=$SHEET_ID&gid=$SHEET_GID"


# Prepatch rom with binary patches
if [[ -f wanwan_prepatch.bin ]]; then rm wanwan_prepatch.bin; fi

$pybin patchrom.py patch "$original_rom" patches.csv wanwan_prepatch.bin


# Patch rom with fonts and resources
echo
if [[ -f tmp.bin ]]; then rm tmp.bin; fi
if [[ -f wanwan_patched.bin ]]; then rm wanwan_patched.bin; fi

$pybin wanwan_font.py inject wanwan_prepatch.bin 0 font_00.png tmp.bin
$pybin wanwan_font.py inject tmp.bin 3 font_03.png wanwan_patched.bin

rm tmp.bin


# Inject strings
echo
if [[ -f wanwan_en.bin ]]; then rm wanwan_en.bin; fi

$pybin wanwan_strings.py inject wanwan_patched.bin strings_tl_en_ph.csv clean_regions.csv wanwan_en.bin


# Run emulator with ADPCM
#echo
#"$emu_bin" wanwan_en.bin "$emu_bios" "$emu_soundbios" | stdbuf -oL grep unmapped | $pybin wanwan_playpcm.py "$emu_pcm" >/dev/nul
open -a LoopyMSE wanwan_en.bin
