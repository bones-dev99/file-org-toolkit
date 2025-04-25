#!/usr/bin/env python3

"""
Serialize Files

Renames all files to a given base name, and enumerates each name with padded numbers.
Pass -h or read the README.md file to learn how to use this script.

Useful for consistent, sequential file names.
"""

import os
import re
import argparse

def get_files(dir, extension_filter):
	print('Getting files.')
	return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) 
		and not f.startswith('.') and not f == os.path.basename(__file__) 
		and (not extension_filter or os.path.splitext(f)[1].lower() in 
		extension_filter)]

def get_correct_files(files, start, prefix, padding, suffix):
	already_named = []
	bases = []
	startl = len(prefix)
	endl = len(suffix)
	max_denominator = len(files) + (start - 1)

	for index, file in enumerate(files):
		base, _ = os.path.splitext(file)
		if base in bases:
			continue
		if base.startswith(prefix) and base.endswith(suffix):
			middle = base[startl:-endl] if suffix else base[startl:]
			if middle.isdigit() and len(middle) == padding and int(middle) <= max_denominator and base not in already_named:
				already_named.append(file)
				bases.append(base)
	return already_named, bases

def serialize_files(prefix, suffix, start, padding, extension_filter, dry_run):
	this_dir = os.getcwd()
	files = get_files(this_dir, extension_filter)
	file_ct = len(files)
	rename_ct = 0

	if file_ct == 0:
		print('No files to serialize.')
		return

	if padding == -1:
		padding = len(str(file_ct)) if files else 0

	already_named, bases = get_correct_files(files, start, prefix, padding, suffix)

	files = [file for file in files if file not in already_named]
	file_ct = len(files)
	if file_ct < 1:
		print('All files already serialized.')
		return

	denominator = start
	
	print('Renaming files.')

	for file in files:
		base, ext = os.path.splitext(file)
		dbase = f'{prefix}{str(denominator).zfill(padding)}{suffix}'

		while dbase in bases:
			denominator += 1
			dbase = f'{prefix}{str(denominator).zfill(padding)}{suffix}'

		dst = f'{dbase}{ext}'

		denominator += 1
		rename_ct += 1

		if not dry_run:
			os.rename(file, dst)
			print(f'Renamed files {rename_ct}/{file_ct}\r', end='')
		else:
			print(f'{file} -> {dst}')

	if  dry_run:
		print('No files renamed.')
	else:
		print()
		print(f'Finished!')

def get_args():
	parser = argparse.ArgumentParser(description='a script that renames files an adds a number in series.')
	parser.add_argument('-b', '--base', type=str, required=True, help='the first part of the name for all the renamed files. will be placed before the number.')
	parser.add_argument('-e', '--end', type=str, default='', help='the last part of the name for all the renamed files. will be placed after the number.')
	parser.add_argument('-s', '--start', type=int, default=1, help='the number of the first file that will be renamed. defaults to 1.')
	parser.add_argument('-p', '--padding', type=int, default=-1, help='the minimum number of digits in each number.')
	parser.add_argument('-f', '--filter', type=str, default=None, help='a comma-separated list of extensions to include (include periods). all other extensions will be ignored.')
	parser.add_argument('-d', '--dry', action='store_true', help='a switch. if included, will not actually rename any files.')
	return parser.parse_args()

def main():
	try:
		args = get_args()
		serialize_files(args.base, args.end, args.start, args.padding, args.filter, args.dry)
	except Exception as e:
		print(f'Encountered an error! {e}')

if __name__ == '__main__':
	main()
