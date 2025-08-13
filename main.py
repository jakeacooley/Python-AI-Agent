import sys
import os
from config import MODEL_NAME
from dotenv import load_dotenv
from google import genai
from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    # Filter out --verbose and get all other arguments as the prompt
    args = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    
    if not args:
        print("Error please provide prompt.")
        sys.exit(1)
    
    user_prompt = " ".join(args)
    verbose = "--verbose" in sys.argv
    
    if verbose:
        print(f"User prompt: {user_prompt}")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    for i in range(20):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],system_instruction=system_prompt
            ))
            
            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.function_calls and len(response.function_calls) > 0:
                function_responses = []
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)

                    # validate result structure
                    if (not function_call_result.parts or not function_call_result.parts[0].function_response):
                        raise Exception("empty function call result")

                    # Print result if verbose
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

                    function_responses.append(function_call_result.parts[0])
                    
                messages.append(types.Content(role="user", parts=function_responses))

                # Check that we got responses
                if not function_responses:
                    raise Exception("no function responses generated, exiting.")
            elif response.text:
                print(f"{response.text}")
                break

            if response.candidates:
                for candidate in response.candidates:
                    print(f"candidate: {candidate}")
                    messages.append(candidate.content)
        except Exception as e:
            raise Exception(e);

if __name__ == "__main__":
    main()
