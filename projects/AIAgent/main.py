import os
import sys
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import *

def main():
    #--Getting user message--
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #--getting api key--
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError('Missing api Key')


    #--contacting OpenAI--
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    for _ in range(20):

        #--Getting a response--
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=1,
            tools=available_functions,
        )


        #--Checking response existance--
        if response.usage != None:
            prompt_tokens = response.usage.prompt_tokens
            complete_tokens = response.usage.completion_tokens

            if args.verbose:
                print(f'User prompt: {args.user_prompt}')
                print(f'Prompt tokens: {prompt_tokens}')
                print(f'Response tokens: {complete_tokens}')
        else:
            raise RuntimeError('No usage tokens: Failed API Response')

        message = response.choices[0].message
        messages.append(message)

        #--printing response--
        if message.tool_calls == None:
            print(f"Final response:\n{message.content}")
            return
        else:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                if function_args != '{}':
                    result_message = call_function(tool_call, args.verbose)
                    messages.append(result_message)
                    if result_message['content'] == None:
                        raise Exception("Error: 'content' should not be empty. Failed to get result")
                    if args.verbose:
                        print(f'-> {result_message['content']}')
                else:
                    print(f"Final response:\n{message.content}")
                    return
    print("Max iterations reached without reaching a conclution")
    sys.exit(1)


if __name__ == "__main__":
    main()
