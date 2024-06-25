import os
import re
import ast
from pathlib import Path

def extract_info_from_file(file_path):
    """
    Extracts relevant information (docstrings, functions, classes) from a Python file,
    and content for CSS and JavaScript files, while ignoring specified file types.
    
    Args:
        file_path (str): The full path to the file.
        
    Returns:
        dict: A dictionary containing the extracted information.
    """
    ignored_extensions = ['.gitattributes', '.gitignore', 'LICENSE', '.md', '.txt', '.db', '.pdf']
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() in ignored_extensions:
        return {}  # Return an empty dictionary for ignored files
    
    info_dict = {'type': file_extension}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.endswith('.py'):
                tree = ast.parse(file.read(), filename=file_path)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        name = node.name
                        docstring = ast.get_docstring(node)
                        if docstring:
                            info_dict[name] = docstring.strip()
                        else:
                            info_dict[name] = "No docstring found."
            elif file_path.endswith(('.css', '.js')):
                content = file.read()
                info_dict['content'] = content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return info_dict

def generate_documentation_md(directory_path, output_file):
    """
    Generates a Markdown file containing documentation for all files in a directory,
    ignoring specified directories and file types.
    
    Args:
        directory_path (str): The path of the directory containing the files.
        output_file (str): The path of the output Markdown file.
    """
    excluded_dirs = [".", "venv", ".env_win", ".git", "__pycache__", "_data", "data", "data_lcl_pdf", "assets", "archives", "_markdown_modules_courses", "assets", "Bills GCP", "Google Cloud Skills Boost", "PPT", "Quiz", "Quiz prompts", "archives_py"]
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for root, dirs, files in os.walk(directory_path):
            # Ignore directories that start with a dot or match one of the excluded patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                info_dict = extract_info_from_file(file_path)
                if info_dict:
                    filename = os.path.basename(file)
                    md_file.write(f"# File {filename} ({info_dict['type']})\n")
                    for key, value in info_dict.items():
                        if key != 'type':
                            md_file.write(f" - **{key}** : {value}\n")
                            # md_file.write(f" - **{key}** : \n\n {value}\n")
                    md_file.write("\n")


#-------------------------#
if __name__ == "__main__":
    # Get the current directory of the script
    current_dir = Path(__file__).resolve().parent
    
    # Use current_dir as directory_path to generate the documentation
    directory_path = str(current_dir)
    output_file = "dev_documentations.md"
    generate_documentation_md(directory_path, output_file)
