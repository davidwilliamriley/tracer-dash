SELECT 
    edges.id,
	edges.identifier,
    source_node.name AS source_name,
    edge_types.name AS edge_name,
    target_node.name AS target_name
FROM 
    edges
JOIN nodes AS source_node ON source_node.id = edges.source_node_id
JOIN edge_types ON edge_types.id = edges.edge_type_id
JOIN nodes AS target_node ON target_node.id = edges.target_node_id;