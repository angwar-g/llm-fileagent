import os
import mimetypes
from datetime import datetime
import stat as stat_mod

def get_file_metadata(file_path):
    if not os.path.isfile(file_path):
        return {"error": f"'{file_path}' does not exist or is not a file."}
    try:
        stat = os.stat(file_path)
        metadata = {
            "Full Path": file_path,
            "Size (KB)": round(stat.st_size / 1024, 2),
            "Created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "Modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "Type": mimetypes.guess_type(file_path)[0],
            "Permissions": stat_mod.filemode(stat.st_mode)
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}
