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
('eb66eeca-ef0e-468d-aa08-cfbfa6014c4f', 'SB', 'SupportedBy', 'Target supports the Source (AssertedInference)', 'system'),
('dd7e00a2-2d25-46d8-bbc2-e427e9d87380', 'ICO', 'InContextOf', 'Provides the Context (AssertedContext)', 'system');

-- SACM Node Properties

-- Properties for Goal
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT 'ca2fbe32-2d1d-425d-b733-4111fdca1a01', id, 'content', 'text', 'Goal Statement', 'system'
FROM NodeType WHERE node_type_identifier = 'G';

-- Properties for Strategy
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT 'f605ecab-728d-450e-8d8d-3716ef95f49e', id, 'content', 'text', 'Description of the Strategy', 'system'
FROM NodeType WHERE node_type_identifier = 'S';

-- Properties for Solution
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT 'fd096fa0-dc77-40d1-8102-e23cb6dca754', id, 'content', 'text', 'Description of the Solution', 'system'
FROM NodeType WHERE node_type_identifier = 'Sn';

-- Properties for Context
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT '48ce4234-7c35-4aca-9244-54048e99e425', id, 'content', 'text', 'Description of the Context', 'system'
FROM NodeType WHERE node_type_identifier = 'C';

-- Properties for Assumption
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT 'a518919a-8f28-420c-8f82-a6ceada65c0f', id, 'content', 'text', 'Description of the Assumption', 'system'
FROM NodeType WHERE node_type_identifier = 'A';

-- Properties for Justification
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT '29575bb0-2016-44f3-a13c-8506f2f44a87', id, 'content', 'text', 'Description of the Justification', 'system'
FROM NodeType WHERE node_type_identifier = 'J';

-- Properties for Evidence
INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_is_required, node_property_definition_description, created_by
)
SELECT '5a75cfc6-9904-4f39-95ec-ec95a4fc43de', id, 'reference', 'string', 1,
       'Document ID or Unique Identifier for the Evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_is_required, node_property_definition_description, created_by
)
SELECT '5487f93f-4474-459e-a241-8101f075361e', id, 'version', 'string', 0,
       'Revision of the Evidence (e.g. A, B, C, 00, 01)', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_is_required, node_property_definition_description, created_by
)
SELECT '95732ec8-f7d0-4a47-8fb1-c2e041a7dc37', id, 'status', 'string', 0,
       'Status of the Evidence (e.g. Draft, IFR, IFI, IFC, IFU)', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_description, created_by
)
SELECT '08a7b12f-fb1b-440c-8bee-ab454f50aa5f', id, 'name', 'string', 'Name of the Evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_is_required, node_property_definition_description, created_by
)
SELECT '888a2f1f-c159-4f0c-b7ff-908e0b07144b', id, 'location', 'string', 0,
       'Location of the Evidence (SharePoint Path, DMS Reference or URL)', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

INSERT INTO NodePropertyDefinition (
    id, node_type_id_fk, node_property_definition_name, node_property_definition_type,
    node_property_definition_is_required, node_property_definition_description, created_by
)
SELECT '83c1719f-2f1b-4aa0-8b21-89358a00da1f', id, 'content', 'text', 0,
       'Description of the Evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'E';

-- SACM Nodes
INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name, created_by) VALUES
('9e8f8d17-6df8-4ff3-b9be-a0fca252ad69', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G0', 'The System is...', 'system'),
('f33d23e1-68d4-43f3-b8fd-d69d7134ed70', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G1', 'Goal 1', 'system'),
('72d6031f-5eb1-4143-b7dd-fccead58b0f2', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G2', 'Goal 2', 'system'),
('bb5143ce-4f7c-4df2-89b5-1bb5a8bece10', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G3', 'Goal 3', 'system'),
('34e55443-64d2-4998-8dce-bf4d1526648e', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G4', 'Goal 4', 'system'),
('2835dede-fe77-45db-9a53-e4e5b32b0cee', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G5', 'Goal 5', 'system'),
('2fb302eb-5025-4e47-b6d3-249d7a45557a', (SELECT id FROM NodeType WHERE node_type_identifier = 'G'), 'G6', 'Goal 6', 'system');

-- SACM Edges
INSERT INTO Edge (id, edge_type_id_fk, source_node_id_fk, target_node_id_fk, created_by) VALUES
('1a2b3c4d-5e6f-7890-abcd-ef1234567890', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G1'), 'system'),
('2b3c4d5e-6f78-90ab-cdef-1234567890ab', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G2'), 'system'),
('3c4d5e6f-7890-abcd-ef12-34567890abcd', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G3'), 'system'),
('4d5e6f78-90ab-cdef-1234-567890abcdef', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G4'), 'system'),
('5e6f7890-abcd-ef12-3456-7890abcdef12', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G5'), 'system'),
('6f7890ab-cdef-1234-5678-90abcdef1234', (SELECT id FROM EdgeType WHERE edge_type_name = 'SupportedBy'), (SELECT id FROM Node WHERE node_identifier = 'G0'), (SELECT id FROM Node WHERE node_identifier = 'G6'), 'system');
