import yaml
import os
import networkx as nx

def load_yaml(file_path):
    """Load and parse a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_python_file(file_path):
    """Load and read the content of a Python file."""
    with open(file_path, 'r') as file:
        return file.read()

def resolve_references(data, base_path):
    """Resolve references to other YAML or Python files."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.endswith(('.yaml', '.yml', '.py')):
                ref_path = os.path.join(base_path, value)
                if os.path.exists(ref_path):
                    if ref_path.endswith(('.yaml', '.yml')):
                        data[key] = load_yaml(ref_path)
                    elif ref_path.endswith('.py'):
                        # Load Python file content
                        data[key] = load_python_file(ref_path)
            elif isinstance(value, (dict, list)):
                resolve_references(value, base_path)
    elif isinstance(data, list):
        for item in data:
            resolve_references(item, base_path)

def build_graph(data, graph, parent_node=None):
    """Build a graph from the YAML data."""
    if isinstance(data, dict):
        for key, value in data.items():
            node = f"{key}"
            graph.add_node(node)
            if parent_node:
                graph.add_edge(parent_node, node)
            build_graph(value, graph, node)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            node = f"List[{index}]"
            graph.add_node(node)
            if parent_node:
                graph.add_edge(parent_node, node)
            build_graph(item, graph, node)
    else:
        node = f"{data}" if len(str(data)) < 50 else f"{str(data)[:50]}..."  # Truncate long text
        graph.add_node(node)
        if parent_node:
            graph.add_edge(parent_node, node)

def export_to_dot(file_path, output_dot_path):
    """Export the YAML file structure as a DOT file."""
    base_path = os.path.dirname(file_path)
    data = load_yaml(file_path)
    resolve_references(data, base_path)

    graph = nx.DiGraph()
    build_graph(data, graph)

    # Export the graph to a DOT file
    nx.drawing.nx_pydot.write_dot(graph, output_dot_path)
    print(f"Graph exported to {output_dot_path}")

if __name__ == "__main__":
    yaml_file_path = "example.yaml"  # Replace with your YAML file path
    output_dot_path = "output_graph.dot"  # Output DOT file path
    export_to_dot(yaml_file_path, output_dot_path)
