import argparse
import json
import os
from os import environ as env
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

from book_maker.loader import BOOK_LOADER_DICT
from book_maker.translator import MODEL_DICT
from book_maker.utils import LANGUAGES, TO_LANGUAGE_CODE

# Added helper function to load project-specific API keys
def get_project_config(key, project_dir=None):
    """
    Retrieve the API key or other config value from a project-specific .env file if available,
    otherwise fallback to the global .env loaded earlier.
    """
    if project_dir:
        project_env = Path(project_dir) / '.env'
        if project_env.exists():
            load_dotenv(dotenv_path=project_env, override=True)
            value = os.getenv(key)
            if value:
                print(f"Using {key} from project-specific .env file: {project_env}")
                return value
    # Fallback to already loaded global .env
    load_dotenv()
    value = os.getenv(key)
    if value:
        print(f"Using {key} from global .env file")
    return value

def parse_prompt_arg(prompt_arg):
    prompt = None
    prompt_file_path = None  # Initialize prompt_file_path
    
    if prompt_arg is None:
        return prompt, prompt_file_path

    # Check if it's a path to a markdown file (PromptDown format)
    if prompt_arg.endswith(".md") and os.path.exists(prompt_arg):
        try:
            from promptdown import StructuredPrompt

            # Instead of relying on the default PromptDown file loading,
            # we'll read the file with explicit UTF-8 encoding first
            with open(prompt_arg, 'r', encoding='utf-8') as f:
                promptdown_content = f.read()
            
            # Parse from string with explicit UTF-8 content
            structured_prompt = StructuredPrompt.from_promptdown_string(promptdown_content)
            prompt_file_path = prompt_arg  # Store the actual file path
            
            # Initialize our prompt structure
            prompt = {}

            # Handle developer_message or system_message
            # Store both the content and the role type
            system_content = None
            system_role = None
            
            if hasattr(structured_prompt, 'developer_message') and structured_prompt.developer_message:
                system_content = structured_prompt.developer_message
                system_role = 'developer'
            elif hasattr(structured_prompt, 'system_message') and structured_prompt.system_message:
                system_content = structured_prompt.system_message
                system_role = 'system'
            
            # Check for invalid placeholders in system/developer message
            if system_content:
                # Find all placeholders with format {something}
                import re
                invalid_placeholders = re.findall(r'\{([^{}]+)\}', system_content)
                if invalid_placeholders:
                    # Only language and text are allowed in rare cases - but generally no placeholders here
                    disallowed = [p for p in invalid_placeholders if p not in ['language', 'text', 'crlf']]
                    if disallowed:
                        raise ValueError(f"Invalid placeholders found in system/developer message: {', '.join('{' + p + '}' for p in disallowed)}")
                
                prompt['system'] = system_content
                prompt['system_role'] = system_role
            
            # Extract user message from conversation
            user_message = None
            if hasattr(structured_prompt, 'conversation') and structured_prompt.conversation:
                for message in structured_prompt.conversation:
                    if message.role.lower() == 'user':
                        user_message = message.content
                        break
                        
            # Ensure we found a user message
            if not user_message:
                raise ValueError("PromptDown file must contain at least one user message")
            
            # Check for invalid placeholders in user message
            invalid_placeholders = re.findall(r'\{([^{}]+)\}', user_message)
            allowed_placeholders = ['text', 'language', 'crlf']
            disallowed = [p for p in invalid_placeholders if p not in allowed_placeholders]
            if disallowed:
                raise ValueError(f"Invalid placeholders found in user message: {', '.join('{' + p + '}' for p in disallowed)}")
            
            # Check for required placeholders
            if '{text}' not in user_message:
                raise ValueError("User message in PromptDown must contain `{text}` placeholder")
                
            prompt['user'] = user_message
            
            print(f"Successfully loaded PromptDown file: {prompt_arg}")
            return prompt, prompt_file_path
            
        except Exception as e:
            print(f"Error parsing PromptDown file: {e}")
            raise  # Re-raise to stop processing if there's an error
    
    # Existing parsing logic for JSON strings and other formats
    if not any(prompt_arg.endswith(ext) for ext in [".json", ".txt", ".md"]):
        try:
            # user can define prompt by passing a json string
            # eg: --prompt '{"system": "You are a professional translator who translates computer technology books", "user": "Translate \`{text}\` to {language}"}'
            prompt = json.loads(prompt_arg)
            prompt_file_path = "inline_json"  # Mark as inline JSON
        except json.JSONDecodeError:
            # if not a json string, treat it as a template string
            prompt = {"user": prompt_arg}
            prompt_file_path = "inline_template"  # Mark as inline template

    elif os.path.exists(prompt_arg):
        prompt_file_path = prompt_arg  # Store the actual file path
        if prompt_arg.endswith(".txt"):
            # if it's a txt file, treat it as a template string
            with open(prompt_arg, encoding="utf-8") as f:
                prompt = {"user": f.read()}
        elif prompt_arg.endswith(".json"):
            # if it's a json file, treat it as a json object
            # eg: --prompt prompt_template_sample.json
            with open(prompt_arg, encoding="utf-8") as f:
                prompt = json.load(f)
    else:
        raise FileNotFoundError(f"{prompt_arg} not found")

    # if prompt is None or any(c not in prompt["user"] for c in ["{text}", "{language}"]):
    if prompt is None or any(c not in prompt["user"] for c in ["{text}"]):
        raise ValueError("prompt must contain `{text}`")

    if "user" not in prompt:
        raise ValueError("prompt must contain the key of `user`")

    if (prompt.keys() - {"user", "system"}) != set():
        raise ValueError("prompt can only contain the keys of `user` and `system`")

    print("prompt config:", prompt)
    return prompt, prompt_file_path


