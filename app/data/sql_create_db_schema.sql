-- ============================================================================
-- TRACER: Graph Database Schema
-- SQLite Implementation
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ============================================================================
-- TYPE LAYER: Define NodeTypes and EdgeTypes
-- ============================================================================

CREATE TABLE NodeType (
    id TEXT PRIMARY KEY,
    node_type_identifier TEXT NOT NULL UNIQUE,
    node_type_name TEXT NOT NULL,
    node_type_description TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_nodetype_identifier ON NodeType(node_type_identifier);
CREATE INDEX idx_nodetype_name ON NodeType(node_type_name);

CREATE TABLE EdgeType (
    id TEXT PRIMARY KEY,
    edge_type_identifier TEXT NOT NULL UNIQUE,
    edge_type_name TEXT NOT NULL,
    edge_type_description TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_edgetype_identifier ON EdgeType(edge_type_identifier);
CREATE INDEX idx_edgetype_name ON EdgeType(edge_type_name);

-- ============================================================================
-- PROPERTY DEFINITION LAYER: Define NodePropertyDefinitions and EdgePropertyDefinitions
-- ============================================================================

CREATE TABLE NodePropertyDefinition (
    id TEXT PRIMARY KEY,
    node_type_id_fk TEXT NOT NULL,
    node_property_definition_name TEXT NOT NULL,
    node_property_definition_type TEXT NOT NULL CHECK(node_property_definition_type IN ('string', 'integer', 'float', 'boolean', 'text', 'date', 'datetime')),
    node_property_definition_is_required BOOLEAN DEFAULT 0,
    node_property_definition_default_value TEXT,
    node_property_definition_description TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (node_type_id_fk) REFERENCES NodeType(id) ON DELETE CASCADE,
    UNIQUE(node_type_id_fk, node_property_definition_name)
);

CREATE INDEX idx_node_property_definition_type ON NodePropertyDefinition(node_type_id_fk);
CREATE INDEX idx_node_property_definition_name ON NodePropertyDefinition(node_property_definition_name);

CREATE TABLE EdgePropertyDefinition (
    id TEXT PRIMARY KEY,
    edge_type_id_fk TEXT NOT NULL,
    edge_property_definition_name TEXT NOT NULL,
    edge_property_definition_type TEXT NOT NULL CHECK(edge_property_definition_type IN ('string', 'integer', 'float', 'boolean', 'text', 'date', 'datetime')),
    edge_property_definition_is_required BOOLEAN DEFAULT 0,
    edge_property_definition_default_value TEXT,
    edge_property_definition_description TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (edge_type_id_fk) REFERENCES EdgeType(id) ON DELETE CASCADE,
    UNIQUE(edge_type_id_fk, edge_property_definition_name)
);

CREATE INDEX idx_edge_property_definition_type ON EdgePropertyDefinition(edge_type_id_fk);
CREATE INDEX idx_edge_property_definition_name ON EdgePropertyDefinition(edge_property_definition_name);

-- ============================================================================
-- INSTANCE LAYER: Define Nodes and Edges
-- ============================================================================

CREATE TABLE Node (
    id TEXT PRIMARY KEY,
    node_type_id_fk TEXT NOT NULL,
    node_identifier TEXT NOT NULL UNIQUE,
    node_name TEXT NOT NULL UNIQUE,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (node_type_id_fk) REFERENCES NodeType(id) ON DELETE RESTRICT
);

CREATE INDEX idx_node_type ON Node(node_type_id_fk);
CREATE INDEX idx_node_name ON Node(node_name);

CREATE TABLE Edge (
    id TEXT PRIMARY KEY,
    edge_type_id_fk TEXT NOT NULL,
    source_node_id_fk TEXT NOT NULL,
    target_node_id_fk TEXT NOT NULL,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (edge_type_id_fk) REFERENCES EdgeType(id) ON DELETE RESTRICT,
    FOREIGN KEY (source_node_id_fk) REFERENCES Node(id) ON DELETE CASCADE,
    FOREIGN KEY (target_node_id_fk) REFERENCES Node(id) ON DELETE CASCADE,
    
    CHECK(source_node_id_fk != target_node_id_fk),
    UNIQUE(edge_type_id_fk, source_node_id_fk, target_node_id_fk)
);

CREATE INDEX idx_edge_type ON Edge(edge_type_id_fk);
CREATE INDEX idx_edge_source ON Edge(source_node_id_fk);
CREATE INDEX idx_edge_target ON Edge(target_node_id_fk);
CREATE INDEX idx_edge_source_target ON Edge(source_node_id_fk, target_node_id_fk);

-- ============================================================================
-- PROPERTY VALUE LAYER: Define NodePropertyValues and EdgePropertyValues
-- ============================================================================

CREATE TABLE NodePropertyValue (
    id TEXT PRIMARY KEY,
    node_id_fk TEXT NOT NULL,
    node_property_definition_id_fk TEXT NOT NULL,
    node_property_value TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (node_id_fk) REFERENCES Node(id) ON DELETE CASCADE,
    FOREIGN KEY (node_property_definition_id_fk) REFERENCES NodePropertyDefinition(id) ON DELETE CASCADE,
    
    UNIQUE(node_id_fk, node_property_definition_id_fk)
);

CREATE INDEX idx_node_property_value_node ON NodePropertyValue(node_id_fk);
CREATE INDEX idx_node_property_value_definition ON NodePropertyValue(node_property_definition_id_fk);

-- Trigger to ensure Property Definition matches Node Type (INSERT)
CREATE TRIGGER validate_node_property_type_insert
BEFORE INSERT ON NodePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition does not match NodeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Node
        JOIN NodePropertyDefinition ON NodePropertyDefinition.id = NEW.node_property_definition_id_fk
        WHERE Node.id = NEW.node_id_fk
          AND Node.node_type_id_fk = NodePropertyDefinition.node_type_id_fk
    );
END;

-- Trigger to ensure Property Definition matches Node Type (UPDATE)
CREATE TRIGGER validate_node_property_type_update
BEFORE UPDATE ON NodePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition does not match NodeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Node
        JOIN NodePropertyDefinition ON NodePropertyDefinition.id = NEW.node_property_definition_id_fk
        WHERE Node.id = NEW.node_id_fk
          AND Node.node_type_id_fk = NodePropertyDefinition.node_type_id_fk
    );
