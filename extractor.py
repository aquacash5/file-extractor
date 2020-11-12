#! /usr/bin/python3

from argparse import ArgumentParser
from pathlib import Path
import shutil


def abs_path(p):
    return Path(p).absolute()


parser = ArgumentParser(
    description='Extracts files from one directory and sorts them by file extension in another.')
parser.add_argument('src',
                    type=abs_path,
                    help='Directory to search for files')
parser.add_argument('dst',
                    type=abs_path,
                    help='Directory to put the matching files')
parser.add_argument('ext',
                    help='File Extetion to find')
args = parser.parse_args()

args.dst = args.dst / args.ext
args.dst.mkdir(parents=True, exist_ok=True)

for extracted in args.src.rglob(f'*.{args.ext}'):
    if '__MACOSX' in str(extracted):
        continue
    final_path = args.dst / extracted.name
    if final_path.exists():
        count = 1
        final_path = args.dst / f'{extracted.stem}_{count}.{args.ext}'
        while final_path.exists():
            count += 1
            final_path = args.dst / f'{extracted.stem}_{count}.{args.ext}'
    shutil.copy(extracted, final_path)
