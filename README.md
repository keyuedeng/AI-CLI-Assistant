A command-line AI assistant that integrates OpenAI's model with custom tools

Installation and configuration:
- clone the repo
- create virtual environment
- install dependencies
- add environment variables and fill in OpenAI API Key

Running the assistant:
- source .venv/bin/activate
- python -m assistant.main
- Type quit to leave

Available Tools:
1. Calculator
    Description: Evaluates mathematical expressions
    Parameters:
        expression (string) - eg. "2 * 8 + 9"
2. Currency Converter
    Description: Converts an amount from one currency to another (using static rates)
    Parameters:
        amount (number) - amount of money
        from_currency (string) - eg. AUD
        to_currency (string) - eg. USD
3. Dice Roller
    Description: Roll one or more dice with specified number of sides
    Parameters:
        sides (integer) - number of sides on each die
        rolls (integer) - number of dice to roll

How to add a new tool:
- Create a new Python file in assistant/tools/
- inherit from Tool
- Set name, description, function_schema
- implement the async def run(...) method
- register in main.py

