import argparse
import json
from config import MAX_ITERATIONS
from functions.call_functions import available_functions, call_function
from prompts import system_prompt
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

def main() -> None:

    parser = argparse.ArgumentParser(description = "This program provides AI agent with a prompt and returns it's answear.")
    parser.add_argument("user_prompt", type = str, help = "Please provide prompt")
    parser.add_argument("--verbose", action = "store_true", help = "Enable stats for nerds output")
    args = parser.parse_args()
    user_prompt = args.user_prompt


    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError ("API key was not found, check it's correctness in .env")

    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    if args.verbose:
        print(f'User prompt: {user_prompt}\n')

    for _ in range(MAX_ITERATIONS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print('Final response')
                print(final_response)
                return
        except Exception as e:
            print(f'Error in generate_content: {e}')

    print(f'Maximum iterations ({MAX_ITERATIONS}) reached')
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:

    response = client.chat.completions.create(
        model = 'openrouter/free',
        messages = messages,
        tools = available_functions
    )

    if not response.usage:
        raise RuntimeError ("Failed API request")

    if verbose:
        print('Prompt tokens:', response.usage.prompt_tokens)
        print('Response tokens:', response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    tool_calls_response = message

    for tool_call in tool_calls_response.tool_calls:
        if tool_call.type != 'function':
            continue
        result_message = call_function(tool_call, verbose)
        if not result_message.get('content'):
            raise RuntimeError(f'Empty function response for {tool_call.function.name}')
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

    return None



if __name__ == "__main__":
    main()
