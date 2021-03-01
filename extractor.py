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
                    help='directory to search for files')
parser.add_argument('dst',
                    type=abs_path,
                    help='directory to put the matching files')
parser.add_argument('ext',
                    help='file Extetion to find')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='show individual actions')
args = parser.parse_args()

args.dst = args.dst / args.ext
args.dst.mkdir(parents=True, exist_ok=True)

for extracted in args.src.rglob(f'*.{args.ext}'):
    if '__MACOSX' in str(extracted):
        continue
    if extracted.is_dir():
        continue
    final_path = args.dst / extracted.name
    if final_path.exists():
        count = 1
        final_path = args.dst / f'{extracted.stem}_{count}.{args.ext}'
        while final_path.exists():
            count += 1
            final_path = args.dst / f'{extracted.stem}_{count}.{args.ext}'
    print(f'Copy {extracted} to {final_path}')
    shutil.copy(extracted, final_path)
