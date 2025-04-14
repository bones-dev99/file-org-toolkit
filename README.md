# File Organization Toolkit

A collection of lightweight command-line tools used for organizing and managing files in bulk. Built for ease of use, consistency, and automation.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
This means you are free to use, study, modify, and share this software, but if you deploy a modified version publicly (including over a network), you are required to share your changes as well (AKA, make it Open Source).

See the [LICENSE](./LICENSE) file for full details. Or don't. You're probably not a lawyer.

I chose AGPL to ensure the project remains free and open, and that improvements made by others are shared with the community.

## Features
- Apply a consistent naming scheme to files in bulk.
- Bulk rename files with serialized names and automatic enumeration.
- Flatten nested directories safely.
- Group large amounts of files into structured subfolders.
- Format the casing on file extensions recursively.

## Requirements

- Python 3.6 or later
- No third-party dependencies - pure Python!

## How to Use

### be-quiet.py

This script will rename all files in the **current working directory (cwd)** and its subfolders to use a consistent casing for their extensions. By default, it will make the extension entirely lowercase, hence the name. If you're more of an uppercase person, you can pass -i or -I to invert the script's function and make the extension uppercase. Remember: Upper case is for the upper class.

### flatten-dir.py

This script will flatten the **current working directory (cwd)** by pulling all files from subfolders into the root folder. Don't worry, the script won't overwrite files with the same name, and will instead automatically rename them. Note: this script does *not* remove the empty directories it leaves behind.

### org-large-dirs.py

This script takes files in the **current working directory (cwd)** and places them into subfolders. Each subfolder will contain a maximum of 1000 files by default, but you can pass an argument to specify the limit (ie, `python3 org-large-dirs.py 500`). Subfolders will inherit the name of the parent folder. If you keep the parent folder's name the same, the script can be ran multiple times to continue organizing new files consistently.

### naming-scheme.py

This script will apply a style to the names of all files in the **current working directory (cwd)**. In specific, it will modify the spaces and the casing on each word. You must specify a space character with -s, which will replace or be added in between all words. You can optionally specify a case, which is either camelCase, PascalCase, UPPERCASE, or lowercase. All of these affect the capitalization of each word. If you're not sure about committing, you can pass the -d switch, which doesn't actually rename the files, and will print what the results would look like to the console.

### serialize-files.py

This script will rename all files in the **current working directory (cwd)** with a passed in base name, adding an incrementing number afterwards. 

Required:
- -b: Base Name, what the new file names will start with.

Optional
- -e: End Name, what the new file names will end with, even after the number.
- -s: Starting Number (default is 1)
- -p: Padding, ie, 3 -> 001, 002, 003, et ceteral.
- -d: Dry Run, preview the results without actually changing anything.

Note: The script does not gather the files in any particular order, including alphabetical. It's only goal is to make sure the file names follow the pattern.
