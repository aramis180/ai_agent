import argparse


def main():
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError ("API key was not found, check it's correctness in .env")

    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = api_key,
    )

    parser = argparse.ArgumentParser(description = "This program provides AI agent with a prompt and returns it's answear.")
    parser.add_argument("user_prompt", type = str, help = "Please provide prompt")
    parser.add_argument("--verbose", action = "store_true", help = "Enable stats for nerds output")
    args = parser.parse_args()
    user_prompt = args.user_prompt

    messages = [
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model = 'openrouter/free',
        messages = messages
    )

    model_response = response.choices[0].message.content

    if response.usage is None:
        raise RuntimeError ("Failed API request")

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    stats_for_nerds = f'Prompt tokens: {prompt_tokens}\nResponse tokens: {completion_tokens}'


    if args.verbose is True:
        output_response = f'User prompt: {user_prompt}\n{stats_for_nerds}\nResponse:\n{model_response}'
    else:
        output_response = f'Response:\n{model_response}'

    return print(output_response)


if __name__ == "__main__":
    main()
