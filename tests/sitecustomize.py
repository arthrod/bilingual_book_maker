import sys
import os

# Ensure local .venv site-packages are available
root = os.path.dirname(os.path.dirname(__file__))
venv_path = os.path.join(root, '.venv', 'lib', f'python{sys.version_info[0]}.{sys.version_info[1]}', 'site-packages')
if os.path.isdir(venv_path):
    sys.path.insert(0, venv_path)
sys.path.insert(0, root)

from book_maker.translator.base_translator import Base
import book_maker.translator as translator

class MockTranslator(Base):
    def __init__(self, key, language, **kwargs):
        super().__init__(key, language)
        self.language = language

    def rotate_key(self):
        pass

    def translate(self, text, needprint=True):
        result = f"{text} ({self.language})"
        if needprint:
            print(result)
        return result

translator.MODEL_DICT = {name: MockTranslator for name in translator.MODEL_DICT}
