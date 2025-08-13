import os
from google.genai import types

def write_file(working_directory, file_path, content):
  try:
    # Normalize paths to prevent directory traversal attacks
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file path is within the permitted working directory
    # Ensure the full_path is within the working_directory (with trailing separator to avoid partial matches)
    working_directory_with_sep = os.path.join(working_directory, '')
    if not full_path.startswith(working_directory_with_sep):
      return f'Error: Cannot write \"{file_path}\" as it is outside the permitted working directory'

    # Create the relevant directories if it doesn't exist
    os.makedirs(name=os.path.dirname(full_path), exist_ok=True)

    # Write content to the file
    with open(full_path, "w") as file:
      file.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a file at the specified path, securely constrained to the working directory. Creates any necessary directories. Returns a success message with the number of characters written, or an error message if the operation fails.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory in which to write the file. All paths are relative to this directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. Intermediate directories will be created if they do not exist.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)