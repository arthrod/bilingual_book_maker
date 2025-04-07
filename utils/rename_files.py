#!/usr/bin/env python3
import os
import sys

def rename_files_in_directory(directory):
    # Get a list of entries in the directory.
    for filename in os.listdir(directory):
        # Create full file path.
        old_path = os.path.join(directory, filename)
        # Skip directories.
        if os.path.isdir(old_path):
            continue
        # Check if filename contains an underscore.
        if "_" not in filename:
            continue
        # Split filename into basename and extension.
        name_without_ext, ext = os.path.splitext(filename)
        # Take the part before the first underscore.
        new_base = name_without_ext.split('_', 1)[0]
        new_filename = new_base + ext
        new_path = os.path.join(directory, new_filename)
        # Check for collisions.
        if os.path.exists(new_path):
            print(f"Skipping {filename} as {new_filename} already exists.")
            continue
        print(f"Renaming {filename} -> {new_filename}")
        os.rename(old_path, new_path)

if __name__ == "__main__":
    # Use directory provided as a command-line argument, or default to current directory.
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    
    rename_files_in_directory(directory)