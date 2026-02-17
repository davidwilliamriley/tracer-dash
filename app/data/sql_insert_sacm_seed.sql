-- ============================================================================
-- SEED DATA: SACM Types to support SACM-based Goal Structuring Notation (GSN)
-- ============================================================================

-- SACM Node Types
INSERT INTO NodeType (id, node_type_identifier, node_type_name, node_type_description, created_by) VALUES
('d9e50ae3-aac1-4992-8030-8d2ce049ccf5', 'G', 'Goal', 'An assertion about system properties that must be supported', 'system'),
('d8e6d310-92a9-433f-a95c-4f6b6bbee05b', 'S', 'Strategy', 'Reasoning approach connecting claims (ArgumentReasoning)', 'system'),
('4408b361-63e0-4f11-b900-67dcd4d89637', 'Sn', 'Solution', 'Supporting information, artifacts, or test results', 'system'),
('2cc4a37d-65c6-4358-b395-d360b1d8ab3c', 'C', 'Context', 'Contextual information about the argument', 'system'),
('1c17d7a0-6103-4cdc-887e-1aeae0c34253', 'A', 'Assumption', 'Assumed claim that does not require support', 'system'),
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'J', 'Justification', 'Justification for an element of the Argument', 'system'),
('f1c9e5b8-9c3a-4d2e-8b0a-5e7c6f1a2b4d', 'E', 'Evidence', 'Specific Evidence (Deliverable) relevant to the Solution', 'system');

-- SACM Edge Types
INSERT INTO EdgeType (id, edge_type_identifier, edge_type_name, edge_type_description, created_by) VALUES
('eb66eeca-ef0e-468d-aa08-cfbfa6014c4f', '', 'SupportedBy', 'Target supports the Source (AssertedInference)', 'system'),
('dd7e00a2-2d25-46d8-bbc2-e427e9d87380', '', 'InContextOf', 'Provides the Context (AssertedContext)', 'system'),

-- SACM Node Properties

-- Properties for Goal
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Goal Statement', 'system'
FROM NodeType WHERE node_type_identifier = 'Goal';

-- Properties for Strategy
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the Strategy', 'system'
FROM NodeType WHERE node_type_identifier = 'Strategy';

-- Properties for Solution
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the Solution', 'system'
FROM NodeType WHERE node_type_identifier = 'Solution';

-- Properties for Context
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the Context', 'system'
FROM NodeType WHERE node_type_identifier = 'Context';

-- Properties for Assumption
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the Assumption', 'system' 
FROM NodeType WHERE node_type_identifier = 'Assumption';

-- Properties for Justification
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the Justification', 'system'
FROM NodeType WHERE node_type_identifier = 'Justification';

-- Properties for Evidence
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'reference', 'string', 1, 'Document ID or Unique Identifier for the Evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'version', 'string', 0, 'Revision of the Evidence (e.g. A, B, C, 00, 01)', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'status', 'string', 0, 'Status of the Evidence (e.g. Draft, Issued for Review (IFR), Issued for Information (IFI), Issued for Construction (IFC), Issued for Use (IFU))', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by) 
SELECT id, 'name', 'string', 'Name of the Evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'location', 'string', 0, 'Location of the Evidence (SharePoint Path, DMS Reference or URL)', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'content', 'text', 0, 'Description of the Evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

-- SACM Nodes
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('9e8f8d17-6df8-4ff3-b9be-a0fca252ad69', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G0', 'The System is...', 'system'),
('f33d23e1-68d4-43f3-b8fd-d69d7134ed70', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G1', 'Goal', 'system'),
('72d6031f-5eb1-4143-b7dd-fccead58b0f2', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G2', 'Goal', 'system'),
('bb5143ce-4f7c-4df2-89b5-1bb5a8bece10', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G3', 'Goal', 'system'),
('34e55443-64d2-4998-8dce-bf4d1526648e', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G4', 'Goal', 'system'),
('2835dede-fe77-45db-9a53-e4e5b32b0cee', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G5', 'Goal', 'system'),
('2fb302eb-5025-4e47-b6d3-249d7a45557a', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G6', 'Goal', 'system');

-- SACM Edges
INSERT INTO Edge (id, edge_type_id_fk, source_node_id_fk, target_node_id_fk, created_by) VALUES
('1a2b3c4d-5e6f-7890-abcd-ef1234567890', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G1'), 'system'),
('2b3c4d5e-6f78-90ab-cdef-1234567890ab', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G2'), 'system'),
('3c4d5e6f-7890-abcd-ef12-34567890abcd', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G3'), 'system'),
('4d5e6f78-90ab-cdef-1234-567890abcdef', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G4'), 'system'),
('5e6f7890-abcd-ef12-3456-7890abcdef12', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G5'), 'system'),
('6f7890ab-cdef-1234-5678-90abcdef1234', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G6'), 'system');