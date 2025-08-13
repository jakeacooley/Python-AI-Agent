import os
from google.genai import types

def get_files_info(working_directory, directory="."):
  try:
    full_path = os.path.join(working_directory, directory)
    if not os.path.isdir(full_path):
      return f'Error: "{directory}" is not a directory'

    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    if not abs_full_path.startswith(abs_working_directory + os.sep) and abs_full_path != abs_working_directory:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    files = os.listdir(path=abs_full_path)
    
    # Build the output string
    result_lines = []
    
    for file in sorted(files):
      file_path = os.path.join(abs_full_path, file)
      file_size = os.path.getsize(file_path)
      is_dir = os.path.isdir(file_path)
      result_lines.append(f" - {file}: file_size={file_size} bytes, is_dir={is_dir}")
    
    return "\n".join(result_lines)
  except Exception as e:
    return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory in which to list files. All paths are relative to this directory.",
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)