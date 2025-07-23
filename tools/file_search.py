import os

def search_files(query, index):
    query = query.lower()
    matches = [path for path in index if query in os.path.basename(path).lower()]
    return matches
