-- ============================================================================
-- SEED DATA: Types to support SACM-based Goal Structuring Notation (GSN)
-- ============================================================================

-- Node Types
INSERT INTO NodeType (id, node_type_identifier, node_type_name, node_type_description, created_by) VALUES
('d9e50ae3-aac1-4992-8030-8d2ce049ccf5', 'G', 'Goal', 'An assertion about system properties that must be supported', 'Seed'),
('d8e6d310-92a9-433f-a95c-4f6b6bbee05b', 'S', 'Strategy', 'Reasoning approach connecting claims (ArgumentReasoning)', 'Seed'),
('4408b361-63e0-4f11-b900-67dcd4d89637', 'Sn', 'Solution', 'Solution supports the Satisfaction of each Goal', 'Seed'),
('2cc4a37d-65c6-4358-b395-d360b1d8ab3c', 'C', 'Context', 'Contextual information about the argument', 'Seed'),
('1c17d7a0-6103-4cdc-887e-1aeae0c34253', 'A', 'Assumption', 'Assumed claim that does not require support', 'Seed'),
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'J', 'Justification', 'Justification for an element of the Argument', 'Seed'),
('f1c9e5b8-9c3a-4d2e-8b0a-5e7c6f1a2b4d', 'E', 'Evidence', 'A Specific Evidence Artifact or Deliverable that supports a Solution', 'Seed');

-- Edge Types
INSERT INTO EdgeType (id, edge_type_identifier, edge_type_name, edge_type_description, created_by) VALUES
('eb66eeca-ef0e-468d-aa08-cfbfa6014c4f', '', 'SupportedBy', 'Target supports the Source', 'Seed'),
('dd7e00a2-2d25-46d8-bbc2-e427e9d87380', '', 'InContextOf', 'Provides the Context', 'Seed');

-- Node Properties

-- Reusable Property Definitions
INSERT INTO NodePropertyDefinition (
	id,
	node_property_definition_identifier,
	node_property_definition_name,
	node_property_definition_type,
	node_property_definition_description,
	created_by
) VALUES
('ca2fbe32-2d1d-425d-b733-4111fdca1a01', '', 'description', 'text', 'Narrative content/statement for argument elements', 'Seed'),
('5a75cfc6-9904-4f39-95ec-ec95a4fc43de', '', 'reference', 'text', 'Document ID or Unique Identifier for the Evidence', 'Seed'),
('5487f93f-4474-459e-a241-8101f075361e', '', 'revision', 'text', 'Revision of the Evidence (e.g. A, B, C, 00, 01)', 'Seed'),
('95732ec8-f7d0-4a47-8fb1-c2e041a7dc37', '', 'status', 'text', 'Status of the Evidence (e.g. Draft, IFR, IFI, IFC, IFU)', 'Seed'),
('08a7b12f-fb1b-440c-8bee-ab454f50aa5f', '', 'title', 'text', 'Name of the Evidence', 'Seed'),
('888a2f1f-c159-4f0c-b7ff-908e0b07144b', '', 'location', 'text', 'Location of the Evidence (SharePoint Path, DMS Reference or URL)', 'Seed');

-- Assign reusable Definitions to NodeTypes
INSERT INTO NodeTypePropertyAssignment (
	id,
	node_type_id_fk,
	node_property_definition_id_fk,
	is_required,
	sort_order,
	created_by
)
SELECT
	CASE NodeType.node_type_identifier
		WHEN 'G' THEN '8fbfbc23-53fb-401f-a5f6-3c188f9af053'
		WHEN 'S' THEN 'b7c2021b-0c90-420f-8f89-35274b2de57f'
		WHEN 'Sn' THEN '96d185b3-4add-445c-b3ac-3999d41218eb'
		WHEN 'C' THEN 'aab3e3c1-b244-4e72-9472-320ac35f2a7f'
		WHEN 'A' THEN 'dc8b520d-a5e0-4b39-a17c-144cccf57d66'
		WHEN 'J' THEN '227719d3-7cad-41f6-bd87-5847acdcfd96'
		WHEN 'E' THEN '2863898d-14ea-4c6d-8da2-aa6f30d3f8b9'
	END,
	NodeType.id,
	NodePropertyDefinition.id,
	0,
	10,
	'Seed'
FROM NodeType
JOIN NodePropertyDefinition
	ON NodePropertyDefinition.node_property_definition_name = 'description'
WHERE NodeType.node_type_identifier IN ('G', 'S', 'Sn', 'C', 'A', 'J', 'E');

INSERT INTO NodeTypePropertyAssignment (id, node_type_id_fk, node_property_definition_id_fk, is_required, sort_order, created_by)
SELECT '279de906-cf8b-4750-bf44-51f2c60628c6', NodeType.id, NodePropertyDefinition.id, 0, 20, 'Seed'
FROM NodeType
JOIN NodePropertyDefinition ON NodePropertyDefinition.node_property_definition_name = 'revision'
WHERE NodeType.node_type_identifier = 'E';

