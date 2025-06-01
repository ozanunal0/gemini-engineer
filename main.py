#!/usr/bin/env python3
"""
Gemini Engineer - AI-driven terminal application for software engineering assistance.

This application leverages Gemini's function calling capabilities to perform file system
operations and provide intelligent coding assistance through an interactive terminal interface.
"""

import os
import sys
import json
import asyncio
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

# Third-party imports
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# File size limit (1MB)
MAX_FILE_SIZE = 1024 * 1024

@dataclass
class ConversationMessage:
    """Represents a message in the conversation history."""
    role: str
    content: str
    timestamp: Optional[str] = None

def normalize_path(file_path: str) -> Path:
    """Normalize and validate file path to prevent directory traversal."""
    path = Path(file_path).resolve()
    cwd = Path.cwd().resolve()
    
    # Ensure the path is within the current working directory
    try:
        path.relative_to(cwd)
    except ValueError:
        raise ValueError(f"Path {file_path} is outside the current directory")
    
    return path

def is_binary_file(file_path: Path) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return True

def is_text_file(file_path: Path) -> bool:
    """Check if a file is a text file based on extension and content."""
    if file_path.suffix.lower() in ['.txt', '.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.md', '.rst', '.sh', '.bat']:
        return True
    
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type and mime_type.startswith('text/'):
        return True
    
    return not is_binary_file(file_path)

def read_local_file(file_path: str) -> Dict[str, Any]:
    """Read content of a single file."""
    try:
        path = normalize_path(file_path)
        
        if not path.exists():
            return {"error": f"File {file_path} does not exist"}
        
        if not path.is_file():
            return {"error": f"{file_path} is not a file"}
        
        if path.stat().st_size > MAX_FILE_SIZE:
            return {"error": f"File {file_path} is too large (max {MAX_FILE_SIZE} bytes)"}
        
        if not is_text_file(path):
            return {"error": f"File {file_path} appears to be binary"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "file_path": str(path),
            "content": content,
            "size": len(content)
        }
    except Exception as e:
        return {"error": f"Failed to read {file_path}: {str(e)}"}

def read_multiple_files(file_paths: List[str]) -> Dict[str, Any]:
    """Read contents of multiple files."""
    results = {}
    errors = []
    
    for file_path in file_paths:
        result = read_local_file(file_path)
        if "error" in result:
            errors.append(f"{file_path}: {result['error']}")
        else:
            results[file_path] = result
    
    return {
        "success": len(errors) == 0,
        "files": results,
        "errors": errors
    }

def create_file(file_path: str, content: str) -> Dict[str, Any]:
    """Create a new file or overwrite an existing one."""
    try:
        path = normalize_path(file_path)
        
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": str(path),
            "size": len(content),
            "message": f"File {file_path} created successfully"
        }
    except Exception as e:
        return {"error": f"Failed to create {file_path}: {str(e)}"}

def create_multiple_files(files: List[Dict[str, str]]) -> Dict[str, Any]:
    """Create multiple files."""
    results = {}
    errors = []
    
    for file_info in files:
        if "path" not in file_info or "content" not in file_info:
            errors.append("File info must contain 'path' and 'content' keys")
            continue
        
        result = create_file(file_info["path"], file_info["content"])
        if "error" in result:
            errors.append(f"{file_info['path']}: {result['error']}")
        else:
            results[file_info["path"]] = result
    
    return {
        "success": len(errors) == 0,
        "files": results,
        "errors": errors
    }

def edit_file(file_path: str, original_snippet: str, new_snippet: str) -> Dict[str, Any]:
    """Replace a specific original_snippet with new_snippet in a file."""
    try:
        path = normalize_path(file_path)
        
        if not path.exists():
            return {"error": f"File {file_path} does not exist"}
        
        # Read current content
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if original_snippet not in content:
            return {"error": f"Original snippet not found in {file_path}"}
        
        # Replace the snippet
        new_content = content.replace(original_snippet, new_snippet)
        
        # Write back to file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            "success": True,
            "file_path": str(path),
            "message": f"File {file_path} edited successfully",
            "changes": {
                "original_length": len(content),
                "new_length": len(new_content),
                "diff": len(new_content) - len(content)
            }
        }
    except Exception as e:
        return {"error": f"Failed to edit {file_path}: {str(e)}"}

