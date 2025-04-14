#!/usr/bin/env python3

"""
Be Quiet

Renames any files with capital letters in the extension to have a lowercase extension.
Pass -h or read the README.md file to learn how to use this script.

If you're bothered by file extensions in capitals, this script will soothe your woes.
"""

import os
import sys

def collect_files(dir):
	files = []
	for file in os.scandir(dir):
		if file.is_dir():
			files.extend(collect_files(file.path))
		elif file.is_file() and not file.name.startswith('.') and not file.name == os.path.basename(__file__):
			files.append(file)
	return files

def rename_file(file, new_ext):
	base, _ = os.path.splitext(file)
	counter = 1
	while os.path.exists(file):
		counter += 1
		file = f'{base}_{counter}{new_ext}'
	return file

def rename_files(files, file_ct, invert):
	rename_ct = 0
	for file in files:
		base, ext = os.path.splitext(file)
		if not invert:
			new_ext = ext.lower()
		else:
			new_ext = ext.upper()
		if ext == new_ext:
			continue
		dst = f'{base}{new_ext}'
		if os.path.exists(dst):
			dst = rename_file(dst, new_ext)
		os.rename(file.path, dst)
		rename_ct += 1
		print(f'Renamed files {rename_ct}/{file_ct}\r', end='')
	return rename_ct

def main():
	try:		
		invert = False
		if len(sys.argv) > 1 and sys.argv[1].strip().lower() == "-i":
			invert = True
		
		this_dir = os.getcwd()
		print(f'Scanning {this_dir}')
		files = collect_files(this_dir)
		file_ct = len(files)
		if file_ct == 0:
			print('No files found.')
			return

		rename_ct = rename_files(files, file_ct, invert)

		print()
		print('Finished!')

	except Exception as e:
		print(f'Encountered an error! {e}')

if __name__ == '__main__':
	main()
