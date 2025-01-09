import yaml  # Import the PyYAML library to handle YAML files
import os

def loadyaml(filepath):
    """
    Load a YAML file and return its contents as a Python dictionary.

    Parameters:
    file_path (str): The path to the YAML file.

    Returns:
    dict: Parsed contents of the YAML file.
    """
    with open(filepath, 'r') as file:  # Open the YAML file in read mode
        data = yaml.safe_load(file)  # Use safeload to parse the YAML file safely
    return data  # Return the parsed data

def describe_yaml(data, indent=0):
    """
    Recursively describe the contents of a parsed YAML object in plain English.

    Parameters:
    data (any): The parsed YAML object (could be dict, list, etc.).
    indent (int): The current indentation level for pretty printing.
    """
    if isinstance(data, dict):  # If the data is a dictionary
        for key, value in data.items():  # Iterate through the dictionary items
            if isinstance(value, list):  # If the value is a list
                print(' ' * indent + f"{key.capitalize()} contains {len(value)} items:")  # Describe the list
                for item in value:  # Iterate through the list items
                    print(' ' * (indent + 2) + f"- {item}")  # Print each item in the list
            elif isinstance(value, dict):  # If the value is another dictionary
                print(' ' * indent + f"{key.capitalize()}:")  # Print the key
                describe_yaml(value, indent + 2)  # Recursively describe the nested dictionary
            else:  # If the value is a primitive type
                print(' ' * indent + f"{key.capitalize()} is {value}")  # Describe the key-value pair
    elif isinstance(data, list):  # If the data is a list
        print(' ' * indent + f"List contains {len(data)} items:")  # Describe the list
        for item in data:  # Iterate through the list items
            print(' ' * (indent + 2) + f"- {item}")  # Print each item in the list
    else:  # If the data is a primitive type (str, int, etc.)
        print(' ' * indent + str(data))  # Print the value with indentation

def main():
    yamlfilepath = './dirname/filename.yaml'  # Path to the YAML file
    if os.path.exists(yamlfilepath):  # Check if the file exists
        yamldata = loadyaml(yamlfilepath)  # Load and parse the YAML file
        print("Parsed YAML Contents:")  # Print a header
        describe_yaml(yamldata)  # Describe the parsed YAML data
    else:
        print(f"File not found: {yamlfilepath}")  # Print an error if the file does not exist

if __name__ == '__main__':
    main()  # Call the main function to run the script
