# load_graph.py
import sqlite3
import networkx as nx

print("Connecting to database...")
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("Loading graph from database...")
graph = nx.DiGraph()  # Using directed graph since edges have source/target

# Load all nodes with their attributes
print("Loading nodes...")
cursor.execute("SELECT id, identifier, name, description FROM nodes")
for node_id, identifier, name, description in cursor.fetchall():
    graph.add_node(
        node_id,
        identifier=identifier,
        name=name,
        description=description
    )

# Load all edges with their attributes
print("Loading edges...")
cursor.execute("""
    SELECT e.id, e.identifier, e.source_node_id, e.target_node_id, 
           e.weight, e.description, et.name as edge_type_name
    FROM edges e
    LEFT JOIN edge_types et ON e.edge_type_id = et.id
""")
for edge_id, identifier, source, target, weight, description, edge_type in cursor.fetchall():
    graph.add_edge(
        source,
        target,
        edge_id=edge_id,
        identifier=identifier,
        weight=weight,
        description=description,
        edge_type=edge_type
    )

print(f"\nGraph loaded successfully!")
print(f"  Nodes: {len(graph.nodes)}")
print(f"  Edges: {len(graph.edges)}")

# Helper functions
def get_node(node_id):
    """Get node attributes by ID"""
    return graph.nodes[node_id]

def get_node_by_identifier(identifier):
    """Find node by identifier"""
    for node_id, data in graph.nodes(data=True):
        if data.get('identifier') == identifier:
            return node_id, data
    return None

def show_neighbors(node_id, direction='out'):
    """Show neighbors of a node
    direction: 'out' (successors), 'in' (predecessors), or 'both'
    """
    if direction == 'out':
        return list(graph.successors(node_id))
    elif direction == 'in':
        return list(graph.predecessors(node_id))
    else:
        return list(graph.successors(node_id)) + list(graph.predecessors(node_id))

def get_edge_info(source, target):
    """Get edge attributes between two nodes"""
    return graph.edges[source, target]

def find_nodes_by_name(name_part):
    """Find nodes whose name contains the given string"""
    results = []
    for node_id, data in graph.nodes(data=True):
        if data.get('name') and name_part.lower() in data['name'].lower():
            results.append((node_id, data))
    return results

def show_node_edges(node_id):
    """Show all edges connected to a node"""
    print(f"\nOutgoing edges from {get_node(node_id).get('name', node_id)}:")
    for target in graph.successors(node_id):
        edge_data = graph.edges[node_id, target]
        print(f"  -> {get_node(target).get('name', target)} ({edge_data.get('edge_type', 'unknown')})")
    
    print(f"\nIncoming edges to {get_node(node_id).get('name', node_id)}:")
    for source in graph.predecessors(node_id):
        edge_data = graph.edges[source, node_id]
        print(f"  <- {get_node(source).get('name', source)} ({edge_data.get('edge_type', 'unknown')})")

print("\n" + "="*60)
print("Ready! Available commands:")
print("  graph                    - The NetworkX DiGraph object")
print("  conn, cursor             - Database connection and cursor")
print("  get_node(node_id)        - Get node attributes")
print("  get_node_by_identifier(identifier) - Find node by identifier")
print("  show_neighbors(node_id)  - Show connected nodes")
print("  get_edge_info(src, tgt)  - Get edge attributes")
print("  find_nodes_by_name(text) - Search nodes by name")
print("  show_node_edges(node_id) - Display all edges for a node")
print("="*60)

# Quick example
print("\nQuick example - Railway Activities node:")
railway = get_node_by_identifier('Ac_80_50')
if railway:
    print(f"  ID: {railway[0]}")
    print(f"  Name: {railway[1]['name']}")
    print(f"  Successors: {len(list(graph.successors(railway[0])))}")
