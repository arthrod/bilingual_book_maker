import sys
from pathlib import Path
import datetime
import os

# Add tqdm import with fallback
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Simple fallback progress indicator
    class SimpleTqdm:
        def __init__(self, iterable=None, total=None, desc=None):
            self.iterable = iterable
            self.total = total or len(iterable) if iterable is not None else 0
            self.desc = desc
            self.current = 0
            self.print_progress()

        def __iter__(self):
            for item in self.iterable:
                yield item
                self.current += 1
                self.print_progress()
            print()  # Add final newline

        def print_progress(self):
            if self.total > 0:
                percent = int(100 * self.current / self.total)
                bar_length = 20
                bar = '█' * int(bar_length * self.current / self.total) + ' ' * (bar_length - int(bar_length * self.current / self.total))
                suffix = f"{self.current}/{self.total}"
                if self.desc:
                    prefix = f"{self.desc}: "
                else:
                    prefix = ""
                sys.stdout.write(f"\r{prefix}[{bar}] {percent}% {suffix}")
                sys.stdout.flush()
    
    tqdm = SimpleTqdm

from book_maker.utils import prompt_config_to_kwargs, generate_output_filename, log_translation_run

from .base_loader import BaseBookLoader


class MarkdownBookLoader(BaseBookLoader):
    def __init__(
        self,
        md_name,
        model,
        key,
        resume,
        language,
        model_api_base=None,
        is_test=False,
        test_num=5,
        prompt_config=None,
        prompt_file_path=None,
        single_translate=False,
        context_flag=False,
        context_paragraph_limit=0,
        temperature=1.0,
        batch_size=10,
    ) -> None:
        self.md_name = md_name
        self.translate_model = model(
            key,
            language,
            api_base=model_api_base,
            temperature=temperature,
            **prompt_config_to_kwargs(prompt_config),
        )
        if prompt_file_path:
            self.translate_model.prompt_file = prompt_file_path
        self.is_test = is_test
        self.p_to_save = []
        self.bilingual_result = []
        self.bilingual_temp_result = []
        self.test_num = test_num
        self.batch_size = batch_size
        self.single_translate = single_translate
        self.md_paragraphs = []

        try:
            with open(f"{md_name}", encoding="utf-8") as f:
                self.origin_book = f.read().splitlines()

        except Exception as e:
            raise Exception("can not load file") from e

        self.resume = resume
        self.bin_path = f"{Path(md_name).parent}/.{Path(md_name).stem}.temp.bin"
        if self.resume:
            self.load_state()

        self.process_markdown_content()

    def process_markdown_content(self):
        """Process the original content into markdown paragraphs."""
        current_paragraph = []
        for line in self.origin_book:
            # If it's an empty line and the current paragraph is not empty, save the current paragraph
            if not line.strip() and current_paragraph:
                self.md_paragraphs.append("\n\n".join(current_paragraph))
                current_paragraph = []
            # If it's a title line, treat it as a separate paragraph
            elif line.strip().startswith("#"):
                if current_paragraph:
                    self.md_paragraphs.append("\n\n".join(current_paragraph))
                    current_paragraph = []
                self.md_paragraphs.append(line)
            # In other cases, add to the current paragraph
            else:
                current_paragraph.append(line)

        # Process the last paragraph
        if current_paragraph:
            self.md_paragraphs.append("\n\n".join(current_paragraph))

    @staticmethod
    def _is_special_text(text):
        return text.isdigit() or text.isspace() or len(text) == 0

    def _make_new_book(self, book):
        pass

    def make_bilingual_book(self):
        index = 0
        
        # Initialize temp_file_path attribute
        self.temp_file_path = None

        try:
            sliced_list = [
                self.md_paragraphs[i : i + self.batch_size]
                for i in range(0, len(self.md_paragraphs), self.batch_size)
            ]
            
            # Add progress bar for batch processing
            progress_bar = tqdm(
                sliced_list,
                desc="Translating",
                unit="batch",
                total=len(sliced_list)
            )
            
            for paragraphs in progress_bar:
                batch_text = "\n\n".join(paragraphs)
                if self._is_special_text(batch_text):
                    continue
                if not self.resume or index >= len(self.p_to_save):
                    try:
                        max_retries = 3
                        retry_count = 0
                        while retry_count < max_retries:
                            try:
                                # Update progress bar description with current batch number
                                progress_bar.set_description(f"Translating batch {index//self.batch_size + 1}/{len(sliced_list)}")
                                
                                temp = self.translate_model.translate(batch_text)
                                # Ensure temp is not None and is a string
                                if temp is None:
                                    temp = ""  # Or some default value
                                break
                            except AttributeError as ae:
                                print(f"\nTranslation error: {ae}")
                                retry_count += 1
                                if retry_count == max_retries:
                                    raise Exception("Translation model initialization failed") from ae
                    except Exception as e:
                        print(f"\nError during translation: {e}")
                        raise Exception("Error occurred during translation") from e

                    self.p_to_save.append(temp)
                    if not self.single_translate:
                        self.bilingual_result.append(batch_text)
                    self.bilingual_result.append(temp)
                index += self.batch_size
                if self.is_test and index > self.test_num:
                    break

            # Get model class name for filename
            model_class = self.translate_model.__class__.__name__.lower()
            
            # Get actual model name if available
            actual_model = getattr(self.translate_model, 'model', model_class)
            
            # Generate output filename with date, language and model info
            output_path = generate_output_filename(
                self.md_name,
                self.translate_model.language,
                actual_model
            )
            
            # Save the file
            self.save_file(output_path, self.bilingual_result)
            
            # Log the translation run with detailed information
            log_params = {
                "language": self.translate_model.language,
                "model_class": model_class,
                "model": actual_model,
                "context_flag": getattr(self.translate_model, 'context_flag', False),
                "batch_size": self.batch_size,	
                "temperature": getattr(self.translate_model, 'temperature', 1.0),
                "is_test": self.is_test,
                "test_num": self.test_num if self.is_test else None,
                "single_translate": self.single_translate,
                "prompt_file": getattr(self.translate_model, 'prompt_file', None),
                "api_calls": getattr(self.translate_model, 'api_call_count', 0),
                "translate_model": self.translate_model,
                "full_system_message": getattr(self.translate_model, 'prompt_sys_msg', None),
                "full_user_message": getattr(self.translate_model, 'prompt_template', None),
                "reasoning_effort": getattr(self.translate_model, 'reasoning_effort', "medium")
            }
            log_translation_run(self.md_name, output_path, log_params)
            
            # Remove temp file if translation was successful
            self.remove_temp_file()
            
            print(f"Done! Bilingual book saved as {output_path}")
            return True

        except (KeyboardInterrupt, Exception) as e:
            print(f"\nError: {e}")
            print("Progress will be saved, you can continue later")
            self._save_progress()
            self._save_temp_book()
            sys.exit(1)  # Non-zero exit code indicates an error

    def _save_temp_book(self):
        # Get model class name
        model_class = self.translate_model.__class__.__name__.lower()
        
        # Get actual model name if available
        actual_model = getattr(self.translate_model, 'model', model_class)
        
        # Create temporary filename based on the new pattern
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        stem = Path(self.md_name).stem
        
        # Clean up model name for filename (remove special chars, limit length)
        safe_model_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in actual_model)
        if len(safe_model_name) > 30:  # Limit length to avoid too long filenames
            safe_model_name = safe_model_name[:30]
            
        temp_filename = f"{stem}_{date_str}_{safe_model_name}_temp.txt"
        temp_path = Path(self.md_name).parent / temp_filename
        
        self.save_file(str(temp_path), self.bilingual_result)
        print(f"Temporary book saved as {temp_path}")
        
        # Store the temp path for later removal if needed
        self.temp_file_path = str(temp_path)

    def _save_progress(self):
        try:
            # Filter out None values before joining
            filtered_content = [item for item in self.p_to_save if item is not None]
            with open(self.bin_path, "w", encoding="utf-8") as f:
                f.write("\n".join(filtered_content))
        except Exception as e:
            print(f"Failed to save progress: {e}")
            raise Exception("can not save resume file")

    def load_state(self):
        try:
            with open(self.bin_path, encoding="utf-8") as f:
                self.p_to_save = f.read().splitlines()
        except Exception as e:
            raise Exception("can not load resume file") from e

    def save_file(self, book_path, content):
        try:
            # Filter out None values before joining
            filtered_content = [item for item in content if item is not None]
            with open(book_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(filtered_content))
        except Exception as e:
            print(f"Failed to save file: {e}")
            raise Exception(f"Cannot save file: {e}")

    def remove_temp_file(self):
        """Remove temporary file if it exists and translation was successful."""
        if hasattr(self, 'temp_file_path') and self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.remove(self.temp_file_path)
                print(f"Temporary file removed: {self.temp_file_path}")
            except Exception as e:
                print(f"Warning: Failed to remove temporary file: {e}")
        
        # Also remove the bin file used for resuming translation
        if hasattr(self, 'bin_path') and self.bin_path and os.path.exists(self.bin_path):
            try:
                os.remove(self.bin_path)
            except Exception:
                # Silently fail if we can't remove the bin file
                pass
