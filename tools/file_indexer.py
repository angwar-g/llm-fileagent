import os
import json
from tqdm import tqdm
from config import INDEX_PATH, ROOT_DIRS

def index_files(root_dirs=ROOT_DIRS, save_path=INDEX_PATH):
    index = []

    for root_dir in root_dirs:
        for dirpath, _, filenames in tqdm(os.walk(root_dir), desc=f"Indexing {root_dir}"):
            for f in filenames:
                full_path = os.path.join(dirpath, f)
                index.append(full_path.lower())

    with open(save_path, 'w') as f:
        json.dump(index, f)
    
    return index

def load_index(path=INDEX_PATH):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

    
def build_index():
    """Convenience function to rebuild the index using default settings."""
    return index_files()