END;

CREATE TABLE EdgePropertyValue (
    id TEXT PRIMARY KEY,
    edge_id_fk TEXT NOT NULL,
    edge_property_definition_id_fk TEXT NOT NULL,
    edge_property_value TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (edge_id_fk) REFERENCES Edge(id) ON DELETE CASCADE,
    FOREIGN KEY (edge_property_definition_id_fk) REFERENCES EdgePropertyDefinition(id) ON DELETE CASCADE,
    
    UNIQUE(edge_id_fk, edge_property_definition_id_fk)
);

CREATE INDEX idx_edge_property_value_edge ON EdgePropertyValue(edge_id_fk);
CREATE INDEX idx_edge_property_value_definition ON EdgePropertyValue(edge_property_definition_id_fk);

-- Trigger to ensure Property Definition matches Edge Type (INSERT)
CREATE TRIGGER validate_edge_property_type_insert
BEFORE INSERT ON EdgePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition does not match EdgeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Edge
        JOIN EdgePropertyDefinition ON EdgePropertyDefinition.id = NEW.edge_property_definition_id_fk
        WHERE Edge.id = NEW.edge_id_fk
          AND Edge.edge_type_id_fk = EdgePropertyDefinition.edge_type_id_fk
    );
END;

-- Trigger to ensure Property Definition matches Edge Type (UPDATE)
CREATE TRIGGER validate_edge_property_type_update
BEFORE UPDATE ON EdgePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition does not match EdgeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Edge
        JOIN EdgePropertyDefinition ON EdgePropertyDefinition.id = NEW.edge_property_definition_id_fk
        WHERE Edge.id = NEW.edge_id_fk
          AND Edge.edge_type_id_fk = EdgePropertyDefinition.edge_type_id_fk
    );
END;