INSERT INTO NodeTypePropertyAssignment (id, node_type_id_fk, node_property_definition_id_fk, is_required, sort_order, created_by)
SELECT '53af46f7-13f5-4de0-9b59-61b2fd954f89', NodeType.id, NodePropertyDefinition.id, 0, 30, 'Seed'
FROM NodeType
JOIN NodePropertyDefinition ON NodePropertyDefinition.node_property_definition_name = 'status'
WHERE NodeType.node_type_identifier = 'E';

-- SACM Nodes G0 and Sub-goals to set out the top-level of the GSN Argument
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('9e8f8d17-6df8-4ff3-b9be-a0fca252ad69', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G0', 'The System is...', 'Seed'),
('f33d23e1-68d4-43f3-b8fd-d69d7134ed70', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G1', 'System Definition', 'Seed'),
('72d6031f-5eb1-4143-b7dd-fccead58b0f2', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G2', 'Quality Management', 'Seed'),
('bb5143ce-4f7c-4df2-89b5-1bb5a8bece10', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G3', 'Safety Management', 'Seed'),
('34e55443-64d2-4998-8dce-bf4d1526648e', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G4', 'System Integration', 'Seed'),
('2835dede-fe77-45db-9a53-e4e5b32b0cee', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G5', 'Technical Assurance', 'Seed'),
('2fb302eb-5025-4e47-b6d3-249d7a45557a', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G6', 'Issues Management', 'Seed'),
('d1e2f3a4-b5c6-7890-abcd-ef1234567890', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G7', 'Operational Readiness', 'Seed');

-- SACM Edges for G0 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('1a2b3c4d-5e6f-7890-abcd-ef1234567890', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G1'), 'Seed'),
('2b3c4d5e-6f78-90ab-cdef-1234567890ab', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G2'), 'Seed'),
('3c4d5e6f-7890-abcd-ef12-34567890abcd', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G3'), 'Seed'),
('4d5e6f78-90ab-cdef-1234-567890abcdef', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G4'), 'Seed'),
('5e6f7890-abcd-ef12-3456-7890abcdef12', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G5'), 'Seed'),
('6f7890ab-cdef-1234-5678-90abcdef1234', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G6'), 'Seed'),
('7a8b9c0d-1e2f-3456-7890-abcd12345678', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G7'), 'Seed');

-- SACM Nodes for G1 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('e1f2a3b4-c5d6-7890-abcd-ef1234567890', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G1.1', 'Goal G1.1', 'Seed');

-- SACM Edges for G1 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('c1d2e3f4-a5b6-7890-abcd-ef1234567890', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G1'), (SELECT id FROM Node WHERE node_identifier = 'G1.1'), 'Seed');

-- SACM Nodes for G2 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('f1e2d3c4-b5a6-7890-abcd-ef1234567890', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G2.1', 'Goal G2.1', 'Seed');

-- SACM Edges for G2 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('d1c2b3a4-e5f6-7890-abcd-ef1234567890', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G2'), (SELECT id FROM Node WHERE node_identifier = 'G2.1'), 'Seed');

-- SACM Nodes for G3 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('0d6ce9dd-30f6-4fe5-af8f-6a9e61f77756', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G3.1', 'Goal G3.1', 'Seed');

-- SACM Edges for G3 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('b1c2d3e4-f5a6-7890-abcd-ef1234567890', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G3'), (SELECT id FROM Node WHERE node_identifier = 'G3.1'), 'Seed');

-- SACM Nodes for G4 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('f8f8441d-f7f7-49f7-b30f-ccf35b96f5a3', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G4.1', 'Goal G4.1', 'Seed');

-- SACM Edges for G4 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('f6f3e4fa-3818-48d2-b2cc-31fc4346b4bb', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G4'), (SELECT id FROM Node WHERE node_identifier = 'G4.1'), 'Seed');

-- SACM Nodes for G5 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('4b65f5d7-7612-4ec2-b456-5fce5905c2e1', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G5.1', 'Goal G5.1', 'Seed');

-- SACM Edges for G5 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('245950b9-67e6-4e09-a68a-f60f4f8ac587', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G5'), (SELECT id FROM Node WHERE node_identifier = 'G5.1'), 'Seed');

-- SACM Nodes for G6 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('f4a1b2c3-d4e5-4f67-89ab-cdef01234567', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G6.1', 'Goal G6.1', 'Seed');

-- SACM Edges for G6 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('6bb28f31-8f9e-4d1d-8c51-2e5fa6b1d903', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G6'), (SELECT id FROM Node WHERE node_identifier = 'G6.1'), 'Seed');

-- SACM Nodes for G7 Sub-goals
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('a9b8c7d6-e5f4-4123-89ab-0fedcba98765', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G7.1', 'Goal G7.1', 'Seed');

-- SACM Edges for G7 to Sub-goals
INSERT INTO Edge (id, edge_type_id_fk, edge_name, source_node_id_fk, target_node_id_fk, created_by) VALUES
('2ac96f9a-6f4f-4f45-9d84-1b4e7e2c6a55', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), 'SupportedBy', (SELECT id FROM Node WHERE node_identifier = 'G7'), (SELECT id FROM Node WHERE node_identifier = 'G7.1'), 'Seed');