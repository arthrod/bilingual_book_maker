"""
inspired by: https://github.com/jesselau76/srt-gpt-translator, MIT License
"""

import re
import sys
from pathlib import Path
import datetime
import os

from book_maker.utils import prompt_config_to_kwargs, generate_output_filename, log_translation_run

from .base_loader import BaseBookLoader


class SRTBookLoader(BaseBookLoader):
    def __init__(
        self,
        srt_name,
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
        accumulated_num=5,
    ) -> None:
        self.srt_name = srt_name
        self.translate_model = model(
            key,
            language,
            api_base=model_api_base,
            temperature=temperature,
            context_flag=context_flag,
            context_paragraph_limit=context_paragraph_limit,
            **prompt_config_to_kwargs(prompt_config),
        )
        if prompt_file_path:
            self.translate_model.prompt_file = prompt_file_path
            
        self.is_test = is_test
        self.p_to_save = []
        self.bilingual_result = []
        self.bilingual_temp_result = []
        self.test_num = test_num
        self.accumulated_num = accumulated_num
        self.blocks = []
        self.single_translate = single_translate

        self.resume = resume
        self.bin_path = f"{Path(srt_name).parent}/.{Path(srt_name).stem}.temp.bin"
        if self.resume:
            self.load_state()

    def _make_new_book(self, book):
        pass

    def _parse_srt(self, srt_text):
        blocks = re.split("\n\s*\n", srt_text)

        final_blocks = []
        new_block = {}
        for i in range(0, len(blocks)):
            block = blocks[i]
            if block.strip() == "":
                continue

            lines = block.strip().splitlines()
            new_block["number"] = lines[0].strip()
            timestamp = lines[1].strip()
            new_block["time"] = timestamp
            text = "\n".join(lines[2:]).strip()
            new_block["text"] = text
            final_blocks.append(new_block)
            new_block = {}

        return final_blocks

    def _get_block_text(self, block):
        return f"{block['number']}\n{block['time']}\n{block['text']}"

    def _get_block_except_text(self, block):
        return f"{block['number']}\n{block['time']}"

    def _concat_blocks(self, sliced_text: str, text: str):
        return f"{sliced_text}\n\n{text}" if sliced_text else text

    def _get_block_translate(self, block):
        return f"{block['number']}\n{block['text']}"

    def _get_block_from(self, text):
        text = text.strip()
        if not text:
            return {}

        block = text.splitlines()
        if len(block) < 2:
            return {"number": block[0], "text": ""}

        return {"number": block[0], "text": "\n".join(block[1:])}

    def _get_blocks_from(self, translate: str):
        if not translate:
            return []

        blocks = []
        blocks_text = translate.strip().split("\n\n")
        for text in blocks_text:
            blocks.append(self._get_block_from(text))

        return blocks

    def _check_blocks(self, translate_blocks, origin_blocks):
        """
        Check if the translated blocks match the original text, with only a simple check of the beginning numbers.
        """
        if len(translate_blocks) != len(origin_blocks):
            return False

        for t in zip(translate_blocks, origin_blocks):
            i = 0
            try:
                i = int(t[0].get("number", 0))
            except ValueError:
                m = re.search(r"\s*\d+", t[0].get("number"))
                if m:
                    i = int(m.group())

            j = int(t[1].get("number", -1))
            if i != j:
                print(f"check failed: {i}!={j}")
                return False

        return True

    def _get_sliced_list(self):
        sliced_list = []
        sliced_text = ""
        begin_index = 0
        for i, block in enumerate(self.blocks):
            text = self._get_block_translate(block)
            if not text:
                continue

            if len(sliced_text + text) < self.accumulated_num:
                sliced_text = self._concat_blocks(sliced_text, text)
            else:
                if sliced_text:
                    sliced_list.append((begin_index, i, sliced_text))
                sliced_text = text
                begin_index = i

        sliced_list.append((begin_index, len(self.blocks), sliced_text))
        return sliced_list

    def make_bilingual_book(self):
        if self.accumulated_num > 512:
            print("warn: accumulated_num > 512, consider smaller blocks in SRT")
            
        # Initialize temp_file_path attribute
        self.temp_file_path = None
        
        try:
            with open(f"{self.srt_name}", encoding="utf-8") as f:
                self.blocks = self._parse_srt(f.read())
        except Exception as e:
            raise Exception("can not load file") from e

        index = 0
        p_to_save_len = len(self.p_to_save)

        try:
            sliced_list = self._get_sliced_list()

            for sliced in sliced_list:
                begin, end, text = sliced

                if not self.resume or index + (end - begin) > p_to_save_len:
                    if index < p_to_save_len:
                        self.p_to_save = self.p_to_save[:index]

                    try:
                        temp = self.translate_model.translate(text)
                    except Exception as e:
                        print(e)
                        raise Exception("Something is wrong when translate") from e

                    translated_blocks = self._get_blocks_from(temp)

                    if self.accumulated_num > 1:
                        if not self._check_blocks(
                            translated_blocks, self.blocks[begin:end]
                        ):
                            translated_blocks = []
                            # try to translate one by one, so don't accumulate too much
                            print(
                                f"retry it one by one:  {self.blocks[begin]['number']} - {self.blocks[end - 1]['number']}"
                            )
                            for block in self.blocks[begin:end]:
                                try:
                                    temp = self.translate_model.translate(
                                        self._get_block_translate(block)
                                    )
                                except Exception as e:
                                    print(e)
                                    raise Exception(
                                        "Something is wrong when translate"
                                    ) from e
                                translated_blocks.append(self._get_block_from(temp))

                            if not self._check_blocks(
                                translated_blocks, self.blocks[begin:end]
                            ):
                                raise Exception(
                                    f"retry failed, adjust the srt manually."
                                )

                    for i, block in enumerate(translated_blocks):
                        text = block.get("text", "")
                        self.p_to_save.append(text)
                        if self.single_translate:
                            self.bilingual_result.append(
                                f"{self._get_block_except_text(self.blocks[begin + i])}\n{text}"
                            )
                        else:
                            self.bilingual_result.append(
                                f"{self._get_block_text(self.blocks[begin + i])}\n{text}"
                            )
                else:
                    for i, block in enumerate(self.blocks[begin:end]):
                        text = self.p_to_save[begin + i]
                        if self.single_translate:
                            self.bilingual_result.append(
                                f"{self._get_block_except_text(self.blocks[begin + i])}\n{text}"
                            )
                        else:
                            self.bilingual_result.append(
                                f"{self._get_block_text(self.blocks[begin + i])}\n{text}"
                            )

                index += end - begin
                if self.is_test and index > self.test_num:
                    break

            # Get model class name for filename
            model_class = self.translate_model.__class__.__name__.lower()
            
            # Get actual model name if available
            actual_model = getattr(self.translate_model, 'model', model_class)
            
            # Generate output filename with date, language and model info
            output_path = generate_output_filename(
                self.srt_name,
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
            log_translation_run(self.srt_name, output_path, log_params)
            
            # Remove temp file if translation was successful
            self.remove_temp_file()
            
            print(f"Done! Bilingual subtitle saved as {output_path}")
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
        stem = Path(self.srt_name).stem
        
        # Clean up model name for filename (remove special chars, limit length)
        safe_model_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in actual_model)
        if len(safe_model_name) > 30:  # Limit length to avoid too long filenames
            safe_model_name = safe_model_name[:30]
            
        temp_filename = f"{stem}_{date_str}_{safe_model_name}_temp.srt"
        temp_path = Path(self.srt_name).parent / temp_filename
        
        self.save_file(str(temp_path), self.bilingual_result)
        print(f"Temporary subtitle file saved as {temp_path}")
        
        # Store the temp path for later removal if needed
        self.temp_file_path = str(temp_path)

    def _save_progress(self):
        try:
            with open(self.bin_path, "w", encoding="utf-8") as f:
                f.write("===".join(self.p_to_save))
        except:
            raise Exception("can not save resume file")

    def load_state(self):
        try:
            with open(self.bin_path, encoding="utf-8") as f:
                text = f.read()
                if text:
                    self.p_to_save = text.split("===")
                else:
                    self.p_to_save = []

        except Exception as e:
            raise Exception("can not load resume file") from e

    def save_file(self, book_path, content):
        try:
            with open(book_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(content))
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