def main():
    translate_model_list = list(MODEL_DICT.keys())
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--book_name",
        dest="book_name",
        type=str,
        help="path of the epub file to be translated",
    )
    parser.add_argument(
        "--book_from",
        dest="book_from",
        type=str,
        choices=["kobo"],  # support kindle later
        metavar="E-READER",
        help="e-reader type, available: {%(choices)s}",
    )
    parser.add_argument(
        "--device_path",
        dest="device_path",
        type=str,
        help="Path of e-reader device",
    )
    ########## KEYS ##########
    parser.add_argument(
        "--openai_key",
        dest="openai_key",
        type=str,
        default="",
        help="OpenAI api key,if you have more than one key, please use comma"
        " to split them to go beyond the rate limits",
    )
    parser.add_argument(
        "--caiyun_key",
        dest="caiyun_key",
        type=str,
        help="you can apply caiyun key from here (https://dashboard.caiyunapp.com/user/sign_in/)",
    )
    parser.add_argument(
        "--deepl_key",
        dest="deepl_key",
        type=str,
        help="you can apply deepl key from here (https://rapidapi.com/splintPRO/api/dpl-translator",
    )
    parser.add_argument(
        "--claude_key",
        dest="claude_key",
        type=str,
        help="you can find claude key from here (https://console.anthropic.com/account/keys)",
    )

    parser.add_argument(
        "--custom_api",
        dest="custom_api",
        type=str,
        help="you should build your own translation api",
    )

    # for Google Gemini
    parser.add_argument(
        "--gemini_key",
        dest="gemini_key",
        type=str,
        help="You can get Gemini Key from  https://makersuite.google.com/app/apikey",
    )

    # for Groq
    parser.add_argument(
        "--groq_key",
        dest="groq_key",
        type=str,
        help="You can get Groq Key from  https://console.groq.com/keys",
    )

    # for xAI
    parser.add_argument(
        "--xai_key",
        dest="xai_key",
        type=str,
        help="You can get xAI Key from  https://console.x.ai/",
    )

    parser.add_argument(
        "--test",
        dest="test",
        action="store_true",
        help="only the first 10 paragraphs will be translated, for testing",
    )
    parser.add_argument(
        "--test_num",
        dest="test_num",
        type=int,
        default=10,
        help="how many paragraphs will be translated for testing",
    )
    parser.add_argument(
        "-m",
        "--model",
        dest="model",
        type=str,
        default="chatgptapi",
        choices=translate_model_list,  # support DeepL later
        metavar="MODEL",
        help="model to use, available: {%(choices)s}",
    )
    parser.add_argument(
        "--ollama_model",
        dest="ollama_model",
        type=str,
        default="",
        metavar="MODEL",
        help="use ollama",
    )
    parser.add_argument(
        "--language",
        type=str,
        choices=sorted(LANGUAGES.keys())
        + sorted([k.title() for k in TO_LANGUAGE_CODE]),
        default="zh-hans",
        metavar="LANGUAGE",
        help="language to translate to, available: {%(choices)s}",
    )
    parser.add_argument(
        "--resume",
        dest="resume",
        action="store_true",
        help="if program stop unexpected you can use this to resume",
    )
    parser.add_argument(
        "-p",
        "--proxy",
        dest="proxy",
        type=str,
        default="",
        help="use proxy like http://127.0.0.1:7890",
    )
    parser.add_argument(
        "--deployment_id",
        dest="deployment_id",
        type=str,
        help="the deployment name you chose when you deployed the model",
    )
    # args to change api_base
    parser.add_argument(
        "--api_base",
        metavar="API_BASE_URL",
        dest="api_base",
        type=str,
        help="specify base url other than the OpenAI's official API address",
    )
    parser.add_argument(
        "--exclude_filelist",
        dest="exclude_filelist",
        type=str,
        default="",
        help="if you have more than one file to exclude, please use comma to split them, example: --exclude_filelist 'nav.xhtml,cover.xhtml'",
    )
    parser.add_argument(
        "--only_filelist",
        dest="only_filelist",
        type=str,
        default="",
        help="if you only have a few files with translations, please use comma to split them, example: --only_filelist 'nav.xhtml,cover.xhtml'",
    )
    parser.add_argument(
        "--translate-tags",
        dest="translate_tags",
        type=str,
        default="p",
        help="example --translate-tags p,blockquote",
    )
    parser.add_argument(
        "--exclude_translate-tags",
        dest="exclude_translate_tags",
        type=str,
        default="sup",
        help="example --exclude_translate-tags table,sup",
    )
    parser.add_argument(
        "--allow_navigable_strings",
        dest="allow_navigable_strings",
        action="store_true",
        default=False,
        help="allow NavigableStrings to be translated",
    )
    parser.add_argument(
        "--prompt",
        dest="prompt_arg",
        type=str,
        metavar="PROMPT_ARG",
        help="used for customizing the prompt. It can be the prompt template string, or a path to the template file. The valid placeholders are `{text}` and `{language}`.",
    )
    parser.add_argument(
        "--accumulated_num",
        dest="accumulated_num",
        type=int,
        default=1,
        help="""Wait for how many tokens have been accumulated before starting the translation.
gpt3.5 limits the total_token to 4090.
For example, if you use --accumulated_num 1600, maybe openai will output 2200 tokens
and maybe 200 tokens for other messages in the system messages user messages, 1600+2200+200=4000,
So you are close to reaching the limit. You have to choose your own value, there is no way to know if the limit is reached before sending
""",
    )
    parser.add_argument(
        "--translation_style",
        dest="translation_style",
        type=str,
        help="""ex: --translation_style "color: #808080; font-style: italic;" """,
    )
    parser.add_argument(
        "--batch_size",
        dest="batch_size",
        type=int,
        help="how many lines will be translated by aggregated translation (This options currently only applies to txt files)",
    )
    parser.add_argument(
        "--retranslate",
        dest="retranslate",
        nargs=4,
        type=str,
        help="""--retranslate "$translated_filepath" "file_name_in_epub" "start_str" "end_str"(optional)
        Retranslate from start_str to end_str's tag:
        python3 "make_book.py" --book_name "test_books/animal_farm.epub" --retranslate 'test_books/animal_farm_bilingual.epub' 'index_split_002.html' 'in spite of the present book shortage which' 'This kind of thing is not a good symptom. Obviously'
        Retranslate start_str's tag:
        python3 "make_book.py" --book_name "test_books/animal_farm.epub" --retranslate 'test_books/animal_farm_bilingual.epub' 'index_split_002.html' 'in spite of the present book shortage which'
""",
    )
    parser.add_argument(
        "--single_translate",
        action="store_true",
        help="output translated book, no bilingual",
    )
    parser.add_argument(
        "--use_context",
        dest="context_flag",
        action="store_true",
        help="adds an additional paragraph for global, updating historical context of the story to the model's input, improving the narrative consistency for the AI model (this uses ~200 more tokens each time)",
    )
    parser.add_argument(
        "--context_paragraph_limit",
        dest="context_paragraph_limit",
        type=int,
        default=0,
        help="if use --use_context, set context paragraph limit",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="temperature parameter for `chatgptapi`/`gpt4`/`claude`/`gemini`",
    )
    parser.add_argument(
        "--block_size",
        type=int,
        default=-1,
        help="merge multiple paragraphs into one block, may increase accuracy and speed up the process, but disturb the original format, must be used with `--single_translate`",
    )
    parser.add_argument(
        "--model_list",
        type=str,
        dest="model_list",
        help="Rather than using our preset lists of models, specify exactly the models you want as a comma separated list `gpt-4-32k,gpt-3.5-turbo-0125` (Currently only supports: `openai`)",
    )
    parser.add_argument(
        "--batch",
        dest="batch_flag",
        action="store_true",
        help="Enable batch translation using ChatGPT's batch API for improved efficiency",
    )
    parser.add_argument(
        "--batch-use",
        dest="batch_use_flag",
        action="store_true",
        help="Use pre-generated batch translations to create files. Run with --batch first before using this option",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.01,
        help="Request interval in seconds (e.g., 0.1 for 100ms). Currently only supported for Gemini models. Default: 0.01",
    )
    parser.add_argument(
        "--reasoning_effort",
        dest="reasoning_effort",
        type=str,
        default="medium",
        choices=["low", "medium", "high", "auto"],
        help="Set the reasoning effort for o3-mini model (default: medium)",
    )

    options = parser.parse_args()
    project_dir = os.path.dirname(os.path.abspath(options.book_name))

    if not options.book_name:
        print(f"Error: please provide the path of your book using --book_name <path>")
        exit(1)
    if not os.path.isfile(options.book_name):
        print(f"Error: the book {options.book_name!r} does not exist.")
        exit(1)

    PROXY = options.proxy
    if PROXY != "":
        os.environ["http_proxy"] = PROXY
        os.environ["https_proxy"] = PROXY

    translate_model = MODEL_DICT.get(options.model)
    assert translate_model is not None, "unsupported model"
    API_KEY = ""
    if options.model in ["openai", "chatgptapi", "gpt4", "gpt4omini", "gpt4o"]:
        API_KEY = get_project_config("BBM_OPENAI_API_KEY", project_dir) or options.openai_key
        if API_KEY:
            # patch if necessary
            pass
        elif options.ollama_model:
            # any string is ok, can't be empty
            API_KEY = "ollama"
        else:
            raise Exception(
                "OpenAI API key not provided, please google how to obtain it",
            )
    elif options.model == "caiyun":
        API_KEY = get_project_config("BBM_CAIYUN_API_KEY", project_dir) or options.caiyun_key
        if not API_KEY:
            raise Exception("Please provide caiyun key")
    elif options.model == "deepl":
        API_KEY = get_project_config("BBM_DEEPL_API_KEY", project_dir) or options.deepl_key
        if not API_KEY:
            raise Exception("Please provide deepl key")
    elif options.model.startswith("claude"):
        API_KEY = get_project_config("BBM_CLAUDE_API_KEY", project_dir) or options.claude_key
        if not API_KEY:
            raise Exception("Please provide claude key")
    elif options.model == "customapi":
        API_KEY = get_project_config("BBM_CUSTOM_API", project_dir) or options.custom_api
        if not API_KEY:
            raise Exception("Please provide custom translate api")
    elif options.model in ["gemini", "geminipro"]:
        API_KEY = get_project_config("BBM_GOOGLE_GEMINI_KEY", project_dir) or options.gemini_key
    elif options.model == "groq":
        API_KEY = get_project_config("BBM_GROQ_API_KEY", project_dir) or options.groq_key
    elif options.model == "xai":
        API_KEY = get_project_config("BBM_XAI_API_KEY", project_dir) or options.xai_key
    else:
        API_KEY = ""

    if options.book_from == "kobo":
        from book_maker import obok

        device_path = options.device_path
        if device_path is None:
            raise Exception(
                "Device path is not given, please specify the path by --device_path <DEVICE_PATH>",
            )
        options.book_name = obok.cli_main(device_path)

    book_type = options.book_name.split(".")[-1]
    support_type_list = list(BOOK_LOADER_DICT.keys())
    if book_type not in support_type_list:
        raise Exception(
            f"now only support files of these formats: {','.join(support_type_list)}",
        )

    if options.block_size > 0 and not options.single_translate:
        raise Exception(
            "block_size must be used with `--single_translate` because it disturbs the original format",
        )

    book_loader = BOOK_LOADER_DICT.get(book_type)
    assert book_loader is not None, "unsupported loader"
    language = options.language
    if options.language in LANGUAGES:
        # use the value for prompt
        language = LANGUAGES.get(language, language)

    # change api_base for issue #42
    model_api_base = options.api_base

    if options.ollama_model and not model_api_base:
        # ollama default api_base
        model_api_base = "http://localhost:11434/v1"

    e = book_loader(
        options.book_name,
        translate_model,
        API_KEY,
        options.resume,
        language=language,
        model_api_base=model_api_base,
        is_test=options.test,
        test_num=options.test_num,
        prompt_config=parse_prompt_arg(options.prompt_arg)[0],  # Get just the prompt config
        prompt_file_path=parse_prompt_arg(options.prompt_arg)[1],  # Get the prompt file path
        single_translate=options.single_translate,
        context_flag=options.context_flag,
        context_paragraph_limit=options.context_paragraph_limit,
        temperature=options.temperature,
    )
    # other options
    if options.allow_navigable_strings:
        e.allow_navigable_strings = True
    if options.translate_tags:
        e.translate_tags = options.translate_tags
    if options.exclude_translate_tags:
        e.exclude_translate_tags = options.exclude_translate_tags
    if options.exclude_filelist:
        e.exclude_filelist = options.exclude_filelist
    if options.only_filelist:
        e.only_filelist = options.only_filelist
    if options.accumulated_num > 1:
        e.accumulated_num = options.accumulated_num
    if options.translation_style:
        e.translation_style = options.translation_style
    if options.batch_size:
        e.batch_size = options.batch_size
    if options.retranslate:
        e.retranslate = options.retranslate
    if options.deployment_id:
        # only work for ChatGPT api for now
        # later maybe support others
        assert options.model in [
            "chatgptapi",
            "gpt4",
            "gpt4omini",
            "gpt4o",
            "o1",
            "o1preview",
            "o1mini",
            "o3mini",
        ], "only support chatgptapi for deployment_id"
        if not options.api_base:
            raise ValueError("`api_base` must be provided when using `deployment_id`")
        e.translate_model.set_deployment_id(options.deployment_id)
    if options.model in ("openai", "groq"):
        # Currently only supports `openai` when you also have --model_list set
        if options.model_list:
            e.translate_model.set_model_list(options.model_list.split(","))
        else:
            raise ValueError(
                "When using `openai` model, you must also provide `--model_list`. For default model sets use `--model chatgptapi` or `--model gpt4` or `--model gpt4omini`",
            )
    # TODO refactor, quick fix for gpt4 model
    if options.model == "chatgptapi":
        if options.ollama_model:
            e.translate_model.set_gpt35_models(ollama_model=options.ollama_model)
        else:
            e.translate_model.set_gpt35_models()
    if options.model == "gpt4":
        e.translate_model.set_gpt4_models()
    if options.model == "gpt4omini":
        e.translate_model.set_gpt4omini_models()
    if options.model == "gpt4o":
        e.translate_model.set_gpt4o_models()
    if options.model == "o1preview":
        e.translate_model.set_o1preview_models()
    if options.model == "o1":
        e.translate_model.set_o1_models()
    if options.model == "o1mini":
        e.translate_model.set_o1mini_models()
    if options.model == "o3mini":
        e.translate_model.set_o3mini_models()
    if options.model.startswith("claude-"):
        e.translate_model.set_claude_model(options.model)
    if options.block_size > 0:
        e.block_size = options.block_size
    if options.batch_flag:
        e.batch_flag = options.batch_flag
    if options.batch_use_flag:
        e.batch_use_flag = options.batch_use_flag

    if options.model in ("gemini", "geminipro"):
        e.translate_model.set_interval(options.interval)
    if options.model == "gemini":
        if options.model_list:
            e.translate_model.set_model_list(options.model_list.split(","))
        else:
            e.translate_model.set_geminiflash_models()
    if options.model == "geminipro":
        e.translate_model.set_geminipro_models()

    # Set the reasoning_effort parameter BEFORE calling make_bilingual_book
    if hasattr(e, "translate_model"):
        e.translate_model.reasoning_effort = options.reasoning_effort

    # Now call make_bilingual_book with all parameters properly set
    e.make_bilingual_book()


if __name__ == "__main__":
    main()
