"""
Simple python wrapper script to use ghoscript function to compress PDF files.

Compression levels:
    0: default - almost identical to /screen, 72 dpi images
    1: prepress - high quality, color preserving, 300 dpi imgs
    2: printer - high quality, 300 dpi images
    3: ebook - low quality, 150 dpi images
    4: screen - screen-view-only quality, 72 dpi images

"""

import argparse
import os.path
import shutil
import subprocess
import sys


def compress(input_file_path, output_file_path, power=0):

    quality = {
        0: "/default",
        1: "/prepress",
        2: "/printer",
        3: "/ebook",
        4: "/screen",
    }

    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file.", input_file_path)
        sys.exit(1)

    if power < 0 or power > len(quality) - 1:
        print("Error: invalid compression level, run pdfc -h for options.", power)
        sys.exit(1)

    #Check compression level to adjust compatibility level
    if power==4:
        compatibility=0.1
    else:
        compatibility=1.4

    if input_file_path.split('.')[-1].lower() != 'pdf':
        print(f"Error: input file is not a PDF.", input_file_path)
        sys.exit(1)

    gs = get_ghostscript_path()
    print("Compress PDF...")
    initial_size = os.path.getsize(input_file_path)

    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel={}".format(compatibility),
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(output_file_path),
            input_file_path,
        ]
    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.5f}MB".format(final_size / 1000000))
    print("Done.")


def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64"]
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(
        f"No GhostScript executable was found on path ({'/'.join(gs_names)})"
    )

if __name__ == "__main__":
   
    input_file_path = input("Enter the input PDF file path: ")
    output_file_path = input("Enter the output PDF file path: ")
    power = int(input("Enter the compression level (0 to 4): "))

    compress(input_file_path, output_file_path, power)
