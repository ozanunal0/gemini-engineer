![gemini-banner.png](public/gemini-banner.png)

# 🤖 Gemini Engineer

An interactive, AI-driven terminal application that acts as a software engineering assistant, leveraging Google's Gemini API with function calling capabilities to perform file system operations and provide intelligent coding assistance.

## ✨ Features

- **AI-Powered Coding Assistant**: Uses Google's Gemini Pro model for intelligent code analysis and suggestions
- **File System Operations**: Read, create, edit, and manage files through AI function calls
- **Interactive Terminal Interface**: Beautiful, feature-rich terminal UI with Rich and prompt_toolkit
- **Function Calling**: Seamless integration between AI reasoning and local file operations
- **Context Management**: Add files and directories to conversation context for better assistance
- **Streaming Responses**: Real-time AI responses with visual feedback
- **Safety Features**: Built-in security checks to prevent directory traversal and handle binary files

## 📷 CLI

![ui.png](public/ui.png)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key

### Installation

1. **Clone or download the project**:
   ```bash
   cd gemini-engineer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**:
   Create a `.env` file in the project directory:
   ```bash
   # Copy the example file and edit it
   cp env.example .env
   # Then edit .env and add your actual API key
   ```
   
   Or create it manually:
   ```bash
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```
   
   **Optional**: You can also specify which Gemini model to use:
   ```bash
   echo "GEMINI_MODEL=gemini-2.5-flash-preview" >> .env
   ```
   
   Available models: `gemini-2.0-flash` (default), `gemini-2.5-flash-preview`, `gemini-2.5-pro-preview`, `gemini-1.5-flash`, `gemini-1.5-pro`
   
   Get your API key from: https://aistudio.google.com/app/apikey

4. **Run the application**:
   ```bash
   python main.py
   ```

## 🎯 Usage

### Basic Commands

- **Chat with AI**: Simply type your questions or requests
- **`/add <file_path>`**: Add a file to conversation context
- **`/add <folder_path>`**: Add all files in a folder to context
- **`/help`**: Show help message
- **`/clear`**: Clear conversation history
- **`/exit`** or **`/quit`**: Exit the application

### Example Interactions

```bash
🤖 gemini-engineer> /add main.py
✅ Added main.py to context

🤖 gemini-engineer> Can you analyze this code and suggest improvements?

🤖 gemini-engineer> Create a simple Python calculator in calc.py

🤖 gemini-engineer> Read the requirements.txt file and explain the dependencies
```

## 🛠️ Available AI Tools

The AI assistant has access to the following file system tools:

### `read_file(file_path)`
Read the content of a single file.

### `read_multiple_files(file_paths)`
Read the contents of multiple files at once.

### `create_file(file_path, content)`
Create a new file or overwrite an existing one.

### `create_multiple_files(files)`
Create multiple files simultaneously.

### `edit_file(file_path, original_snippet, new_snippet)`
Replace specific text snippets in files.

### `list_directory(dir_path)`
List the contents of a directory.

## 🔒 Security Features

- **Path Validation**: Prevents directory traversal attacks (`../`)
- **File Size Limits**: Maximum file size of 1MB for reads/writes
- **Binary File Detection**: Automatically skips binary files
- **Working Directory Restriction**: Operations are confined to the current directory and subdirectories

## 🏗️ Architecture

### Core Components

- **`GeminiEngineer`**: Main application class managing the interactive loop
- **Tool Functions**: File system operations (`read_local_file`, `create_file`, etc.)
- **Tool Schemas**: JSON schemas defining available tools for Gemini
- **Safety Utilities**: Path normalization and file type validation
- **Rich UI**: Terminal interface with panels, tables, and syntax highlighting

### Technology Stack

- **`google-generativeai`**: Gemini API integration
- **`rich`**: Terminal UI and formatting
- **`prompt_toolkit`**: Interactive command-line interface
- **`pydantic`**: Data validation
- **`python-dotenv`**: Environment variable management

## 📝 Examples

### Creating a Python Project

```bash
🤖 gemini-engineer> Create a simple Flask web application with a hello world endpoint
```

The AI will:
1. Create the main Flask app file
2. Set up requirements.txt
3. Create a README with instructions
4. Provide run instructions

### Code Analysis

```bash
🤖 gemini-engineer> /add src/
🤖 gemini-engineer> Analyze this codebase for potential bugs and security issues
```

### Refactoring Code

```bash
🤖 gemini-engineer> /add legacy_code.py
🤖 gemini-engineer> Refactor this code to use modern Python best practices
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

**API Key Error**: Make sure your `.env` file contains a valid Gemini API key.

**Permission Errors**: Ensure you have write permissions in the current directory.

**Import Errors**: Install all dependencies with `pip install -r requirements.txt`.

**Binary File Warnings**: The tool automatically skips binary files for safety.

## 🔮 Future Enhancements

- [ ] Support for more AI models (Claude, GPT-4, etc.)
- [ ] Git integration for version control operations
- [ ] Project templates and scaffolding
- [ ] Code execution in sandboxed environments
- [ ] Plugin system for custom tools
- [ ] Web interface option
- [ ] Team collaboration features

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the existing issues on GitHub
3. Create a new issue with detailed information about your problem

---

**Happy coding with Gemini Engineer! 🚀** 