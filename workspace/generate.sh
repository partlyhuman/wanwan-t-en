# One-time
# python3 wanwan_font.py inject wanwan_prepatch.bin 0 font_00.png tmp.bin
# python3 wanwan_font.py inject tmp.bin 3 font_03.png wanwan_patched.bin
# rm tmp.bin
# python3 wanwan_strings.py regions wanwan_patched.bin strings_tl_en.csv clean_regions.csv 0x1FB950-0x200000

# Every time
if [[ -f wanwan_en.bin ]]; then rm wanwan_en.bin; fi
python3 wanwan_strings.py inject wanwan_patched.bin roger.csv clean_regions.csv wanwan_en.bin remapcc && loopymse wanwan_en.bin

# Padded version
#cp wanwan_patched.bin wanwan_patched_3m.bin
#pad wanwan_patched_3m.bin $((3 * 1024 * 1024))
#python3 wanwan_strings.py regions wanwan_patched_3m.bin strings_tl_en.csv clean_regions_3m.csv 0x1FB950-0x300000

# Pad every time
# python3 wanwan_strings.py inject wanwan_patched_3m.bin roger.csv clean_regions_3m.csv wanwan_en.bin remapcc && loopymse wanwan_en.bin

