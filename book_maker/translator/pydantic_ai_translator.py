from __future__ import annotations

import os
from itertools import cycle
from typing import Optional

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from .base_translator import Base


class PydanticAITranslator(Base):
    """Translator using the `pydantic_ai` library."""

    DEFAULT_PROMPT = (
        "Please translate `{text}` to {language}, return only the translated content"
    )

    def __init__(
        self,
        key: str,
        language: str,
        model: str = "openai:gpt-3.5-turbo",
        api_base: Optional[str] = None,
        prompt_template: Optional[str] = None,
        prompt_sys_msg: Optional[str] = None,
        temperature: float = 1.0,
        **kwargs,
    ) -> None:
        super().__init__(key, language)
        self.model = model
        self.api_base = api_base
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT
        self.prompt_sys_msg = prompt_sys_msg or ""
        self.temperature = temperature
        self.keys = cycle(key.split(","))
        self.current_key = next(self.keys)

    def rotate_key(self) -> None:
        self.current_key = next(self.keys)

    def _create_agent(self) -> Agent:
        os.environ["OPENAI_API_KEY"] = self.current_key
        if self.api_base:
            os.environ["OPENAI_BASE_URL"] = self.api_base
        settings = ModelSettings(temperature=self.temperature)
        return Agent(self.model, instructions=self.prompt_sys_msg, model_settings=settings)

    def translate(self, text: str, needprint: bool = True) -> str:
        self.rotate_key()
        agent = self._create_agent()
        prompt = self.prompt_template.format(text=text, language=self.language, crlf="\n")
        result = agent.run_sync(prompt)
        translated = result.output or ""
        if needprint:
            print(translated)
        return translated
