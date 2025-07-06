import aiohttp
from typing import List, Dict, Optional

class OpenAIClient:
    def __init__(self, api_key: str, model: str, temperature: float = 0.7):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def chat(self, messages: List[Dict]) -> Dict:
        """ Simple chat completion without function calling """
        return await self._post_chat(messages=messages, functions=None, function_call=None)

    async def chat_with_tools(self, messages: List[Dict], functions: List[Dict]) -> Dict:
        """ Chat completion with function calling enabled """
        return await self._post_chat(messages=messages, functions=functions, function_call="auto")

    async def _post_chat(self, messages: List[Dict], functions: Optional[List[Dict]], function_call: Optional[str]) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }

        if functions is not None:
            payload["functions"] = functions
        if function_call is not None:
            payload["function_call"] = function_call

        # Disable SSL verification here - insecure but useful for testing
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(self.api_url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(f"OpenAI API error {resp.status}: {text}")
                data = await resp.json()

        message = data["choices"][0]["message"]
        return message
