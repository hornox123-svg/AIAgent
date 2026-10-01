import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_path, file_path))

        if not os.path.isfile(target_path):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')

        valid_target_path = os.path.commonpath([working_dir_path, target_path]) == working_dir_path
        if not valid_target_path:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')

        file = open(target_path, 'r')
        read_file = file.read(10000)
        if file.read(1):
            read_file += f'[...File "{file_path}" truncated at 10,000 characters]'

        return read_file

    except Exception as e:
        return f'     Error: {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most 10,000 characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
