from typing import Dict, Type, Optional
from .base_tool import Tool

class ToolRegistry:
    _tools: Dict[str, Type[Tool]] = {}

    @classmethod
    def register(cls, tool_class: Type[Tool]) -> None:
        cls._tools[tool_class.name] = tool_class

    @classmethod
    def get_tool(cls, name: str) -> Optional[Type[Tool]]:
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls) -> Dict[str, Type[Tool]]:
        return cls._tools.copy()
    
    @classmethod
    def get_functions(cls) -> list:
        functions = []
        for tool_class in cls._tools.values():
            if hasattr(tool_class, "function_schema"):
                functions.append(tool_class.function_schema)
            else:
                # fallback empty schema if none defined
                function_def = {
                    "name": tool_class.name,
                    "description": tool_class.description,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
                functions.append(function_def)
        return functions

