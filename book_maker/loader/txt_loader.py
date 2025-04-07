import sys
from pathlib import Path
import datetime
import os

from book_maker.utils import prompt_config_to_kwargs, generate_output_filename, log_translation_run

from .base_loader import BaseBookLoader


class TXTBookLoader(BaseBookLoader):
    def __init__(
        self,
        txt_name,
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
        batch_size=50,
    ) -> None:
        self.txt_name = txt_name
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

        try:
            with open(f"{txt_name}", encoding="utf-8") as f:
                self.origin_book = f.read().splitlines()

        except Exception as e:
            raise Exception("can not load file") from e

        self.resume = resume
        self.bin_path = f"{Path(txt_name).parent}/.{Path(txt_name).stem}.temp.bin"
        if self.resume:
            self.load_state()

    @staticmethod
    def _is_special_text(text):
        return text.isdigit() or text.isspace() or len(text) == 0

    def _make_new_book(self, book):
        pass

    def make_bilingual_book(self):
        index = 0
        p_to_save_len = len(self.p_to_save)
        
        # Initialize temp_file_path attribute
        self.temp_file_path = None

        try:
            for line in self.origin_book:
                if self._is_special_text(line):
                    continue
                if not self.resume or index >= p_to_save_len:
                    try:
                        t_line = self.translate_model.translate(line)
                    except Exception as e:
                        print(f"translate failed {e}")
                        raise Exception("translation failed") from e
                    self.p_to_save.append(t_line)
                    if not self.single_translate:
                        self.bilingual_result.append(line)
                    self.bilingual_result.append(t_line)
                    index += 1
                    if index % 20 == 0:
                        self._save_progress()
                else:
                    t_line = self.p_to_save[index]
                    if not self.single_translate:
                        self.bilingual_result.append(line)
                    self.bilingual_result.append(t_line)
                    index += 1
                if self.is_test and index > self.test_num:
                    break
            
            # Get model class name for filename
            model_class = self.translate_model.__class__.__name__.lower()
            
            # Get actual model name if available
            actual_model = getattr(self.translate_model, 'model', model_class)
            
            # Generate output filename with date, language and model info
            output_path = generate_output_filename(
                self.txt_name,
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
                "temperature": getattr(self.translate_model, 'temperature', 1.0),
                "is_test": self.is_test,
                "test_num": self.test_num if self.is_test else None,
                "single_translate": self.single_translate,
                "prompt_file": getattr(self.translate_model, 'prompt_file', None),
                "api_calls": getattr(self.translate_model, 'api_call_count', 0),
                "translate_model": self.translate_model
            }
            log_translation_run(self.txt_name, output_path, log_params)
            
            # Remove temp file if translation was successful
            self.remove_temp_file()
            
            print(f"Done! Bilingual book saved as {output_path}")
            return True

        except (KeyboardInterrupt, Exception) as e:
            print(e)
            print("you can resume it next time")
            self._save_progress()
            self._save_temp_book()
            sys.exit(0)

    def _save_temp_book(self):
        # Get model class name
        model_class = self.translate_model.__class__.__name__.lower()
        
        # Get actual model name if available
        actual_model = getattr(self.translate_model, 'model', model_class)
        
        # Create temporary filename based on the new pattern
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        stem = Path(self.txt_name).stem
        
        # Clean up model name for filename (remove special chars, limit length)
        safe_model_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in actual_model)
        if len(safe_model_name) > 30:  # Limit length to avoid too long filenames
            safe_model_name = safe_model_name[:30]
            
        temp_filename = f"{stem}_{date_str}_{safe_model_name}_temp.txt"
        temp_path = Path(self.txt_name).parent / temp_filename
        
        self.save_file(str(temp_path), self.bilingual_result)
        print(f"Temporary book saved as {temp_path}")
        
        # Store the temp path for later removal if needed
        self.temp_file_path = str(temp_path)

    def _save_progress(self):
        try:
            with open(self.bin_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.p_to_save))
        except:
            raise Exception("can not save resume file")

    def load_state(self):
        try:
            with open(self.bin_path, encoding="utf-8") as f:
                self.p_to_save = f.read().splitlines()
        except Exception as e:
            raise Exception("can not load resume file") from e

    def save_file(self, book_path, content):
        try:
            with open(book_path, "w", encoding="utf-8") as f:
                f.write("\n".join(content))
        except:
            raise Exception("can not save file")

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
