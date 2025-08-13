import os
from google.genai import types

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
  try:
    # Normalize paths to prevent directory traversal attacks
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file path is within the permitted working directory
    if not full_path.startswith(working_directory):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file exists and is a regular file
    if not os.path.isfile(full_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read the file content
    with open(full_path, "r") as f:
      file_content_string = f.read(MAX_CHARS)
      return file_content_string
      
  except Exception as e:
    return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory containing the file, specified relative to the working directory. If not provided, defaults to the working directory itself.",
            ),
        },
    ),
)