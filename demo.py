#!/usr/bin/env python3
"""
Simple demo script for Gemini Engineer
This demonstrates the core functionality without requiring all dependencies.
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_file_operations():
    """Demonstrate file operations without external dependencies."""
    print("🤖 Gemini Engineer - Core Functionality Demo")
    print("=" * 50)
    
    # Import only the core functions we need
    try:
        from main import (
            normalize_path, 
            is_text_file, 
            read_local_file, 
            create_file, 
            edit_file,
            list_directory
        )
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return
    
    print("\n📂 Testing file operations...")
    
    # Test 1: Create a file
    print("\n1. Creating test file...")
    result = create_file("demo_test.txt", "Hello from Gemini Engineer!\nThis is a test file.")
    if result.get("success"):
        print(f"   ✅ {result['message']}")
    else:
        print(f"   ❌ {result.get('error', 'Unknown error')}")
    
    # Test 2: Read the file
    print("\n2. Reading test file...")
    result = read_local_file("demo_test.txt")
    if result.get("success"):
        print(f"   ✅ Read {result['size']} characters")
        print(f"   📄 Content preview: {result['content'][:50]}...")
    else:
        print(f"   ❌ {result.get('error', 'Unknown error')}")
    
    # Test 3: Edit the file
    print("\n3. Editing test file...")
    result = edit_file("demo_test.txt", "Hello from Gemini Engineer!", "Greetings from Gemini Engineer!")
    if result.get("success"):
        print(f"   ✅ {result['message']}")
    else:
        print(f"   ❌ {result.get('error', 'Unknown error')}")
    
    # Test 4: List directory
    print("\n4. Listing current directory...")
    result = list_directory(".")
    if result.get("success"):
        print(f"   ✅ Found {result['count']} items")
        for item in result['items'][:5]:  # Show first 5 items
            print(f"   📁 {item['name']} ({item['type']})")
        if result['count'] > 5:
            print(f"   ... and {result['count'] - 5} more items")
    else:
        print(f"   ❌ {result.get('error', 'Unknown error')}")
    
    # Test 5: Path validation
    print("\n5. Testing security features...")
    try:
        dangerous_path = normalize_path("../../../etc/passwd")
        print(f"   ❌ Security check failed - dangerous path allowed: {dangerous_path}")
    except ValueError as e:
        print(f"   ✅ Security check passed - dangerous path blocked: {e}")
    
    # Test 6: File type detection
    print("\n6. Testing file type detection...")
    if Path("demo_test.txt").exists():
        is_text = is_text_file(Path("demo_test.txt"))
        print(f"   ✅ demo_test.txt is text file: {is_text}")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    try:
        os.remove("demo_test.txt")
        print("   ✅ Test file removed")
    except FileNotFoundError:
        print("   ✅ Test file already removed")
    
    print("\n🎉 Demo completed successfully!")
    print("\nTo use the full interactive application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up your API key in .env file")
    print("3. (Optional) Set GEMINI_MODEL in .env to choose a different model")
    print("4. Run: python main.py")

if __name__ == "__main__":
    demo_file_operations() 