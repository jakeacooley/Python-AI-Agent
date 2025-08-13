import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
  try:
    # Normalize paths to prevent directory traversal attacks
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file path is within the permitted working directory
    # Ensure the full_path is within the working_directory (with trailing separator to avoid partial matches)
    working_directory_with_sep = os.path.join(working_directory, '')
    if not full_path.startswith(working_directory_with_sep):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # ensure file_path exists
    if not os.path.isfile(full_path):
      return f'Error: File "{file_path}" not found.'

    # ensure file ends with .py extension
    if not file_path.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file.'

    # Run the Python file with arguments, capturing stdout and stderr
    cmd = ["python", full_path] + args
    completed_process = subprocess.run(
        cmd,
        cwd=working_directory,
        capture_output=True,
        text=True,
        timeout=30
    )

    # Build output string
    output = ""
    if completed_process.stdout:
      output += f"STDOUT: {completed_process.stdout}"
    if completed_process.stderr:
      output += f"STDERR: {completed_process.stderr}"
    if completed_process.returncode != 0:
      output += f"Process exited with code {completed_process.returncode}"
    
    if not output:
      return "No output produced."
    return output
  except Exception as e:
    return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, securely constrained to the working directory. Captures and returns both standard output and error output from the execution.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory in which to execute the Python file. All paths are relative to this directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory. Must have a .py extension.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional argv list for the Python script. If the user provides a single string argument (e.g., an expression), pass it as a single-element list.",
            ),
        },
    ),
)