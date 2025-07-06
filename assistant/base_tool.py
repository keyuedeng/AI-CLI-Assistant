from abc import ABC, abstractmethod
from typing import Any, Protocol

class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    async def run(self, *args, **kwargs) -> str:
        pass
