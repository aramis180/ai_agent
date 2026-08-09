
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Make changes in a given file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File_path is a name of a file that are going to be changed, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Data that is going to overite given file, only this data is left after changes"
                }
            },
        },
    },
}


import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = os.path.commonpath([absolute_working_dir, target_dir]) == absolute_working_dir
        print(target_dir)
        if valid_target_dir is False:
            result = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            return (f'{result}')

        if os.path.isdir(target_dir) is True:
            result = f'Error: Cannot write to "{file_path}" as it is a directory'
            return (f'{result}')

        os.makedirs(os.path.dirname(target_dir), exist_ok = True)

        with open(target_dir, "w") as f:
            f.write(content)
            result = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            return result




    except Exception as e:
        return f'Error: {e}'
