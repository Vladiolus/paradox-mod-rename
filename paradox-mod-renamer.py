import os
import re

def extract_info(lines):
    mod_name = None
    sub_path = None
    for line in lines:
        if line.startswith('name='):
            match = re.search(r'name="(.+)"', line)
            if match:
                mod_name = match.group(1)
        if line.startswith('path='):
            match = re.search(r'path="(.+)"', line)
            if match:
                path = match.group(1)
                norm_path = os.path.normpath(path)
                sub_path = os.path.basename(norm_path)

    return mod_name, sub_path

def rename_mods(root_dir):
    # Iterate over all files in the mod directory
    for filename in os.listdir(root_dir):
        if filename.endswith('.mod'):
            file_path = os.path.join(root_dir, filename)

            # Read the .mod file
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Extract mod name and path
            mod_name, sub_path = extract_info(lines)

            if not (mod_name and sub_path):
                print(f'Failed to read info from "{filename}"')
                return
        
            # Normalize mod name to create a valid directory/file name
            new_name = re.sub(r'[\*\|\\\:\"<>\?\/]', "", mod_name)

            # Define new paths
            new_file_path = os.path.join(root_dir, new_name + '.mod')
            sub_dir = os.path.join(root_dir, sub_path)
            new_sub_dir = os.path.join(root_dir, new_name)

            # Update path in the .mod file
            new_path_line = f'path="mod/{new_name}/"\n'
            updated_lines = [new_path_line if line.startswith('path=') else line for line in lines]

            # Write updated .mod file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)

            # Rename .mod file
            os.rename(file_path, new_file_path)

            # Rename sub-directory
            if os.path.exists(sub_dir):
                os.rename(sub_dir, new_sub_dir)

            print(f'{filename}  -->  {new_name}')

print("""
~~~~~~~~~~~~~
INITIALIZATION
~~~~~~~~~~~~~

It is a simple mod renamer for Paradox games.
This program will rename all .mod files and corresponding subdirectories inside the specified directory.
""")

# Get mod directory from user input
root_dir = input('Enter the mod directory path: \n')

print("""
Launching...
""")

# Run the rename function
rename_mods(root_dir)

print("""
Completed.
""")

input('Press Enter to exit...')
