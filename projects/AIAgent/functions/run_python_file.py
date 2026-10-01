import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_path, file_path))

        if not os.path.isfile(target_path):
            raise Exception(f'"{file_path}" does not exist or is not a regular file')

        if not target_path.endswith('.py'):
            raise Exception(f'"{file_path}" is not a Python file')

        valid_target_path = os.path.commonpath([working_dir_path, target_path]) == working_dir_path
        if not valid_target_path:
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        command = ["python", target_path]
        if args != None:
            command.extend(args)

        result = subprocess.run(command, capture_output = True, text = True, timeout = 30)

        result_str = ''
        if result.returncode != 0:
            result_str = f"Process exited with code {result.returncode}"

        if result.stdout != None and result.stderr != None:
            result_str += f'STDOUT: {result.stdout}'
            result_str += f'STDERR: {result.stderr}'
        else:
            result_str = "No output produced"

        return result_str

    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}
