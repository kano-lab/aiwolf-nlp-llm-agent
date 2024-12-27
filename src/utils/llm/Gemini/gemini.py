from __future__ import annotations

import configparser
import os
from pathlib import Path
from typing import TYPE_CHECKING

import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import GenerateContentResponse, GenerationConfig

if TYPE_CHECKING:
    from google.generativeai.types import content_types


class Gemini:
    __config_key = "params"

    def __init__(
        self,
        config: configparser.ConfigParser,
        system_instruction: content_types.ContentType = None,
    ) -> None:
        self.load_api_key(config=config)
        gemini_config = self.read_config(config=config)

        self.model: str = gemini_config.get(self.__config_key, "model")

        self.optional_config: GenerationConfig = GenerationConfig(
            candidate_count=gemini_config.getint(
                self.__config_key,
                "candidate_count",
                fallback=None,
            ),
            max_output_tokens=gemini_config.getint(
                self.__config_key,
                "max_output_tokens",
                fallback=None,
            ),
            temperature=gemini_config.getfloat(self.__config_key, "temperature", fallback=None),
            top_p=gemini_config.getfloat(self.__config_key, "top_p", fallback=None),
            top_k=gemini_config.getint(self.__config_key, "top_k", fallback=None),
            seed=gemini_config.getint(self.__config_key, "seed", fallback=None),
            presence_penalty=gemini_config.getfloat(
                self.__config_key,
                "presence_penalty",
                fallback=None,
            ),
            frequency_penalty=gemini_config.getfloat(
                self.__config_key,
                "frequency_penalty",
                fallback=None,
            ),
        )

        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.client = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=system_instruction,
        )
        self.chat = self.client.start_chat(history=[])

    @classmethod
    def read_config(cls, config: configparser.ConfigParser) -> configparser.ConfigParser:
        gemini_config_path: str = config.get("path", "gemini_config")

        if not Path(gemini_config_path).is_file():
            raise FileNotFoundError(gemini_config_path, "Geminiの設定ファイルが見つかりません")

        gemini_config = configparser.ConfigParser()
        gemini_config.read(gemini_config_path)

        return gemini_config

    @classmethod
    def load_api_key(cls, config: configparser.ConfigParser) -> None:
        api_key_path: str = config.get("path", "api_key_path")

        if not Path(api_key_path).is_file():
            raise FileNotFoundError(api_key_path, "APIの設定ファイルが見つかりません")

        load_dotenv(api_key_path)

    def create_message(self, content: content_types.ContentType) -> GenerateContentResponse:
        return self.chat.send_message(content=content, generation_config=self.optional_config)
