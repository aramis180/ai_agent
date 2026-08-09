
import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_dir, directory))
        valid_target_dir = os.path.commonpath([absolute_working_dir, target_dir]) == absolute_working_dir

        if valid_target_dir is False:
            result = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return (f'{result}')

        if os.path.isdir(target_dir) is False:
            result = f'Error: "{directory}" is not a directory'
            return (f'{result}')

        #result = f'Success: "{directory}" is within the working directory'
        #return result
        dir_contents = os.listdir(target_dir)
        files_info: list[str] = []
        for i in dir_contents:
            path = '/'.join([target_dir, i])
            name = i
            size = os.path.getsize(path)
            is_dir = False
            if os.path.isdir(path):
                is_dir = True
            files_info.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')

        return '\n'.join(files_info)


    except Exception as e:
        return f'Error: {e}'
