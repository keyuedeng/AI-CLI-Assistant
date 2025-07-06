from dataclasses import dataclass
from dotenv import load_dotenv
import os
import sys

load_dotenv()

@dataclass
class Config:
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.7

    @classmethod
    def load(cls) -> "Config":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("ERROR: OPENAI_API_KEY is missing in .env")
            sys.exit(1)
        return cls(
            openai_api_key=api_key,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("TEMPERATURE", 0.7))
        )
