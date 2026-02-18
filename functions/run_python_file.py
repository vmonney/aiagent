import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(abs_working_directory, file_path)
        )

        if (
            os.path.commonpath([abs_working_directory, target_path])
            != abs_working_directory
        ):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the'
                " permitted working directory"
            )

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, target_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
