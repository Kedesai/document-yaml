import os
import re

def extract_csharp_documentation(file_path):
    """Extract classes, methods, and XML comments from a C# file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to match XML comments
    xml_comment_pattern = re.compile(r'///\s*(<summary>.*?</summary>)', re.DOTALL)
    # Regex to match class definitions
    class_pattern = re.compile(r'class\s+(\w+)\s*{')
    # Regex to match method definitions
    method_pattern = re.compile(r'(public|private|protected|internal)\s+(\w+)\s+(\w+)\s*\(([^)]*)\)')

    # Extract XML comments
    xml_comments = xml_comment_pattern.findall(content)
    # Extract class definitions
    classes = class_pattern.findall(content)
    # Extract method definitions
    methods = method_pattern.findall(content)

    return {
        'file_path': file_path,
        'xml_comments': xml_comments,
        'classes': classes,
        'methods': methods,
    }

def generate_markdown_documentation(data, output_file):
    """Generate Markdown documentation from extracted data."""
    with open(output_file, 'w') as md_file:
        md_file.write(f"# Documentation for {data['file_path']}\n\n")

        # Write classes
        if data['classes']:
            md_file.write("## Classes\n\n")
            for class_name in data['classes']:
                md_file.write(f"### `{class_name}`\n\n")

        # Write methods
        if data['methods']:
            md_file.write("## Methods\n\n")
            for access_modifier, return_type, method_name, parameters in data['methods']:
                md_file.write(f"### `{return_type} {method_name}({parameters})`\n")
                md_file.write(f"- **Access Modifier**: `{access_modifier}`\n")
                md_file.write(f"- **Parameters**: `{parameters}`\n\n")

        # Write XML comments
        if data['xml_comments']:
            md_file.write("## XML Comments\n\n")
            for comment in data['xml_comments']:
                md_file.write(f"```xml\n{comment}\n```\n\n")

def document_net_code(directory, output_file):
    """Document all C# files in a directory."""
    documentation_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                data = extract_csharp_documentation(file_path)
                documentation_data.append(data)

    # Generate Markdown documentation
    generate_markdown_documentation({'file_path': directory, 'xml_comments': [], 'classes': [], 'methods': []}, output_file)
    for data in documentation_data:
        generate_markdown_documentation(data, output_file)

if __name__ == "__main__":
    # Specify the directory containing .NET code and the output Markdown file
    code_directory = "path/to/your/csharp/code"
    output_markdown_file = "documentation.md"

    # Generate documentation
    document_net_code(code_directory, output_markdown_file)
    print(f"Documentation generated at {output_markdown_file}")
