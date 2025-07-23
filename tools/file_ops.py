import os
import shutil
from tools import file_indexer

def read_file(file_path):
    file_path = resolve_path(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"


def resolve_path(file_path: str):
    parts = file_path.split(os.sep) if os.sep in file_path else file_path.split('/')
    
    # Replace root-level folders
    if parts[0].lower() == "downloads":
        parts[0] = os.path.expanduser("~/Downloads")
    elif parts[0].lower() == "desktop":
        parts[0] = os.path.expanduser("~/Desktop")

    return os.path.abspath(os.path.join(*parts))



def write_file(file_path: str, content: str, append: bool = False):
    file_path = resolve_path(file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    mode = 'a' if append else 'w'
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(content)
    
def delete_file(file_path):
    file_path = resolve_path(file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        raise FileNotFoundError(f"No file or directory found at: {file_path}")


