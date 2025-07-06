from assistant.base_tool import Tool
from assistant.registry import ToolRegistry
import random

class DiceRollerTool(Tool):
    name = "dice_roller"
    description = "Roll one or more dice with a specified number of sides."
    
    function_schema = {
        "name": "dice_roller",
        "description": "roll dice and get random results.",
        "parameters": {
            "type": "object",
            "properties": {
                "sides": {
                    "type": "integer",
                    "description": "Number of sides on the dice"
                },
                "num_dice": {
                    "type": "integer",
                    "description": "Number of dice to roll"
                }
            },
            "required": ["sides", "num_dice"]
        }
    }

    async def run(self, sides: int, num_dice: int) -> str:
        if sides <= 0 or num_dice <= 0:
            return "Number of sides and dice must be positive."

        results = [random.randint(1, sides) for _ in range(num_dice)]
        rolls_str = ", ".join(str(roll) for roll in results)
        return f"You rolled: {rolls_str}"

ToolRegistry.register(DiceRollerTool)