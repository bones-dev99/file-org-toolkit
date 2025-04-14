#!/usr/bin/env python3

"""
Flatten Directory

Recursively gets all the files in the cwd's folders and pulls them into the root folder.
Automatically renames files to avoid overwrites.

Useful for gathering files in one place, especially to simply reorganize them.
"""

import os
import shutil

def collect_files(dir, base_dir):
	files = []
	for file in os.scandir(dir):
		if file.is_dir():
			files.extend(collect_files(file.path, base_dir))
		elif file.is_file() and not file.name.startswith('.') and os.path.dirname(file.path) != base_dir and not file == os.path.basename(__file__):
			files.append(file.name)
	return files

def rename_file(file):
	base, ext = os.path.splitext(file)
	counter = 1
	while os.path.exists(file):
		counter += 1
		file = f'{base}_{counter}{ext}'
	return file

def move_files(files, dir, file_ct):
	move_ct = 0
	for file in files:
		dst = os.path.join(dir, file)
		if os.path.exists(dst):
			dst = rename_file(dst)
		os.rename(file.path, dst)
		move_ct += 1
		print(f'Moved files {move_ct}/{file_ct}\r', end='')
	return move_ct

def main():
	try:
		this_dir = os.getcwd()
		move_ct = 0

		print(f'Scanning {this_dir}')
		files = collect_files(this_dir, this_dir)
		file_ct = len(files)
		if file_ct == 0:
			print('No files found.')
			return
			
		if file_ct > 20:
			user_input = input(f'This will move {file_ct} files. Are you sure? (y/n): ')
			if user_input.lower() != 'y':
				print('Aborted.')
				exit()

		move_ct = move_files(files, this_dir, file_ct)

		print()
		print('Finished!')
		
	except Exception as e:
		print(f'Encountered an error! {e}')

if __name__ == '__main__':
	main()
