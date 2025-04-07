from promptdown import StructuredPrompt
import pprint

def debug_promptdown_structure(file_path):
    """Debug helper to understand the structure of a PromptDown parsed object"""
    print(f"Loading PromptDown file: {file_path}")
    structured_prompt = StructuredPrompt.from_promptdown_file(file_path)
    
    print("\n=== Object Type ===")
    print(type(structured_prompt))
    
    print("\n=== Available Attributes ===")
    attributes = [attr for attr in dir(structured_prompt) if not attr.startswith('_')]
    pprint.pprint(attributes)
    
    print("\n=== String Representation ===")
    print(str(structured_prompt))
    
    print("\n=== Object Dictionary ===")
    if hasattr(structured_prompt, '__dict__'):
        pprint.pprint(vars(structured_prompt))
    elif hasattr(structured_prompt, 'to_dict'):
        pprint.pprint(structured_prompt.to_dict())
    else:
        print("No dictionary representation available")
    
    return structured_prompt

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        debug_promptdown_structure(sys.argv[1])
    else:
        print("Please provide a path to a PromptDown file.") 