def list_directory(dir_path: str = ".") -> Dict[str, Any]:
    """List contents of a directory."""
    try:
        path = normalize_path(dir_path)
        
        if not path.exists():
            return {"error": f"Directory {dir_path} does not exist"}
        
        if not path.is_dir():
            return {"error": f"{dir_path} is not a directory"}
        
        items = []
        for item in path.iterdir():
            item_info = {
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            }
            items.append(item_info)
        
        return {
            "success": True,
            "directory": str(path),
            "items": items,
            "count": len(items)
        }
    except Exception as e:
        return {"error": f"Failed to list directory {dir_path}: {str(e)}"}

# Tool definitions for Gemini function calling
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the content of a single file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "read_multiple_files",
        "description": "Read the contents of multiple files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths to read"
                }
            },
            "required": ["file_paths"]
        }
    },
    {
        "name": "create_file",
        "description": "Create a new file or overwrite an existing one",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path where the file should be created"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "create_multiple_files",
        "description": "Create multiple files at once",
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["path", "content"]
                    },
                    "description": "List of files to create, each with path and content"
                }
            },
            "required": ["files"]
        }
    },
    {
        "name": "edit_file",
        "description": "Replace a specific snippet in a file with new content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit"
                },
                "original_snippet": {
                    "type": "string",
                    "description": "The exact text to be replaced"
                },
                "new_snippet": {
                    "type": "string",
                    "description": "The new text to replace the original snippet"
                }
            },
            "required": ["file_path", "original_snippet", "new_snippet"]
        }
    },
    {
        "name": "list_directory",
        "description": "List the contents of a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory to list (default: current directory)"
                }
            }
        }
    }
]

# Function mapping for tool execution
TOOL_FUNCTIONS = {
    "read_file": read_local_file,
    "read_multiple_files": read_multiple_files,
    "create_file": create_file,
    "create_multiple_files": create_multiple_files,
    "edit_file": edit_file,
    "list_directory": list_directory
}