-- ============================================================================
-- AUTO-UPDATE TRIGGERS: Set modified_on on UPDATE
-- ============================================================================

CREATE TRIGGER update_node_modified_on
AFTER UPDATE ON Node
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE Node SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_edge_modified_on
AFTER UPDATE ON Edge
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE Edge SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_node_property_value_modified_on
AFTER UPDATE ON NodePropertyValue
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE NodePropertyValue SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_edge_property_value_modified_on
AFTER UPDATE ON EdgePropertyValue
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE EdgePropertyValue SET modified_on = datetime('now') WHERE id = NEW.id;
END;

-- ============================================================================
-- VIEWS: Convenient queries
-- ============================================================================

-- -- View: Complete node information with properties
-- CREATE VIEW v_NodesWithProperties AS
-- SELECT 
--     Node.id AS node_id,
--     Node.node_name,
--     NodeType.node_type_name,
--     NodeType.node_type_identifier,
--     NodePropertyDefinition.node_property_definition_name,
--     NodePropertyDefinition.node_property_definition_type,
--     NodePropertyValue.node_property_value,
--     Node.modified_by,
--     Node.modified_on
-- FROM Node
-- JOIN NodeType ON Node.node_type_id_fk = NodeType.id
-- LEFT JOIN NodePropertyValue ON NodePropertyValue.node_id_fk = Node.id
-- LEFT JOIN NodePropertyDefinition ON NodePropertyValue.node_property_definition_id_fk = NodePropertyDefinition.id;

-- -- View: Complete edge information with properties
-- CREATE VIEW v_EdgesWithProperties AS
-- SELECT 
--     Edge.id AS edge_id,
--     EdgeType.edge_type_name,
--     EdgeType.edge_type_identifier,
--     SourceNode.node_name AS source_node_name,
--     TargetNode.node_name AS target_node_name,
--     EdgePropertyDefinition.edge_property_definition_name,
--     EdgePropertyDefinition.edge_property_definition_type,
--     EdgePropertyValue.edge_property_value,
--     Edge.modified_by,
--     Edge.modified_on
-- FROM Edge
-- JOIN EdgeType ON Edge.edge_type_id_fk = EdgeType.id
-- JOIN Node AS SourceNode ON Edge.source_node_id_fk = SourceNode.id
-- JOIN Node AS TargetNode ON Edge.target_node_id_fk = TargetNode.id
-- LEFT JOIN EdgePropertyValue ON EdgePropertyValue.edge_id_fk = Edge.id
-- LEFT JOIN EdgePropertyDefinition ON EdgePropertyValue.edge_property_definition_id_fk = EdgePropertyDefinition.id;

-- -- View: Node type schemas (what properties each type has)
-- CREATE VIEW v_NodeTypeSchema AS
-- SELECT 
--     NodeType.node_type_identifier,
--     NodeType.node_type_name,
--     NodePropertyDefinition.node_property_definition_name,
--     NodePropertyDefinition.node_property_definition_type,
--     NodePropertyDefinition.node_property_definition_is_required,
--     NodePropertyDefinition.node_property_definition_default_value,
--     NodePropertyDefinition.node_property_definition_description
-- FROM NodeType
-- LEFT JOIN NodePropertyDefinition ON NodePropertyDefinition.node_type_id_fk = NodeType.id
-- ORDER BY NodeType.node_type_name, NodePropertyDefinition.node_property_definition_name;

-- -- View: Edge type schemas
-- CREATE VIEW v_EdgeTypeSchema AS
-- SELECT 
--     EdgeType.edge_type_identifier,
--     EdgeType.edge_type_name,
--     EdgePropertyDefinition.edge_property_definition_name,
--     EdgePropertyDefinition.edge_property_definition_type,
--     EdgePropertyDefinition.edge_property_definition_is_required,
--     EdgePropertyDefinition.edge_property_definition_default_value,
--     EdgePropertyDefinition.edge_property_definition_description
-- FROM EdgeType
-- LEFT JOIN EdgePropertyDefinition ON EdgePropertyDefinition.edge_type_id_fk = EdgeType.id
-- ORDER BY EdgeType.edge_type_name, EdgePropertyDefinition.edge_property_definition_name;

