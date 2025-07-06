import asyncio
import json

from rich.console import Console
from assistant.config import Config
from assistant.registry import ToolRegistry
from assistant.openai_client import OpenAIClient

console = Console()

async def main():
    # Load config (.env)
    config = Config.load()

    # Setup OpenAI client
    openai_client = OpenAIClient(
        api_key=config.openai_api_key,
        model=config.openai_model,
        temperature=config.temperature,
    )

    # Initialize your tool registry
    tool_registry = ToolRegistry()

    # Register your Calculator tool here
    from assistant.tools.calculator import CalculatorTool
    tool_registry.register(CalculatorTool)

    console.print("[bold green]AI CLI Assistant[/bold green] — type 'exit' to quit")

    # Start conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    while True:
        user_input = console.input("[bold green]> [/bold green]").strip()

        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold red]Goodbye![/bold red]")
            break
        elif user_input.lower() == "tools":
            console.print(f"[yellow]Available tools:[/yellow] {tool_registry.list_tools()}")
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Send to OpenAI with tool definitions
        response = await openai_client.chat_with_tools(
            messages,
            tool_registry.get_functions()
        )

        # If GPT wants to call a function:
        if response.get("function_call"):
            func_name = response["function_call"]["name"]
            args_json = response["function_call"].get("arguments", "{}")

            try:
                args = json.loads(args_json)
            except Exception:
                args = {}


            tool = tool_registry.get_tool(func_name)
            if not tool:
                console.print(f"[red]Unknown tool requested: {func_name}[/red]")
                continue

            # Check required argument before calling run()
            if "expression" not in args:
                console.print(f"[red]Error: Missing required argument 'expression' for tool {func_name}[/red]")
                continue

            # Run the tool (await if async)
            result = await tool().run(**args)

            # Add the function call and result to the conversation history
            messages.append({
                "role": "assistant",
                "content": "",
                "function_call": response["function_call"]
            })

            messages.append({
                "role": "function",
                "name": func_name,
                "content": result
            })

            # Get follow-up reply from GPT with the tool result
            followup = await openai_client.chat(messages)
            messages.append({"role": "assistant", "content": followup["content"]})
            console.print(f"[bold blue]Assistant:[/bold blue] {followup['content']}")

        else:
            # Normal chat reply
            messages.append({"role": "assistant", "content": response["content"]})
            console.print(f"[bold blue]Assistant:[/bold blue] {response['content']}")


if __name__ == "__main__":
    asyncio.run(main())
