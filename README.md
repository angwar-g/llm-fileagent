# LLM File Agent
A local file system assistant powered by a Language Model (LLM), enabling natural language interaction to search, manage, and manipulate files directly from your computer.

The LLM File Agent is a lightweight, interactive server that allows users to communicate with their file system intuitively. You can ask the agent to locate files, inspect metadata, read or modify documents, and perform file operations, all using natural language prompts.

> _“Find the latest version of my resume.”_  
> _“Move the file called cover letter to Desktop.”_  
> _“Create a new empty file called `notes.txt` in Downloads.”_

- Powered by [Google Gemini](https://ai.google.dev).
- Converts user instructions into tool calls and workflows.

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/llm-fileagent.git
cd llm-fileagent
```

### 2. Install Requirements
Create a virtual environment (recommended), then:
```bash
pip install -r requirements.txt
```

### 3. Setup API Key
Create a .env file in the project root:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Index Your File System (First-Time Setup)
This will scan your Downloads and Desktop folders and create a searchable file index.
```bash
python build_index.py
```

### 5. Run the Agent
```bash
python app.py
```
