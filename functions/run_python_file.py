
import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = os.path.commonpath([absolute_working_dir, target_dir]) == absolute_working_dir

        if valid_target_dir is False:
            result = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            return (f'{result}')

        if os.path.isfile(target_dir) is False:
            result = f'Error: "{file_path}" does not exist or is not a regular file'
            return (f'{result}')

        if target_dir.endswith(".py") is False:
            result = f'Error: "{file_path}" is not a Python file'
            return result

        command: list[str] = ["python", target_dir]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output = True, text = True, timeout = 30)
        results_to_return = ''
        if result.returncode != 0:
            results_to_return += f'Proces exited with code {result.returncode}'
        if not result.stdout and not result.stderr:
            results_to_return += f'No output produced'
        if result.stdout:
            results_to_return += f'STDOUT: {result.stdout}'
        if result.stderr:
            results_to_return += f'STDERR: {result.stderr}'

        return results_to_return




    except Exception as e:
        return f'Error: executing Python file: {e}'
