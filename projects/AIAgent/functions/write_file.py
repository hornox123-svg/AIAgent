import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_path, file_path))

        if os.path.isdir(target_path):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory')

        valid_target_path = os.path.commonpath([working_dir_path, target_path]) == working_dir_path
        if not valid_target_path:
            raise Exception(f'Cannot write to "{file_path}" as it is outside the permitted working directory')

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
