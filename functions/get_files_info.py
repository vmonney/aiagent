import os


def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))

    if os.path.commonpath([abs_working_directory, target_directory]) != abs_working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    try:
        entries = os.listdir(target_directory)
        result_lines = []
        for entry in entries:
            entry_path = os.path.join(target_directory, entry)
            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error: {e}"
