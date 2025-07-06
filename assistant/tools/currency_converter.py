from assistant.base_tool import Tool
from assistant.registry import ToolRegistry

class CurrencyConverterTool(Tool):
    name = "currency_converter"
    description = "Convert amount from one currency to another"

    function_schema = {
        "name": "currency_converter",
        "description": "Convert an amount from one currency to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount of money to convert"
                },
                "from_currency": {
                    "type": "string",
                    "description": "Currency code to convert from (e.g. AUD)"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Currency code to convert to (e.g. USD)"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    }

    async def run(self, amount: float, from_currency: str, to_currency: str) -> str:
        # static example rates relative to AUD
        rates = {
            "AUD": 1.0,
            "USD": 0.68,
            "EUR": 0.62,
            "GBP": 0.53,
            "JPY": 101.5,
            "CAD": 0.91,
            "NZD": 1.08,
            "CNY": 4.70
        }
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in rates or to_currency not in rates:
            return f"Unsupported currency: {from_currency} or {to_currency}"
        
        # Convert amount from from_currency to AUD
        aud_amount = amount / rates[from_currency]

        # Convert AUD to to_currency
        converted_amount = aud_amount * rates[to_currency]

        return f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency}"

# Register tool to the registry
ToolRegistry.register(CurrencyConverterTool)
