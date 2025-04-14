#!/usr/bin/env python3

"""
Naming Scheme

Edits file names to conform to a specific casing and use a specific kind of spacing.
Pass -h or read the README.md file to learn how to use this script.

Useful if you want all your file names to look the same.
"""

import os
import argparse

def get_files(dir):
	print('Getting files.')
	return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) 
		and not f.startswith('.') and not f == os.path.basename(__file__)]

def is_space(char):
	return char in ['_', '-', ' ']

def split_into_words(string):
	words = []
	current = []
	for char in string:
		if current and char.isupper():
			prev_char = current[-1] if current else ''
			if not prev_char.isupper():
				words.append(''.join(current))
				current = []
			current.append(char)
		elif current and is_space(char):
			words.append(''.join(current))
			current = []
		else:
			current.append(char)
	if current:
		words.append(''.join(current))
	return words

def lower_case(words):
	return [word.lower() for word in words]

def upper_case(words):
	return [word.upper() for word in words]

def capitalize_each_word(words):
	return [
		word if len(word) > 1 and word[0].isupper() and word[1].isupper()
		else word[0].upper() + word[1:]
		for word in words
	]

def camel_case(words):
	return [words[0].lower()] + capitalize_each_word(words[1:])

def pascal_case(words):
	return capitalize_each_word(words)

def apply_casing(words, case):
	if (case == 'lowercase'):
		return lower_case(words)
	elif (case == 'UPPERCASE'):
		return upper_case(words)
	elif (case == 'camelCase'):
		return camel_case(words)
	elif (case == 'PascalCase'):
		return pascal_case(words)
	else:
		return words

def get_new_string(string, case, space_char):
	string = string.replace(' - ', '-')
	words = split_into_words(string)
	words = apply_casing(words, case)
	return space_char.join(words)

def rename_file(file, space_char):
	if not space_char or space_char == '':
		space_char = ' '
	base, ext = os.path.splitext(file)
	counter = 1
	while os.path.exists(file):
		counter += 1
		file = f'{base}{space_char}{counter}{ext}'
	return file

def apply_scheme(case, space_char, dry_run):
	this_dir = os.getcwd()
	files = get_files(this_dir)
	file_ct = len(files)
	rename_ct = 0

	if file_ct == 0:
		print('No files to rename.')
		return
		
	print('Applying naming scheme.')

	for file in files:
		base, ext = os.path.splitext(file)
		dst = get_new_string(base, case, space_char) + ext

		if file == dst:
			continue
		if os.path.exists(dst):
			dst = rename_file(dst, space_char)

		rename_ct += 1
		if not dry_run:
			os.rename(file, dst)
			print(f'Renamed files {rename_ct}/{file_ct}\r', end='')
		else:
			print(f'{file} -> {dst}')

	if dry_run:
		print('No files renamed.')
	else:
		print()
		print('Finished!')

def get_args():
	parser = argparse.ArgumentParser(description='a script that renames files with a specific styling.')
	parser.add_argument('-s', '--space', type=str, required=True, default='_', help='determines what character is used as a spacer. defaults to underscore. can also be no character at all.')
	parser.add_argument('-c', '--case', type=str, choices=['lowercase', 'UPPERCASE', 'camelCase', 'PascalCase'], help='determines the style.')
	parser.add_argument('-d', '--dry', action='store_true', help='a switch. if included, will not actually rename any files.')
	return parser.parse_args()

def main():
	try:
		args = get_args()
		apply_scheme(args.case, args.space, args.dry)
	except Exception as e:
		print(f'Encountered an error! {e}')

if __name__ == '__main__':
	main()
