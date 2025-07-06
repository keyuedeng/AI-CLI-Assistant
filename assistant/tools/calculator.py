from assistant.base_tool import Tool
from assistant.registry import ToolRegistry

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate a safe mathematical expression"

    # Add function schema property for OpenAI function calling
    function_schema = {
        "name": "calculator",
        "description": "Evaluate a safe mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    }

    async def run(self, expression: str) -> str:
        import math
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        try:
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {e}"

ToolRegistry.register(CalculatorTool)