-- -- View: NetworkX export format (nodes)
-- CREATE VIEW v_NetworkX_Nodes AS
-- SELECT 
--     Node.node_name,
--     NodeType.node_type_identifier,
--     GROUP_CONCAT(NodePropertyDefinition.node_property_definition_name || '=' || COALESCE(NodePropertyValue.node_property_value, ''), '|') AS properties
-- FROM Node
-- JOIN NodeType ON Node.node_type_id_fk = NodeType.id
-- LEFT JOIN NodePropertyValue ON NodePropertyValue.node_id_fk = Node.id
-- LEFT JOIN NodePropertyDefinition ON NodePropertyValue.node_property_definition_id_fk = NodePropertyDefinition.id
-- GROUP BY Node.id, Node.node_name, NodeType.node_type_identifier;

-- -- View: NetworkX export format (edges)
-- CREATE VIEW v_NetworkX_Edges AS
-- SELECT 
--     SourceNode.node_name AS source,
--     TargetNode.node_name AS target,
--     EdgeType.edge_type_identifier AS edge_type,
--     GROUP_CONCAT(
--         EdgePropertyDefinition.edge_property_definition_name || '=' || COALESCE(EdgePropertyValue.edge_property_value, ''),
--         '|'
--     ) AS properties
-- FROM Edge
-- JOIN EdgeType ON Edge.edge_type_id_fk = EdgeType.id
-- JOIN Node AS SourceNode ON Edge.source_node_id_fk = SourceNode.id
-- JOIN Node AS TargetNode ON Edge.target_node_id_fk = TargetNode.id
-- LEFT JOIN EdgePropertyValue ON EdgePropertyValue.edge_id_fk = Edge.id
-- LEFT JOIN EdgePropertyDefinition ON EdgePropertyValue.edge_property_definition_id_fk = EdgePropertyDefinition.id
-- GROUP BY Edge.id, SourceNode.node_name, TargetNode.node_name, EdgeType.edge_type_identifier;

-- ============================================================================
-- SEED DATA: SACM Types
-- ============================================================================

-- SACM Node Types
INSERT INTO NodeType (id, node_type_identifier, node_type_name, node_type_description, created_by) VALUES
    ('sacm:Claim', 'Claim', 'An assertion about system properties that must be supported', 'system'),
    ('sacm:Evidence', 'Evidence', 'Supporting information, artifacts, or test results', 'system'),
    ('sacm:Strategy', 'Strategy', 'Reasoning approach connecting claims (ArgumentReasoning)', 'system'),
    ('sacm:Context', 'Context', 'Contextual information about the argument', 'system'),
    ('sacm:Assumption', 'Assumption', 'Assumed claim that does not require support', 'system'),
    ('sacm:Justification', 'Justification', 'Explanation of reasoning or decision', 'system');

-- SACM Edge Types
INSERT INTO EdgeType (edge_type_identifier, edge_type_name, edge_type_description, created_by) VALUES
    ('sacm:SupportedBy', 'SupportedBy', 'Target supports source (AssertedInference)', 'system'),
    ('sacm:InContextOf', 'InContextOf', 'Provides contextual information (AssertedContext)', 'system'),
    ('sacm:Assumes', 'Assumes', 'Source assumes target', 'system');

-- Properties for Claim
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Main statement of the claim', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Claim';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'assumed', 'boolean', 'Whether this claim is assumed without support', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Claim';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'toBeSupported', 'boolean', 'Whether this claim requires supporting evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Claim';

-- Properties for Evidence
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the evidence', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Evidence';

INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'reference', 'string', 'Reference to evidence artifact (document ID, URL, etc.)', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Evidence';

-- Properties for Strategy
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Description of the reasoning strategy', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Strategy';

-- Properties for Context
INSERT INTO NodePropertyDefinition (node_type_id_fk, node_property_name, node_property_type, node_property_description, created_by)
SELECT id, 'content', 'text', 'Contextual information', 'system'
FROM NodeType WHERE node_type_identifier = 'sacm:Context';

-- Properties for Artefact

