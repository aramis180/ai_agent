
schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_files_content",
        "description": "Provide content of a given file with a limitation of characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File_path is a name of a file that are going to be read, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


import os
from config import max_chars

def get_file_content(working_directory: str, file_path:str) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = os.path.commonpath([absolute_working_dir, target_dir]) == absolute_working_dir

        if valid_target_dir is False:
            result = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            return (f'{result}')

        if os.path.isfile(target_dir) is False:
            result = f'Error: File not found or is not a regular file: "{file_path}"'
            return (f'{result}')

        with open(target_dir, "r") as f:
            file_content_string = f.read(max_chars)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {max_chars} characters]'
            return file_content_string




    except Exception as e:
        return f'Error: {e}'
