-- ============================================================================
-- SEED DATA: SACM Types to support SACM-based Goal Structuring Notation (GSN)
-- ============================================================================

-- SACM Node Types
INSERT INTO NodeType (id, node_type_identifier, node_type_name, node_type_description, created_by) VALUES
('d9e50ae3-aac1-4992-8030-8d2ce049ccf5', 'Goal', 'An assertion about system properties that must be supported', 'system'),
('d8e6d310-92a9-433f-a95c-4f6b6bbee05b', 'Strategy', 'Reasoning approach connecting claims (ArgumentReasoning)', 'system'),
('4408b361-63e0-4f11-b900-67dcd4d89637', 'Solution', 'Supporting information, artifacts, or test results', 'system'),
('2cc4a37d-65c6-4358-b395-d360b1d8ab3c', 'Context', 'Contextual information about the argument', 'system'),
('1c17d7a0-6103-4cdc-887e-1aeae0c34253', 'Assumption', 'Assumed claim that does not require support', 'system'),
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Justification', 'Justification for an argument element', 'system'),
('f1c9e5b8-9c3a-4d2e-8b0a-5e7c6f1a2b4d', 'Artefact', 'Physical or digital artifact relevant to the argument', 'system');

-- SACM Edge Types
INSERT INTO EdgeType (id, edge_type_identifier, edge_type_name, edge_type_description, created_by) VALUES
('eb66eeca-ef0e-468d-aa08-cfbfa6014c4f', 'sacm:SupportedBy', 'SupportedBy', 'Target supports the Source (AssertedInference)', 'system'),
('dd7e00a2-2d25-46d8-bbc2-e427e9d87380', 'sacm:InContextOf', 'InContextOf', 'Provides the Context (AssertedContext)', 'system'),

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

-- Properties for Artefact
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'reference', 'string', 1, 'Document ID or Unique Identifier for the Artefact', 'system'
FROM NodeType WHERE node_type_identifier = 'Artefact';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'version', 'string', 0, 'Revision of the Artefact (e.g. A, B, C, 00, 01)', 'system'
FROM NodeType WHERE node_type_identifier = 'Artefact';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'status', 'string', 0, 'Status of the Artefact (e.g. Draft, Issued for Review (IFR), Issued for Information (IFI), Issued for Construction (IFC), Issued for Use (IFU))', 'system'
FROM NodeType WHERE node_type_identifier = 'Artefact';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by) 
SELECT id, 'name', 'string', 'Name of the Artefact', 'system'
FROM NodeType WHERE node_type_identifier = 'Artefact';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'location', 'string', 0, 'Location of the Artefact (SharePoint Path, DMS Reference or URL)', 'system'
FROM NodeType WHERE node_type_identifier = 'Artefact';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, is_required, node_property_description, created_by)
SELECT id, 'content', 'text', 0, 'Description of the Artefact', 'system'
FROM NodeType WHERE node_type_identifier = 'Artefact';
