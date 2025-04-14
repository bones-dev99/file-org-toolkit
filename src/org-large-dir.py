#!/usr/bin/env python3

"""
Organize Large Directory

Takes the files in the cwd and moves them into subfolders, divided by the value of file_limit.
Can pass an argument to specify the file_limit.

Useful for breaking up large directories into smaller, more manageable ones.
"""

import os
import sys
import shutil

def get_files(dir):
	print('Getting files.')
	return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) 
		and not f.startswith('.') and not f == os.path.basename(__file__)]

def get_last_folder_number(dir, subdir):
	folders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f)) and f.startswith(subdir)]
	numbers = [int(f[len(subdir) + 1:]) for f in folders if f [len(subdir) + 1:].isdigit()]
	return max(numbers, default=1)

def increment_folder_number(dir, subdir, folder_number):
	folder_number += 1
	folder = os.path.join(dir, f'{subdir}_{folder_number}')
	os.makedirs(folder, exist_ok=True)
	return folder, folder_number

def rename_file(file):
	base, ext = os.path.splitext(file)
	counter = 1
	while os.path.exists(file):
		counter += 1
		file = f'{base}_{counter}{ext}'
	return file

def main():
	try:
		file_limit = 1000
		if len(sys.argv) > 1:
			if sys.argv[1].isdigit():
				file_limit = int(sys.argv[1])
				if file_limit == 0:
					print('Argument must be greater than zero.')
					return
			else:
				print('Argument must be a numeric value.')
				return

		this_dir = os.getcwd()
		files = get_files(this_dir)
		file_ct = len(files)
		if file_ct == 0:
			print('No files to organize.')
			return
		
		subdir = os.path.basename(this_dir)

		folder_number = get_last_folder_number(this_dir, subdir)
		folder = os.path.join(this_dir, f'{subdir}_{folder_number}')
		os.makedirs(folder, exist_ok=True)
		existing_files = len(os.listdir(folder))
		
		if (existing_files > file_limit):
			folder, folder_number = increment_folder_number(this_dir, subdir, folder_number)
		file_index = 1
			
		print('Organizing folder.')
		
		for file in files:
			if existing_files >= file_limit:
				folder, folder_number = increment_folder_number(this_dir, subdir, folder_number)
				existing_files = 0
			src = os.path.join(this_dir, file)
			dst = os.path.join(folder, file)
			if os.path.exists(dst):
				dst = rename_file(dst)
			os.rename(src, dst)
			print(f'Moved files {file_index}/{file_ct}\r', end='')
			existing_files += 1
			file_index += 1
		print()
		print('Finished!')
	except Exception as e:
		print(f'Encountered an error! {e}')

if __name__ == '__main__':
	main()
