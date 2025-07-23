from google import genai
from google.genai import types
from config import GEMINI_API_KEY
from tools import file_indexer, file_search, metadata, file_ops

import os

# Load index once
FILE_INDEX = file_indexer.load_index()
 
client = genai.Client(api_key=GEMINI_API_KEY)

# ========================
# TOOL FUNCTION DEFINITIONS
# ========================

def search_files(query: str):
    global FILE_INDEX
    matches = file_search.search_files(query, FILE_INDEX)
    return matches[:5]

def get_metadata(file_path: str):
    return metadata.get_file_metadata(file_path)

def read_file(file_path: str):
    return file_ops.read_file(file_path)

def write_file(file_path: str, content: str, append: bool = False):
    global FILE_INDEX
    file_ops.write_file(file_path, content, append)
    FILE_INDEX = file_indexer.build_index()
    resolved_path = file_ops.resolve_path(file_path)
    return f"{'Appended' if append else 'Written'} to {resolved_path}"


# Add this at the top if not already there
PENDING_DELETIONS = {}

def delete_file(file_path: str, confirm: str = None):
    global PENDING_DELETIONS, FILE_INDEX

    file_path = os.path.abspath(file_path)

    # If no confirmation is provided, ask for it
    if confirm is None:
        PENDING_DELETIONS["file"] = file_path
        return f"Are you sure you want to delete `{file_path}`? Type 'yes' to confirm."

    # If confirmation is provided, delete without requiring exact match
    if confirm.lower() == "yes":
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        file_ops.delete_file(file_path)
        FILE_INDEX = file_indexer.build_index()
        PENDING_DELETIONS.pop("file", None)
        return f"Deleted {file_path}"

    return "Deletion cancelled or invalid confirmation."



def find_latest_file_by_name(name_query: str):
    global FILE_INDEX
    matches = file_search.search_files(name_query, FILE_INDEX)
    if not matches:
        return "No matching files found."

    # Get metadata and pick latest
    latest_file = max(matches, key=lambda f: os.path.getmtime(f))
    return f"Latest file: {latest_file} (last modified: {os.path.getmtime(latest_file)})"


def move_file_by_name(filename: str, destination: str = "Desktop"):
    global FILE_INDEX
    matches = file_search.search_files(filename, FILE_INDEX)
    if not matches:
        return f"No file found with name matching: '{filename}'"

    file_path = matches[0]
    dest_dir = os.path.expanduser(f"~/{destination}")
    os.makedirs(dest_dir, exist_ok=True)
    new_path = os.path.join(dest_dir, os.path.basename(file_path))

    try:
        os.rename(file_path, new_path)
        FILE_INDEX = file_indexer.build_index()
        return f"Moved file to: {new_path}"
    except Exception as e:
        return f"Failed to move file: {str(e)}"

def create_empty_file(file_path: str):
    global FILE_INDEX
    file_ops.write_file(file_path, content="", append=False)
    FILE_INDEX = file_indexer.build_index()
    resolved_path = file_ops.resolve_path(file_path)
    return f"Created empty file at: {resolved_path}"

tool_declarations = [
    {
        "name": "searchFiles",
        "description": "Searches files whose names match a given query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Partial or full name of the file to search for"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "getMetadata",
        "description": "Gets metadata (path, size, dates, etc.) of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Full file path"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "readFile",
        "description": "Reads the content of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Full file path"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "writeFile",
        "description": "Writes or appends content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "content": {"type": "string"},
                "append": {"type": "boolean", "default": False}
            },
            "required": ["file_path", "content"]
        }
    },
    {
    "name": "deleteFile",
    "description": "Deletes a file or directory at the given path, with confirmation.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
            "confirm": {
                "type": "string",
                "description": "User confirmation input like 'yes'"
            }
        },
        "required": ["file_path"]
    }
},
    {
    "name": "findLatestFile",
    "description": "Finds the most recently modified file whose name matches a given query.",
    "parameters": {
        "type": "object",
        "properties": {
            "name_query": {
                "type": "string",
                "description": "Keyword to match in the file name, like 'resume' or 'report'"
            }
        },
        "required": ["name_query"]
    }
},
{
    "name": "moveFileByName",
    "description": "Finds a file by name and moves it to a destination folder like Desktop or Documents.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {"type": "string"},
            "destination": {
                "type": "string",
                "default": "Desktop",
                "description": "Target folder name like Desktop or Documents"
            }
        },
        "required": ["filename"]
    }
},
{
  "name": "createEmptyFile",
  "description": "Creates an empty file at the specified path.",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string"}
    },
    "required": ["file_path"]
  }
}
]

function_map = {
    "searchFiles": search_files,
    "getMetadata": get_metadata,
    "readFile": read_file,
    "writeFile": write_file,
    "deleteFile": delete_file,
    "findLatestFile": find_latest_file_by_name,
    "moveFileByName": move_file_by_name,
    "createEmptyFile": create_empty_file
}

# ========================
# MAIN HANDLER
# ========================

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=tool_declarations)]
)

def handle_prompt(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=types.Content(parts=[types.Part(text=prompt)]), 
            config=config
        )

        part = response.candidates[0].content.parts[0]
        func_call = getattr(part, "function_call", None)

        if func_call is not None:
            func_name = func_call.name
            func_args = func_call.args

            print(f"[Gemini decided to call]: {func_name}({func_args})")

            func = function_map.get(func_name)
            if not func:
                return f"Function {func_name} not implemented."

            return func(**func_args)

        # No function call — return LLM's natural reply
        return part.text if hasattr(part, "text") else str(part)

    except Exception as e:
        return f"Gemini API Error: {e}"
