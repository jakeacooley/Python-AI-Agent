## AI Coding Agent (Python)

An example terminal AI agent that uses Google Gemini to plan and execute a small set of safe, file-system-related tools within a constrained working directory.

The agent accepts a natural-language prompt and, if needed, calls tools to:

- List files and directories
- Read file contents
- Write files
- Execute Python files with optional args

All tool calls are sandboxed to a single working directory (`./calculator`).

## Requirements

- Python 3.10+
- A Google Generative AI API key
- Dependencies: `google-genai==1.12.1`, `python-dotenv==1.1.0`

## Setup

1) Clone the repo and enter the directory.

2) Install dependencies (pick one):

### Using pip
```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install google-genai==1.12.1 python-dotenv==1.1.0
```

### Using uv
```bash
uv sync
```

3) Configure your API key. Create a `.env` file in the project root with:
```bash
GEMINI_API_KEY=your_api_key_here
```

You can change the model and read limits in `config.py`:

- `MODEL_NAME` (default: `gemini-2.0-flash-001`)
- `MAX_CHARS` for file reads

## Usage

Basic invocation:
```bash
python main.py "List the files in the project"
```

Verbose mode (prints internal traces like token counts and tool call outputs):
```bash
python main.py --verbose "Read the file at pkg/calculator.py and summarize it"
```

Notes:

- The agent is instructed to operate only inside the working directory `./calculator`.
- If the model decides to run tools, paths must be inside `./calculator` or a subdirectory.
- The loop can run for multiple turns (up to 20) until a final text response is produced.

### Example prompts

- "List files in the current directory"
- "Read `pkg/calculator.py`"
- "Write a new file `notes/todo.md` with a short checklist"
- "Run `main.py`"
- "Execute `main.py` with argument '3 + 5'" (the tool passes args to Python scripts)

## What the tools do

Implemented in `functions/` and registered in `main.py`:

- `get_files_info(working_directory, directory=".")`: Lists files with size and whether each is a directory.
- `get_file_content(working_directory, file_path)`: Reads up to `MAX_CHARS` from a file.
- `write_file(working_directory, file_path, content)`: Writes text, creating directories as needed.
- `run_python_file(working_directory, file_path, args=[])`: Executes a `.py` file with optional `args`, returning stdout/stderr.

### Safety constraints

- All tools normalize and validate paths to prevent escaping the working directory. Attempts to access paths outside `./calculator` return an error.
- Python execution is limited to `.py` files and times out after 30 seconds.

## Project structure

```text
ai-agent-python/
├─ main.py                # CLI entrypoint; sends your prompt to Gemini with tool support
├─ config.py              # MODEL_NAME and MAX_CHARS
├─ functions/             # Tool implementations and registry
│  ├─ call_function.py
│  ├─ get_file_content.py
│  ├─ get_files_info.py
│  ├─ run_python.py
│  └─ write_file.py
├─ calculator/            # The sandboxed working directory for tool actions
│  ├─ main.py             # Simple example script
│  ├─ pkg/
│  │  └─ calculator.py    # Infix calculator implementation
│  ├─ tests.py            # Sample script calling the tools
│  └─ README.md
├─ tests.py               # Smoke test script for the tools
├─ pyproject.toml         # Project metadata and dependencies
└─ uv.lock                # Lockfile (if using uv)
```

## Running the included smoke tests

Run the ad-hoc tests that exercise the tool layer directly:
```bash
python tests.py
```

You can also try the `calculator/tests.py` script:
```bash
python calculator/tests.py
```

## Troubleshooting

- "Error please provide prompt.": You need to pass a prompt string to `main.py`.
- API key errors: Ensure `GEMINI_API_KEY` is set in `.env` or your environment.
- "outside the permitted working directory": The requested path is not inside `./calculator`.
- Empty or unexpected output when running a script: Check `STDERR` in the returned output and confirm the file ends with `.py`.

## License

Unspecified. If you plan to distribute this, add a license file.


