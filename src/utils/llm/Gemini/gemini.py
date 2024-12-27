from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from dotenv import load_dotenv

if TYPE_CHECKING:
    import configparser


class Gemini:
    __config_key = "Gemini"

    def __init__(self, config: configparser.ConfigParser):
        self.model: str = config.get(self.__config_key, "model")

        self.optional_args: GenerationConfig = GenerationConfig(
            candidate_count=config.getint(self.__config_key, "candidate_count", fallback=None),
            max_output_tokens=config.getint(self.__config_key, "max_output_tokens", fallback=None),
            temperature=config.getfloat(self.__config_key, "temperature", fallback=None),
            top_p=config.getfloat(self.__config_key, "top_p", fallback=None),
            top_k=config.getint(self.__config_key, "top_k", fallback=None),
            seed=config.getint(self.__config_key, "seed", fallback=None),
            presence_penalty=config.getfloat(self.__config_key, "presence_penalty", fallback=None),
            frequency_penalty=config.getfloat(
                self.__config_key, "frequency_penalty", fallback=None
            ),
        )

        self.client = genai.GenerativeModel(
            model_name=self.model, generation_config=self.optional_args
        )

    @classmethod
    def load_api_key(cls, config: configparser.ConfigParser) -> None:
        api_key_path: str = config.get("path", "api_key_path")

        if not Path(api_key_path).is_file():
            raise FileNotFoundError(api_key_path, "APIの設定ファイルが見つかりません")

        load_dotenv(api_key_path)
