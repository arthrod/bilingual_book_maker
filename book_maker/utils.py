import tiktoken
import datetime
import json
import os
from pathlib import Path

# Borrowed from : https://github.com/openai/whisper
LANGUAGES = {
    "en": "english",
    "zh-hans": "simplified chinese",
    "zh": "simplified chinese",
    "zh-hant": "traditional chinese",
    "zh-yue": "cantonese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "français",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "nederlands",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
}

# language code lookup by name, with a few language aliases
TO_LANGUAGE_CODE = {
    **{language: code for code, language in LANGUAGES.items()},
    "burmese": "my",
    "valencian": "ca",
    "flemish": "nl",
    "haitian": "ht",
    "letzeburgesch": "lb",
    "pushto": "ps",
    "panjabi": "pa",
    "moldavian": "ro",
    "moldovan": "ro",
    "sinhalese": "si",
    "castilian": "es",
}


def prompt_config_to_kwargs(prompt_config):
    prompt_config = prompt_config or {}
    return dict(
        prompt_template=prompt_config.get("user", None),
        prompt_sys_msg=prompt_config.get("system", None),
        system_role=prompt_config.get("system_role", None),
    )


# ref: https://platform.openai.com/docs/guides/chat/introduction
def num_tokens_from_text(text, model="gpt-3.5-turbo-0301"):
    messages = (
        {
            "role": "user",
            "content": text,
        },
    )

    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )

def count_tokens_with_tiktoken(messages, model="gpt-3.5-turbo"):
    """
    Returns the number of tokens used by a list of messages using tiktoken.
    If each message is a dictionary (with keys like "role" and "content"), it follows
    the chat message token counting rules; if it's a string, it just counts the tokens in the string.
    
    Args:
        messages (list): A list where each element is either a dictionary with keys such as
                         "role", "content", (and optionally "name") or a plain string.
        model (str): The model name to use for tokenization.
    
    Returns:
        int: The total number of tokens.
    """
    import tiktoken

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fall back to a base encoding if the model-specific encoding is not found
        encoding = tiktoken.get_encoding("cl100k_base")
    
    total_tokens = 0
    for message in messages:
        if isinstance(message, dict):
            # For chat messages, include the formatting tokens.
            total_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                if key == "role":
                    total_tokens += 1  # Role is always required and usually 1 token
                elif key in ("content", "name") and value:
                    total_tokens += len(encoding.encode(value))
        elif isinstance(message, str):
            # For plain strings, simply count the encoded tokens.
            total_tokens += len(encoding.encode(message))
        else:
            # Fallback for any other types, convert to string.
            total_tokens += len(encoding.encode(str(message)))
    
    return total_tokens

def generate_output_filename(input_path, language, model_name):
    """Generate standardized output filename with date, time and model info.
    
    Args:
        input_path: Original file path
        language: Target language code (used in logs but not in filename)
        model_name: Name of the translation model used
        
    Returns:
        String containing the new filename path with pattern: 
        original_YYYYMMDD_HHMM_model.ext
    """
    path = Path(input_path)
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    stem = path.stem

    # Clean up model name for filename (remove special chars, limit length)
    safe_model_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in model_name)
    if len(safe_model_name) > 30:  # Limit length to avoid too long filenames
        safe_model_name = safe_model_name[:30]

    # Create new filename with pattern: original_YYYYMMDD_HHMM_model.ext
    new_filename = f"{stem}_{date_str}_{safe_model_name}{path.suffix}"

    return str(path.parent / new_filename)

def log_translation_run(input_path, output_path, run_params):
    """
    Log translation run parameters using the token usage information from the translator instance,
    as well as file token/line counts and extra parameters including batch_size, language, model,
    context_flag, single_translate, and api_calls.

    Args:
        input_path (str): Original file path.
        output_path (str): Output file path.
        run_params (dict): Dictionary of run parameters. Expected to include (optionally)
                           a key 'translate_model' whose value is the translator instance.
                           Also may contain keys:
                             - batch_size
                             - language
                             - model
                             - context_flag
                             - single_translate
                             - api_calls
                             - reasoning_effort
                           as well as prompt file and message info.
    """
    import datetime
    import os
    import json
    from pathlib import Path
    import tiktoken

    # Determine log file path in the same directory as the input file
    log_dir = Path(input_path).parent
    log_file = log_dir / "translation_log.json"
    timestamp = datetime.datetime.now().isoformat()

    # Count lines and tokens in the input file
    input_line_count = 0
    input_file_tokens = 0
    if os.path.exists(input_path):
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                input_text = f.read()
                f.seek(0)
                input_line_count = sum(1 for _ in f)
            encoding = tiktoken.get_encoding("cl100k_base")
            input_file_tokens = len(encoding.encode(input_text))
        except Exception as e:
            print(f"Warning: Could not process input file: {e}")

    # Count lines and tokens in the output file (if it exists)
    output_line_count = 0
    output_file_tokens = 0
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                output_text = f.read()
                f.seek(0)
                output_line_count = sum(1 for _ in f)
            encoding = tiktoken.get_encoding("cl100k_base")
            output_file_tokens = len(encoding.encode(output_text))
        except Exception as e:
            print(f"Warning: Could not process output file: {e}")

    # Extract the translator instance if provided
    translator = run_params.pop("translate_model", None)

    # Build the basic log entry with file info and extra parameters
    log_entry = {
        "timestamp": timestamp,
        "input_file": Path(input_path).name,
        "input_line_count": input_line_count,
        "input_file_tokens": input_file_tokens,
        "output_file": Path(output_path).name,
        "output_line_count": output_line_count,
        "output_file_tokens": output_file_tokens,
        "batch_size": run_params.get("batch_size"),
        "language": run_params.get("language"),
        "model": run_params.get("model"),
        "context_flag": run_params.get("context_flag"),
        "single_translate": run_params.get("single_translate"),
        "api_calls": run_params.get("api_calls"),
        "reasoning_effort": run_params.get("reasoning_effort"),
    }

    # Append the translator's token-usage information if available
    if translator:
        log_entry["cumulative_log_info"] = translator.cumulative_log_info

    # Optionally include prompt template information if provided
    if "prompt_file" in run_params and run_params["prompt_file"]:
        prompt_template = run_params["prompt_file"]
        if isinstance(prompt_template, str) and os.path.exists(prompt_template):
            log_entry["prompt_filename"] = Path(prompt_template).name
        elif isinstance(prompt_template, str) and len(prompt_template) > 20:
            log_entry["prompt_filename"] = "inline_template"

    if "full_user_message" in run_params and run_params["full_user_message"]:
        user_message = run_params["full_user_message"]
        log_entry["full_user_message"] = (
            user_message[:100] + "..." if len(user_message) > 100 else user_message
        )

    if "full_system_message" in run_params and run_params["full_system_message"]:
        system_message = run_params["full_system_message"]
        log_entry["full_system_message"] = (
            system_message[:100] + "..." if len(system_message) > 100 else system_message
        )

    # Load any existing log entries or initialize the log data structure
    log_data = {"runs": []}
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                log_data = json.load(f)
                if isinstance(log_data, list):
                    log_data = {"runs": log_data}
                elif not isinstance(log_data, dict) or "runs" not in log_data:
                    log_data = {"runs": []}
        except (json.JSONDecodeError, Exception):
            log_data = {"runs": []}

    # Append the new entry and write back to the file
    log_data["runs"].append(log_entry)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"Translation run logged to {log_file}")
