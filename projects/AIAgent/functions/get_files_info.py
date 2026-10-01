import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:


        working_dir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_path, directory))

        if not os.path.isdir(target_dir):
            raise Exception(f'"{directory}" is not a directory')

        valid_target_path = os.path.commonpath([working_dir_path, target_dir]) == working_dir_path
        if not valid_target_path:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')


        #print(f'Success: "{directory}" is within the working directory')


        dir_contents = os.listdir(target_dir)

        dir_info = "  "

        for item in dir_contents:
            item_name = item
            item_size = os.path.getsize(target_dir + "/" + item)
            item_dir = 'is_dir=True' if os.path.isdir(target_dir + "/" + item) else 'is_dir=False'
            item_info = f'- {item_name}: file_size={item_size} bytes, {item_dir}'
            dir_info += ''.join(item_info + '\n  ')
        return dir_info
    except Exception as e:
        return f'     Error: {e}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