class GeminiEngineer:
    """Main application class for Gemini Engineer."""
    
    def __init__(self):
        self.console = Console()
        self.conversation_history: List[ConversationMessage] = []
        self.model = None
        self.history = InMemoryHistory()
        self.setup_gemini_client()
        
    def setup_gemini_client(self):
        """Initialize the Gemini client and model."""
        api_key = os.getenv('GEMINI_API_KEY')
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash-preview-05-20')  # Default to gemini-2.5-flash-preview-05-20
        
        if not api_key or api_key == 'your_api_key_here':
            self.console.print(Panel(
                "[red]❌ Gemini API key not found![/red]\n\n"
                "Please set your GEMINI_API_KEY environment variable:\n"
                "1. Create a .env file in this directory\n"
                "2. Add: GEMINI_API_KEY=your_actual_api_key\n"
                "3. Get your API key from: https://aistudio.google.com/app/apikey",
                title="Setup Required",
                border_style="red"
            ))
            sys.exit(1)
            
        try:
            genai.configure(api_key=api_key)
            # Use configurable model name from environment variable
            self.model = genai.GenerativeModel(model_name)
            self.console.print(f"[green]✅ Gemini client initialized successfully! (Model: {model_name})[/green]")
        except Exception as e:
            self.console.print(f"[red]❌ Failed to initialize Gemini client: {e}[/red]")
            self.console.print(f"[yellow]💡 Make sure the model '{model_name}' is valid and available[/yellow]")
            sys.exit(1)
    
    def display_welcome_banner(self):
        """Display the welcome banner and instructions."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                        🤖 GEMINI ENGINEER                    ║
║                   AI-Driven Coding Assistant                 ║
╚══════════════════════════════════════════════════════════════╝
        """
        
        instructions = """
[bold cyan]Available Commands:[/bold cyan]
• [yellow]/add <file_path>[/yellow] - Add a file to conversation context
• [yellow]/add <folder_path>[/yellow] - Add all files in a folder to context
• [yellow]/exit[/yellow] or [yellow]/quit[/yellow] - Exit the application
• [yellow]/help[/yellow] - Show this help message
• [yellow]/clear[/yellow] - Clear conversation history

[bold cyan]Features:[/bold cyan]
• File system operations (read, create, edit files)
• Code analysis and suggestions
• Interactive file management
• Streaming AI responses with function calling

[bold green]Ready to assist with your coding tasks![/bold green]
        """
        
        self.console.print(Panel(banner, style="bold blue"))
        self.console.print(Panel(instructions, title="Getting Started", border_style="cyan"))

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool function and return the result."""
        try:
            if tool_name not in TOOL_FUNCTIONS:
                return {"error": f"Unknown tool: {tool_name}"}
            
            tool_function = TOOL_FUNCTIONS[tool_name]
            
            # Execute the function with the provided parameters
            if tool_name == "list_directory" and not parameters:
                result = tool_function()
            else:
                result = tool_function(**parameters)
            
            return result
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def display_tool_result(self, tool_name: str, result: Dict[str, Any]):
        """Display tool execution results with rich formatting."""
        if "error" in result:
            self.console.print(Panel(
                f"[red]❌ {result['error']}[/red]",
                title=f"Tool Error: {tool_name}",
                border_style="red"
            ))
        else:
            if tool_name == "read_file":
                self.console.print(Panel(
                    f"[green]✅ Read {result['file_path']} ({result['size']} characters)[/green]",
                    title="File Read",
                    border_style="green"
                ))
            elif tool_name == "create_file":
                self.console.print(Panel(
                    f"[green]✅ {result['message']} ({result['size']} characters)[/green]",
                    title="File Created",
                    border_style="green"
                ))
            elif tool_name == "edit_file":
                self.console.print(Panel(
                    f"[green]✅ {result['message']}[/green]\n"
                    f"Changes: {result['changes']['diff']:+d} characters",
                    title="File Edited",
                    border_style="green"
                ))
            elif tool_name == "list_directory":
                table = Table(title=f"Directory: {result['directory']}")
                table.add_column("Name", style="cyan")
                table.add_column("Type", style="magenta")
                table.add_column("Size", style="green")
                
                for item in result['items']:
                    size_str = str(item['size']) if item['size'] else "-"
                    table.add_row(item['name'], item['type'], size_str)
                
                self.console.print(table)

    def stream_gemini_response(self, user_input: str):
        """Stream response from Gemini with function calling support."""
        try:
            # Add user message to history
            self.conversation_history.append(ConversationMessage("user", user_input))
            
            # Prepare messages for Gemini
            messages = []
            for msg in self.conversation_history:
                if msg.role == "function":
                    continue  # Skip function responses in this simplified version
                messages.append({"role": msg.role, "parts": [msg.content]})
            
            # Start the generation
            with Progress(SpinnerColumn(), TextColumn("[blue]Thinking..."), console=self.console) as progress:
                task = progress.add_task("processing", total=None)
                
                # Generate content with tools
                try:
                    response = self.model.generate_content(
                        messages,
                        tools=[{"function_declarations": TOOLS}],
                        stream=True
                    )
                except Exception as e:
                    # Fallback to non-streaming if streaming fails
                    self.console.print(f"[yellow]⚠️ Streaming failed, using regular response: {e}[/yellow]")
                    response = self.model.generate_content(
                        messages,
                        tools=[{"function_declarations": TOOLS}],
                        stream=False
                    )
                    response = [response]  # Make it iterable
                
                progress.remove_task(task)
            
            # Process the streaming response
            ai_response_parts = []
            tool_calls = []
            
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    ai_response_parts.append(chunk.text)
                    self.console.print(chunk.text, end="")
                
                # Check for function calls in the response
                if hasattr(chunk, 'candidates') and chunk.candidates:
                    for candidate in chunk.candidates:
                        if hasattr(candidate, 'content') and candidate.content:
                            for part in candidate.content.parts:
                                if hasattr(part, 'function_call') and part.function_call:
                                    tool_calls.append(part.function_call)
            
            if ai_response_parts:
                ai_response = "".join(ai_response_parts)
                self.conversation_history.append(ConversationMessage("assistant", ai_response))
                print()  # New line after streaming
            
            # Execute any tool calls
            if tool_calls:
                self.console.print("\n[yellow]🔧 Executing tools...[/yellow]")
                
                for tool_call in tool_calls:
                    tool_name = tool_call.name
                    parameters = {}
                    
                    # Extract parameters from the function call
                    if hasattr(tool_call, 'args') and tool_call.args:
                        for key, value in tool_call.args.items():
                            parameters[key] = value
                    
                    self.console.print(f"[cyan]▶ {tool_name}({', '.join(f'{k}={v}' for k, v in parameters.items())})[/cyan]")
                    
                    result = self.execute_tool(tool_name, parameters)
                    self.display_tool_result(tool_name, result)
                    
                    # Create function response and continue conversation
                    function_response_content = f"Function {tool_name} executed with result: {result}"
                    
                    # Get follow-up response from Gemini
                    follow_up_messages = messages + [
                        {"role": "assistant", "parts": [f"I'll call the {tool_name} function."]},
                        {"role": "function", "parts": [function_response_content]}
                    ]
                    
                    try:
                        follow_up_response = self.model.generate_content(follow_up_messages, stream=True)
                        
                        follow_up_parts = []
                        for chunk in follow_up_response:
                            if hasattr(chunk, 'text') and chunk.text:
                                follow_up_parts.append(chunk.text)
                                self.console.print(chunk.text, end="")
                        
                        if follow_up_parts:
                            follow_up_text = "".join(follow_up_parts)
                            self.conversation_history.append(ConversationMessage("assistant", follow_up_text))
                            print()
                    except Exception as e:
                        self.console.print(f"[yellow]⚠️ Follow-up response failed: {e}[/yellow]")
                        
        except Exception as e:
            self.console.print(f"\n[red]❌ Error during conversation: {e}[/red]")
            # Try a simpler approach without function calling
            try:
                simple_response = self.model.generate_content(user_input)
                self.console.print(f"\n[blue]AI Response:[/blue] {simple_response.text}")
                self.conversation_history.append(ConversationMessage("assistant", simple_response.text))
            except Exception as simple_e:
                self.console.print(f"[red]❌ Simple fallback also failed: {simple_e}[/red]")

    def add_file_to_context(self, file_path: str):
        """Add a file or directory to the conversation context."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                self.console.print(f"[red]❌ Path {file_path} does not exist[/red]")
                return
            
            if path.is_file():
                result = read_local_file(str(path))
                if "error" in result:
                    self.console.print(f"[red]❌ {result['error']}[/red]")
                else:
                    content = f"File: {result['file_path']}\n```\n{result['content']}\n```"
                    self.conversation_history.append(ConversationMessage("system", content))
                    self.console.print(f"[green]✅ Added {path} to context[/green]")
            
            elif path.is_dir():
                added_count = 0
                for file_path in path.rglob("*"):
                    if file_path.is_file() and is_text_file(file_path):
                        try:
                            result = read_local_file(str(file_path))
                            if "success" in result:
                                content = f"File: {result['file_path']}\n```\n{result['content']}\n```"
                                self.conversation_history.append(ConversationMessage("system", content))
                                added_count += 1
                        except Exception:
                            continue
                
                self.console.print(f"[green]✅ Added {added_count} files from {path} to context[/green]")
                
        except Exception as e:
            self.console.print(f"[red]❌ Error adding {file_path} to context: {e}[/red]")

    def run_interactive_loop(self):
        """Run the main interactive loop."""
        completer = WordCompleter(['/add', '/exit', '/quit', '/help', '/clear'], ignore_case=True)
        
        try:
            while True:
                try:
                    user_input = prompt(
                        "🤖 gemini-engineer> ",
                        history=self.history,
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=completer
                    ).strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle commands
                    if user_input.lower() in ['/exit', '/quit']:
                        self.console.print("[yellow]👋 Goodbye![/yellow]")
                        break
                    
                    elif user_input.lower() == '/help':
                        self.display_welcome_banner()
                        continue
                    
                    elif user_input.lower() == '/clear':
                        self.conversation_history.clear()
                        self.console.print("[green]✅ Conversation history cleared[/green]")
                        continue
                    
                    elif user_input.startswith('/add '):
                        file_path = user_input[5:].strip()
                        self.add_file_to_context(file_path)
                        continue
                    
                    # Process regular user input
                    self.stream_gemini_response(user_input)
                    
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Use /exit or /quit to exit[/yellow]")
                    continue
                except EOFError:
                    self.console.print("\n[yellow]👋 Goodbye![/yellow]")
                    break
                    
        except Exception as e:
            self.console.print(f"[red]❌ Fatal error: {e}[/red]")

def main():
    """Main application entry point."""
    app = GeminiEngineer()
    app.display_welcome_banner()
    app.run_interactive_loop()

if __name__ == "__main__":
    main() 