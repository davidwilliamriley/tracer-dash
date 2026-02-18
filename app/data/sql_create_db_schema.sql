-- ============================================================================
-- TRACER: Graph Database Schema
-- SQLite Implementation of SACM Graph Data Model
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
    edge_type_identifier TEXT,
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

CREATE INDEX idx_node_property_definition_node_type ON NodePropertyDefinition(node_type_id_fk);
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

CREATE INDEX idx_edge_property_definition_edge_type ON EdgePropertyDefinition(edge_type_id_fk);
CREATE INDEX idx_edge_property_definition_name ON EdgePropertyDefinition(edge_property_definition_name);

-- Trigger to validate Node Property Definition default value types (INSERT)
CREATE TRIGGER validate_node_property_definition_default_value_insert
BEFORE INSERT ON NodePropertyDefinition
WHEN NEW.node_property_definition_default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Default value does not match expected type (integer)')
    WHERE NEW.node_property_definition_type = 'integer'
    AND NOT (
        (TRIM(NEW.node_property_definition_default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.node_property_definition_default_value)) > 0)
        OR
        (substr(TRIM(NEW.node_property_definition_default_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.node_property_definition_default_value)) > 1
         AND substr(TRIM(NEW.node_property_definition_default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (float)')
    WHERE NEW.node_property_definition_type = 'float'
    AND typeof(NEW.node_property_definition_default_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.node_property_definition_default_value AS REAL) IS NOT NULL
             AND CAST(NEW.node_property_definition_default_value AS REAL) != 0.0
             OR NEW.node_property_definition_default_value = '0'
             OR NEW.node_property_definition_default_value = '0.0');

    SELECT RAISE(ABORT, 'Default value does not match expected type (boolean)')
    WHERE NEW.node_property_definition_type = 'boolean'
    AND NEW.node_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE NEW.node_property_definition_type = 'date'
    AND (
        date(NEW.node_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.node_property_definition_default_value) != NEW.node_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE NEW.node_property_definition_type = 'datetime'
    AND (
        datetime(NEW.node_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.node_property_definition_default_value) != NEW.node_property_definition_default_value
    );
END;

-- Trigger to validate Node Property Definition default value types (UPDATE)
CREATE TRIGGER validate_node_property_definition_default_value_update
BEFORE UPDATE ON NodePropertyDefinition
WHEN NEW.node_property_definition_default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Default value does not match expected type (integer)')
    WHERE NEW.node_property_definition_type = 'integer'
    AND NOT (
        (TRIM(NEW.node_property_definition_default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.node_property_definition_default_value)) > 0)
        OR
        (substr(TRIM(NEW.node_property_definition_default_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.node_property_definition_default_value)) > 1
         AND substr(TRIM(NEW.node_property_definition_default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (float)')
    WHERE NEW.node_property_definition_type = 'float'
    AND typeof(NEW.node_property_definition_default_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.node_property_definition_default_value AS REAL) IS NOT NULL
             AND CAST(NEW.node_property_definition_default_value AS REAL) != 0.0
             OR NEW.node_property_definition_default_value = '0'
             OR NEW.node_property_definition_default_value = '0.0');

    SELECT RAISE(ABORT, 'Default value does not match expected type (boolean)')
    WHERE NEW.node_property_definition_type = 'boolean'
    AND NEW.node_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE NEW.node_property_definition_type = 'date'
    AND (
        date(NEW.node_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.node_property_definition_default_value) != NEW.node_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE NEW.node_property_definition_type = 'datetime'
    AND (
        datetime(NEW.node_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.node_property_definition_default_value) != NEW.node_property_definition_default_value
    );
END;

-- Trigger to validate Edge Property Definition default value types (INSERT)
CREATE TRIGGER validate_edge_property_definition_default_value_insert
BEFORE INSERT ON EdgePropertyDefinition
WHEN NEW.edge_property_definition_default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Default value does not match expected type (integer)')
    WHERE NEW.edge_property_definition_type = 'integer'
    AND NOT (
        (TRIM(NEW.edge_property_definition_default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.edge_property_definition_default_value)) > 0)
        OR
        (substr(TRIM(NEW.edge_property_definition_default_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.edge_property_definition_default_value)) > 1
         AND substr(TRIM(NEW.edge_property_definition_default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (float)')
    WHERE NEW.edge_property_definition_type = 'float'
    AND typeof(NEW.edge_property_definition_default_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.edge_property_definition_default_value AS REAL) IS NOT NULL
             AND CAST(NEW.edge_property_definition_default_value AS REAL) != 0.0
             OR NEW.edge_property_definition_default_value = '0'
             OR NEW.edge_property_definition_default_value = '0.0');

    SELECT RAISE(ABORT, 'Default value does not match expected type (boolean)')
    WHERE NEW.edge_property_definition_type = 'boolean'
    AND NEW.edge_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE NEW.edge_property_definition_type = 'date'
    AND (
        date(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE NEW.edge_property_definition_type = 'datetime'
    AND (
        datetime(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );
END;

-- Trigger to validate Edge Property Definition default value types (UPDATE)
CREATE TRIGGER validate_edge_property_definition_default_value_update
BEFORE UPDATE ON EdgePropertyDefinition
WHEN NEW.edge_property_definition_default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Default value does not match expected type (integer)')
    WHERE NEW.edge_property_definition_type = 'integer'
    AND NOT (
        (TRIM(NEW.edge_property_definition_default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.edge_property_definition_default_value)) > 0)
        OR
        (substr(TRIM(NEW.edge_property_definition_default_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.edge_property_definition_default_value)) > 1
         AND substr(TRIM(NEW.edge_property_definition_default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (float)')
    WHERE NEW.edge_property_definition_type = 'float'
    AND typeof(NEW.edge_property_definition_default_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.edge_property_definition_default_value AS REAL) IS NOT NULL
             AND CAST(NEW.edge_property_definition_default_value AS REAL) != 0.0
             OR NEW.edge_property_definition_default_value = '0'
             OR NEW.edge_property_definition_default_value = '0.0');

    SELECT RAISE(ABORT, 'Default value does not match expected type (boolean)')
    WHERE NEW.edge_property_definition_type = 'boolean'
    AND NEW.edge_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE NEW.edge_property_definition_type = 'date'
    AND (
        date(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE NEW.edge_property_definition_type = 'datetime'
    AND (
        datetime(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );
END;

-- ============================================================================
-- INSTANCE LAYER: Define Nodes and Edges
-- ============================================================================

CREATE TABLE Node (
    id TEXT PRIMARY KEY,
    node_type_id_fk TEXT NOT NULL,
    node_identifier TEXT NOT NULL UNIQUE,
    node_name TEXT NOT NULL,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (node_type_id_fk) REFERENCES NodeType(id) ON DELETE RESTRICT,
    UNIQUE(node_type_id_fk, node_name)
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

-- Trigger to validate Node Property Value Types against Definitions (INSERT)
CREATE TRIGGER validate_node_property_value_type_insert
BEFORE INSERT ON NodePropertyValue
WHEN NEW.node_property_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Property value does not match expected type (integer)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'integer'
    AND NOT (
        (TRIM(NEW.node_property_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.node_property_value)) > 0)
        OR
        (substr(TRIM(NEW.node_property_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.node_property_value)) > 1
         AND substr(TRIM(NEW.node_property_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (float)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'float'
    AND typeof(NEW.node_property_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.node_property_value AS REAL) IS NOT NULL
             AND CAST(NEW.node_property_value AS REAL) != 0.0
             OR NEW.node_property_value = '0'
             OR NEW.node_property_value = '0.0');

    SELECT RAISE(ABORT, 'Property value does not match expected type (boolean)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'boolean'
    AND NEW.node_property_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Property value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'date'
    AND (
        date(NEW.node_property_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.node_property_value) != NEW.node_property_value
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'datetime'
    AND (
        datetime(NEW.node_property_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.node_property_value) != NEW.node_property_value
    );
END;

-- Trigger to validate Node Property Value Types against Definitions (UPDATE)
CREATE TRIGGER validate_node_property_value_type_update
BEFORE UPDATE ON NodePropertyValue
WHEN NEW.node_property_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Property value does not match expected type (integer)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'integer'
    AND NOT (
        (TRIM(NEW.node_property_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.node_property_value)) > 0)
        OR
        (substr(TRIM(NEW.node_property_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.node_property_value)) > 1
         AND substr(TRIM(NEW.node_property_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (float)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'float'
    AND typeof(NEW.node_property_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.node_property_value AS REAL) IS NOT NULL
             AND CAST(NEW.node_property_value AS REAL) != 0.0
             OR NEW.node_property_value = '0'
             OR NEW.node_property_value = '0.0');

    SELECT RAISE(ABORT, 'Property value does not match expected type (boolean)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'boolean'
    AND NEW.node_property_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Property value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'date'
    AND (
        date(NEW.node_property_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.node_property_value) != NEW.node_property_value
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE (
        SELECT node_property_definition_type FROM NodePropertyDefinition
        WHERE id = NEW.node_property_definition_id_fk
    ) = 'datetime'
    AND (
        datetime(NEW.node_property_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.node_property_value) != NEW.node_property_value
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

CREATE TRIGGER validate_edge_property_value_type_insert
BEFORE INSERT ON EdgePropertyValue
WHEN NEW.edge_property_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Property value does not match expected type (integer)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'integer'
    AND NOT (
        (TRIM(NEW.edge_property_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.edge_property_value)) > 0)
        OR
        (substr(TRIM(NEW.edge_property_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.edge_property_value)) > 1
         AND substr(TRIM(NEW.edge_property_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (float)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'float'
    AND typeof(NEW.edge_property_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.edge_property_value AS REAL) IS NOT NULL
             AND CAST(NEW.edge_property_value AS REAL) != 0.0
             OR NEW.edge_property_value = '0'
             OR NEW.edge_property_value = '0.0');

    SELECT RAISE(ABORT, 'Property value does not match expected type (boolean)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'boolean'
    AND NEW.edge_property_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Property value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'date'
    AND (
        date(NEW.edge_property_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.edge_property_value) != NEW.edge_property_value
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'datetime'
    AND (
        datetime(NEW.edge_property_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.edge_property_value) != NEW.edge_property_value
    );
END;

CREATE TRIGGER validate_edge_property_value_type_update
BEFORE UPDATE ON EdgePropertyValue
WHEN NEW.edge_property_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Property value does not match expected type (integer)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'integer'
    AND NOT (
        (TRIM(NEW.edge_property_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.edge_property_value)) > 0)
        OR
        (substr(TRIM(NEW.edge_property_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.edge_property_value)) > 1
         AND substr(TRIM(NEW.edge_property_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (float)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'float'
    AND typeof(NEW.edge_property_value) NOT IN ('integer', 'real')
    AND NOT (CAST(NEW.edge_property_value AS REAL) IS NOT NULL
             AND CAST(NEW.edge_property_value AS REAL) != 0.0
             OR NEW.edge_property_value = '0'
             OR NEW.edge_property_value = '0.0');

    SELECT RAISE(ABORT, 'Property value does not match expected type (boolean)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'boolean'
    AND NEW.edge_property_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Property value does not match expected type (date - expected YYYY-MM-DD)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'date'
    AND (
        date(NEW.edge_property_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.edge_property_value) != NEW.edge_property_value
    );

    SELECT RAISE(ABORT, 'Property value does not match expected type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE (
        SELECT edge_property_definition_type FROM EdgePropertyDefinition
        WHERE id = NEW.edge_property_definition_id_fk
    ) = 'datetime'
    AND (
        datetime(NEW.edge_property_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.edge_property_value) != NEW.edge_property_value
    );
END;

-- ============================================================================
-- AUTO-UPDATE TRIGGERS: Set modified_on on UPDATE
-- ============================================================================

CREATE TRIGGER update_nodetype_modified_on
AFTER UPDATE ON NodeType
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE NodeType SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_edgetype_modified_on
AFTER UPDATE ON EdgeType
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE EdgeType SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_node_property_definition_modified_on
AFTER UPDATE ON NodePropertyDefinition
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE NodePropertyDefinition SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_edge_property_definition_modified_on
AFTER UPDATE ON EdgePropertyDefinition
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE EdgePropertyDefinition SET modified_on = datetime('now') WHERE id = NEW.id;
END;

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
