import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please set it in your .env file or export it in your shell."
        )

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError(
                "Usage metadata is not available. The API request may have failed."
            )

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.function_calls:
            print(f"Final response:\n{response.text}")
            break

        function_results = []
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts")
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Function call result has no function_response")
            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Function call result has no response")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))
    else:
        print("Error: maximum iterations reached without a final response")
        sys.exit(1)


if __name__ == "__main__":
    main()
