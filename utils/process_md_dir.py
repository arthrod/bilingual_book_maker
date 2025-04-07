#!/usr/bin/env python3
"""
Simple script to process multiple markdown files in a directory using bbook_maker.
Uses the same arguments as bbook_maker but processes all markdown files in a directory.

Example usage:
python process_md_dir.py quarto --model openai --model_list o3-mini --prompt prompts/nl-translate.prompt.md --single_translate --language nl
"""

import os
import sys
import subprocess
from pathlib import Path

def find_markdown_files(directory_path):
    """Find all markdown files in a directory (recursively)"""
    markdown_files = []
    
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        sys.exit(1)
        
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            # Only process .md and .qmd files
            if file_ext in ['.md', '.qmd']:
                # Skip any files with an underscore in the name
                if "_" in file:
                    continue
                markdown_files.append(file_path)
    
    # Sort files for consistent processing
    markdown_files.sort()
    return markdown_files

def main():
    # Make sure we have at least one argument (the directory)
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <directory> [bbook_maker_args...]")
        sys.exit(1)
    
    # Get the directory and remaining arguments
    directory = sys.argv[1]
    bbook_args = ' '.join(sys.argv[2:])
    
    print(f"Directory: {directory}")
    print(f"Additional arguments: {bbook_args}")
    
    # Find markdown files
    md_files = find_markdown_files(directory)
    
    if not md_files:
        print(f"No markdown files found in {directory}")
        sys.exit(1)
    
    print(f"Found {len(md_files)} markdown files to process:")
    for file in md_files:
        print(f"  - {os.path.relpath(file, directory)}")
    
    # Ask for confirmation
    response = input("\nProcess these files? (y/n): ").strip().lower()
    if response != 'y':
        print("Operation cancelled")
        sys.exit(0)
    
    # Process each file
    successful_files = 0
    failed_files = 0
    failures = []
    
    for i, file_path in enumerate(md_files, 1):
        relative_path = os.path.relpath(file_path, directory)
        print(f"\n[{i}/{len(md_files)}] Processing: {relative_path}")
        
        # Construct the command
        cmd = f"pdm run bbook_maker --book_name {file_path} {bbook_args}"
        print(f"Running: {cmd}")
        
        try:
            # Run bbook_maker for this file
            process = subprocess.run(cmd, shell=True, text=True)
            
            # Print the output
            if process.stdout:
                print(process.stdout)
            if process.stderr:
                print(process.stderr)
            
            if process.returncode == 0:
                print(f"✓ Successfully processed {relative_path}")
                successful_files += 1
            else:
                print(f"✗ Failed to process {relative_path} (return code: {process.returncode})")
                failed_files += 1
                failures.append(file_path)
                
                # Ask if we should continue on error
                if failed_files == 1:  # Only ask on first failure
                    cont = input("Continue processing other files? (y/n): ").strip().lower()
                    if cont != 'y':
                        print("Stopping due to error.")
                        break
                    
        except Exception as e:
            print(f"✗ Error running command for {relative_path}: {str(e)}")
            failed_files += 1
            failures.append(file_path)
            
            # Ask if we should continue on error
            if failed_files == 1:  # Only ask on first failure
                cont = input("Continue processing other files? (y/n): ").strip().lower()
                if cont != 'y':
                    print("Stopping due to error.")
                    break
    
    # Print summary
    print("\n" + "="*50)
    print(f"Processing complete!")
    print(f"Total files: {len(md_files)}")
    print(f"Successfully processed: {successful_files}")
    print(f"Failed: {failed_files}")
    
    if failed_files > 0:
        print("\nFailed files:")
        for file_path in failures:
            print(f"  - {os.path.relpath(file_path, directory)}")
    
if __name__ == "__main__":
    main()