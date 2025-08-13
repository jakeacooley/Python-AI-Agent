from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

FUNCTION_REGISTRY = {
  "get_file_content": get_file_content,
  "get_files_info": get_files_info,
  "run_python_file": run_python_file,
  "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
  if verbose == True:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  if function_call_part.name in FUNCTION_REGISTRY:
    args_with_working_dir = function_call_part.args.copy()
    args_with_working_dir["working_directory"] = "./calculator"
    function_result = FUNCTION_REGISTRY[function_call_part.name](**args_with_working_dir)

    return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_call_part.name,
              response={"result": function_result},
          )
      ],
    )
  else:
    return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_call_part.name,
              response={"error": f"Unknown function: {function_call_part.name}"},
          )
      ],
  )