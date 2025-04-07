import re
import os
import sys

def split_chapters(input_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all footnotes
    footnote_pattern = r'\[\^(\d+)\]:\s*(.*?)(?=\n\[\^|$)'
    footnotes = dict(re.findall(footnote_pattern, content, re.DOTALL))
    
    # Remove footnotes from the main content
    main_content = re.sub(r'\n\[\^\d+\]:.*?(?=\n\[\^|$)', '', content, flags=re.DOTALL)
    
    # Split content by H1 headings
    chapter_pattern = r'^#\s+(.*?)(?=\n#\s+|\Z)'
    chapters = re.findall(chapter_pattern, main_content, re.MULTILINE | re.DOTALL)
    chapter_titles = re.findall(r'^#\s+(.*?)$', main_content, re.MULTILINE)
    
    # Create output directory if it doesn't exist
    output_dir = "chapters"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each chapter
    for i, (title, content) in enumerate(zip(chapter_titles, chapters)):
        # Find footnote references in this chapter
        footnote_refs = set(re.findall(r'\[\^(\d+)\]', content))
        
        # Create chapter file
        sanitized_title = re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '_')
        filename = f"{output_dir}/ch{i:02d}.md"
        
        # Add chapter content
        chapter_content = f"# {title}\n\n{content[len(title):].strip()}\n\n"
        
        # Add referenced footnotes
        if footnote_refs:
            chapter_content += "\n## Footnotes\n\n"
            for ref in sorted(footnote_refs, key=int):
                if ref in footnotes:
                    chapter_content += f"[^{ref}]: {footnotes[ref]}\n"
        
        # Write chapter to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chapter_content)
        
        print(f"Created {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_chapters.py <input_file>")
        sys.exit(1)
    
    split_chapters(sys.argv[1])
    print("Chapter splitting complete!") 