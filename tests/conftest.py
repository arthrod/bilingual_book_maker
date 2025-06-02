import os
import sys
import pytest

@pytest.fixture(autouse=True)
def _configure_env(monkeypatch):
    root = os.path.dirname(os.path.dirname(__file__))
    sitecustomize_dir = os.path.join(root, 'tests')
    venv_site = os.path.join(root, '.venv', 'lib', f'python{sys.version_info[0]}.{sys.version_info[1]}', 'site-packages')
    pythonpath = os.pathsep.join(filter(None, [sitecustomize_dir, venv_site, os.environ.get('PYTHONPATH', '')]))
    monkeypatch.setenv('PYTHONPATH', pythonpath)
    monkeypatch.setenv('OPENAI_API_KEY', 'test')
    monkeypatch.setenv('BBM_CAIYUN_API_KEY', 'test')
    monkeypatch.setenv('BBM_DEEPL_API_KEY', 'test')
    yield
