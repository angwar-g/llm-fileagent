# build_index.py
from tools.file_indexer import index_files

if __name__ == "__main__":
    index = index_files()
    print(f"Indexed {len(index)} files.")
