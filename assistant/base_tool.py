from abc import ABC, abstractmethod
from typing import Any, Protocol, Dict

class Tool(ABC):
    name: str
    description: str
    function_schema: Dict[str, Any] = {}

    @abstractmethod
    async def run(self, *args, **kwargs) -> str:
        pass

    function_schema = {
        "name": "base_tool",
        "description": "Base tool with no parameters",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
