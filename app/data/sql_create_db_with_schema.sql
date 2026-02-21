-- ============================================================================
-- TRACER: Graph Database Schema v2
--
-- SQLite Implementation of a Flexible Graph Database with support 
-- for Dynamic Node and Edge Types, Reusable Property Definitions 
-- assigned via Junction Tables, and Property Values.
--
-- CHANGES FROM v1:
--   - NodePropertyDefinition / EdgePropertyDefinition decoupled from types
--   - New NodeTypePropertyAssignment / EdgeTypePropertyAssignment junction tables
--   - node_description removed from Node (define as a property instead)
--   - edge_description removed from Edge (define as a property instead)
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ============================================================================
-- TYPE LAYER: Define NodeTypes and EdgeTypes
-- ============================================================================

CREATE TABLE NodeType (
    id TEXT PRIMARY KEY,
    node_type_identifier TEXT UNIQUE,
    node_type_name TEXT NOT NULL,
    node_type_description TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_nodetype_name ON NodeType(node_type_name);

CREATE TABLE EdgeType (
    id TEXT PRIMARY KEY,
    edge_type_identifier TEXT UNIQUE,
    edge_type_name TEXT NOT NULL,
    edge_type_description TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_edgetype_name ON EdgeType(edge_type_name);

-- ============================================================================
-- PROPERTY DEFINITION LAYER: Reusable Property Definitions (type-independent)
-- ============================================================================

CREATE TABLE NodePropertyDefinition (
    id TEXT PRIMARY KEY,
    node_property_definition_identifier TEXT UNIQUE,
    node_property_definition_name TEXT NOT NULL UNIQUE,
    node_property_definition_description TEXT,
    node_property_definition_type TEXT NOT NULL CHECK(node_property_definition_type IN ('text', 'integer', 'float', 'boolean', 'date', 'datetime')),
    node_property_definition_default_value TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_node_property_definition_name ON NodePropertyDefinition(node_property_definition_name);

CREATE TABLE EdgePropertyDefinition (
    id TEXT PRIMARY KEY,
    edge_property_definition_identifier TEXT UNIQUE,
    edge_property_definition_name TEXT NOT NULL UNIQUE,
    edge_property_definition_description TEXT,
    edge_property_definition_type TEXT NOT NULL CHECK(edge_property_definition_type IN ('text','integer', 'float', 'boolean', 'date', 'datetime')),
    edge_property_definition_default_value TEXT,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_edge_property_definition_name ON EdgePropertyDefinition(edge_property_definition_name);

-- ============================================================================
-- PROPERTY ASSIGNMENT LAYER: Assign Property Definitions to Types
-- ============================================================================

CREATE TABLE NodeTypePropertyAssignment (
    id TEXT PRIMARY KEY,
    node_type_id_fk TEXT NOT NULL,
    node_property_definition_id_fk TEXT NOT NULL,
    is_required BOOLEAN DEFAULT 0,
    default_value TEXT,
    sort_order INTEGER DEFAULT 0,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (node_type_id_fk) REFERENCES NodeType(id) ON DELETE CASCADE,
    FOREIGN KEY (node_property_definition_id_fk) REFERENCES NodePropertyDefinition(id) ON DELETE CASCADE,
    UNIQUE(node_type_id_fk, node_property_definition_id_fk)
);

CREATE INDEX idx_ntpa_node_type ON NodeTypePropertyAssignment(node_type_id_fk);
CREATE INDEX idx_ntpa_property_def ON NodeTypePropertyAssignment(node_property_definition_id_fk);

CREATE TABLE EdgeTypePropertyAssignment (
    id TEXT PRIMARY KEY,
    edge_type_id_fk TEXT NOT NULL,
    edge_property_definition_id_fk TEXT NOT NULL,
    is_required BOOLEAN DEFAULT 0,
    default_value TEXT,
    sort_order INTEGER DEFAULT 0,
    created_by TEXT,
    created_on TEXT DEFAULT (datetime('now')),
    modified_by TEXT,
    modified_on TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (edge_type_id_fk) REFERENCES EdgeType(id) ON DELETE CASCADE,
    FOREIGN KEY (edge_property_definition_id_fk) REFERENCES EdgePropertyDefinition(id) ON DELETE CASCADE,
    UNIQUE(edge_type_id_fk, edge_property_definition_id_fk)
);

CREATE INDEX idx_etpa_edge_type ON EdgeTypePropertyAssignment(edge_type_id_fk);
CREATE INDEX idx_etpa_property_def ON EdgeTypePropertyAssignment(edge_property_definition_id_fk);

-- ============================================================================
-- PROPERTY DEFINITION DEFAULT VALUE VALIDATION TRIGGERS
-- ============================================================================

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

    SELECT RAISE(ABORT, 'Default value does not match expected Type (float)')
    WHERE NEW.node_property_definition_type = 'float'
    AND NOT (
        (
            NEW.node_property_definition_default_value NOT GLOB '*[^0-9.]*'
            AND NEW.node_property_definition_default_value GLOB '[0-9]*'
            AND (LENGTH(NEW.node_property_definition_default_value) - LENGTH(REPLACE(NEW.node_property_definition_default_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.node_property_definition_default_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.node_property_definition_default_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.node_property_definition_default_value) - LENGTH(REPLACE(NEW.node_property_definition_default_value, '.', ''))) <= 1
        )
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (boolean)')
    WHERE NEW.node_property_definition_type = 'boolean'
    AND NEW.node_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected Type (date - expected YYYY-MM-DD)')
    WHERE NEW.node_property_definition_type = 'date'
    AND (
        date(NEW.node_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.node_property_definition_default_value) != NEW.node_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (datetime - expected YYYY-MM-DD HH:MM:SS)')
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
    SELECT RAISE(ABORT, 'Default value does not match expected Type (integer)')
    WHERE NEW.node_property_definition_type = 'integer'
    AND NOT (
        (TRIM(NEW.node_property_definition_default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.node_property_definition_default_value)) > 0)
        OR
        (substr(TRIM(NEW.node_property_definition_default_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.node_property_definition_default_value)) > 1
         AND substr(TRIM(NEW.node_property_definition_default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (float)')
    WHERE NEW.node_property_definition_type = 'float'
    AND NOT (
        (
            NEW.node_property_definition_default_value NOT GLOB '*[^0-9.]*'
            AND NEW.node_property_definition_default_value GLOB '[0-9]*'
            AND (LENGTH(NEW.node_property_definition_default_value) - LENGTH(REPLACE(NEW.node_property_definition_default_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.node_property_definition_default_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.node_property_definition_default_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.node_property_definition_default_value) - LENGTH(REPLACE(NEW.node_property_definition_default_value, '.', ''))) <= 1
        )
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (boolean)')
    WHERE NEW.node_property_definition_type = 'boolean'
    AND NEW.node_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected Type (date - expected YYYY-MM-DD)')
    WHERE NEW.node_property_definition_type = 'date'
    AND (
        date(NEW.node_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.node_property_definition_default_value) != NEW.node_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (datetime - expected YYYY-MM-DD HH:MM:SS)')
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

    SELECT RAISE(ABORT, 'Default value does not match expected Type (float)')
    WHERE NEW.edge_property_definition_type = 'float'
    AND NOT (
        (
            NEW.edge_property_definition_default_value NOT GLOB '*[^0-9.]*'
            AND NEW.edge_property_definition_default_value GLOB '[0-9]*'
            AND (LENGTH(NEW.edge_property_definition_default_value) - LENGTH(REPLACE(NEW.edge_property_definition_default_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.edge_property_definition_default_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.edge_property_definition_default_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.edge_property_definition_default_value) - LENGTH(REPLACE(NEW.edge_property_definition_default_value, '.', ''))) <= 1
        )
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (boolean)')
    WHERE NEW.edge_property_definition_type = 'boolean'
    AND NEW.edge_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected Type (date - expected YYYY-MM-DD)')
    WHERE NEW.edge_property_definition_type = 'date'
    AND (
        date(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE NEW.edge_property_definition_type = 'datetime'
    AND (
        datetime(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );
END;

-- Trigger to validate Edge Property Definition default value Types (UPDATE)
CREATE TRIGGER validate_edge_property_definition_default_value_update
BEFORE UPDATE ON EdgePropertyDefinition
WHEN NEW.edge_property_definition_default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Default value does not match expected Type (integer)')
    WHERE NEW.edge_property_definition_type = 'integer'
    AND NOT (
        (TRIM(NEW.edge_property_definition_default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.edge_property_definition_default_value)) > 0)
        OR
        (substr(TRIM(NEW.edge_property_definition_default_value), 1, 1) = '-'
         AND LENGTH(TRIM(NEW.edge_property_definition_default_value)) > 1
         AND substr(TRIM(NEW.edge_property_definition_default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (float)')
    WHERE NEW.edge_property_definition_type = 'float'
    AND NOT (
        (
            NEW.edge_property_definition_default_value NOT GLOB '*[^0-9.]*'
            AND NEW.edge_property_definition_default_value GLOB '[0-9]*'
            AND (LENGTH(NEW.edge_property_definition_default_value) - LENGTH(REPLACE(NEW.edge_property_definition_default_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.edge_property_definition_default_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.edge_property_definition_default_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.edge_property_definition_default_value) - LENGTH(REPLACE(NEW.edge_property_definition_default_value, '.', ''))) <= 1
        )
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (boolean)')
    WHERE NEW.edge_property_definition_type = 'boolean'
    AND NEW.edge_property_definition_default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Default value does not match expected Type (date - expected YYYY-MM-DD)')
    WHERE NEW.edge_property_definition_type = 'date'
    AND (
        date(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );

    SELECT RAISE(ABORT, 'Default value does not match expected Type (datetime - expected YYYY-MM-DD HH:MM:SS)')
    WHERE NEW.edge_property_definition_type = 'datetime'
    AND (
        datetime(NEW.edge_property_definition_default_value) IS NULL
        OR strftime('%Y-%m-%d %H:%M:%S', NEW.edge_property_definition_default_value) != NEW.edge_property_definition_default_value
    );
END;

-- ============================================================================
-- ASSIGNMENT DEFAULT VALUE VALIDATION TRIGGERS
-- Validate that default_value on assignment matches the property definition type
-- ============================================================================

CREATE TRIGGER validate_ntpa_default_value_insert
BEFORE INSERT ON NodeTypePropertyAssignment
WHEN NEW.default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Assignment default value does not match property type (integer)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'integer'
    AND NOT (
        (TRIM(NEW.default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.default_value)) > 0)
        OR
        (substr(TRIM(NEW.default_value), 1, 1) = '-' AND LENGTH(TRIM(NEW.default_value)) > 1
         AND substr(TRIM(NEW.default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (float)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'float'
    AND NOT (
        (NEW.default_value NOT GLOB '*[^0-9.]*' AND NEW.default_value GLOB '[0-9]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
        OR
        (NEW.default_value GLOB '-[0-9]*' AND SUBSTR(NEW.default_value, 2) NOT GLOB '*[^0-9.]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (boolean)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'boolean'
    AND NEW.default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (date)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'date'
    AND (date(NEW.default_value) IS NULL OR strftime('%Y-%m-%d', NEW.default_value) != NEW.default_value);

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (datetime)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'datetime'
    AND (datetime(NEW.default_value) IS NULL OR strftime('%Y-%m-%d %H:%M:%S', NEW.default_value) != NEW.default_value);
END;

CREATE TRIGGER validate_ntpa_default_value_update
BEFORE UPDATE ON NodeTypePropertyAssignment
WHEN NEW.default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Assignment default value does not match property type (integer)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'integer'
    AND NOT (
        (TRIM(NEW.default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.default_value)) > 0)
        OR
        (substr(TRIM(NEW.default_value), 1, 1) = '-' AND LENGTH(TRIM(NEW.default_value)) > 1
         AND substr(TRIM(NEW.default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (float)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'float'
    AND NOT (
        (NEW.default_value NOT GLOB '*[^0-9.]*' AND NEW.default_value GLOB '[0-9]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
        OR
        (NEW.default_value GLOB '-[0-9]*' AND SUBSTR(NEW.default_value, 2) NOT GLOB '*[^0-9.]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (boolean)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'boolean'
    AND NEW.default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (date)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'date'
    AND (date(NEW.default_value) IS NULL OR strftime('%Y-%m-%d', NEW.default_value) != NEW.default_value);

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (datetime)')
    WHERE (SELECT node_property_definition_type FROM NodePropertyDefinition WHERE id = NEW.node_property_definition_id_fk) = 'datetime'
    AND (datetime(NEW.default_value) IS NULL OR strftime('%Y-%m-%d %H:%M:%S', NEW.default_value) != NEW.default_value);
END;

CREATE TRIGGER validate_etpa_default_value_insert
BEFORE INSERT ON EdgeTypePropertyAssignment
WHEN NEW.default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Assignment default value does not match property type (integer)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'integer'
    AND NOT (
        (TRIM(NEW.default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.default_value)) > 0)
        OR
        (substr(TRIM(NEW.default_value), 1, 1) = '-' AND LENGTH(TRIM(NEW.default_value)) > 1
         AND substr(TRIM(NEW.default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (float)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'float'
    AND NOT (
        (NEW.default_value NOT GLOB '*[^0-9.]*' AND NEW.default_value GLOB '[0-9]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
        OR
        (NEW.default_value GLOB '-[0-9]*' AND SUBSTR(NEW.default_value, 2) NOT GLOB '*[^0-9.]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (boolean)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'boolean'
    AND NEW.default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (date)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'date'
    AND (date(NEW.default_value) IS NULL OR strftime('%Y-%m-%d', NEW.default_value) != NEW.default_value);

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (datetime)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'datetime'
    AND (datetime(NEW.default_value) IS NULL OR strftime('%Y-%m-%d %H:%M:%S', NEW.default_value) != NEW.default_value);
END;

CREATE TRIGGER validate_etpa_default_value_update
BEFORE UPDATE ON EdgeTypePropertyAssignment
WHEN NEW.default_value IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'Assignment default value does not match property type (integer)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'integer'
    AND NOT (
        (TRIM(NEW.default_value) NOT GLOB '*[^0-9]*' AND LENGTH(TRIM(NEW.default_value)) > 0)
        OR
        (substr(TRIM(NEW.default_value), 1, 1) = '-' AND LENGTH(TRIM(NEW.default_value)) > 1
         AND substr(TRIM(NEW.default_value), 2) NOT GLOB '*[^0-9]*')
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (float)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'float'
    AND NOT (
        (NEW.default_value NOT GLOB '*[^0-9.]*' AND NEW.default_value GLOB '[0-9]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
        OR
        (NEW.default_value GLOB '-[0-9]*' AND SUBSTR(NEW.default_value, 2) NOT GLOB '*[^0-9.]*'
         AND (LENGTH(NEW.default_value) - LENGTH(REPLACE(NEW.default_value, '.', ''))) <= 1)
    );

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (boolean)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'boolean'
    AND NEW.default_value NOT IN ('0', '1', 'true', 'false');

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (date)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'date'
    AND (date(NEW.default_value) IS NULL OR strftime('%Y-%m-%d', NEW.default_value) != NEW.default_value);

    SELECT RAISE(ABORT, 'Assignment default value does not match property type (datetime)')
    WHERE (SELECT edge_property_definition_type FROM EdgePropertyDefinition WHERE id = NEW.edge_property_definition_id_fk) = 'datetime'
    AND (datetime(NEW.default_value) IS NULL OR strftime('%Y-%m-%d %H:%M:%S', NEW.default_value) != NEW.default_value);
END;

-- ============================================================================
-- INSTANCE LAYER: Define Nodes and Edges
-- ============================================================================

CREATE TABLE Node (
    id TEXT PRIMARY KEY,
    node_type_id_fk TEXT NOT NULL,
    node_identifier TEXT UNIQUE,
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
    edge_identifier TEXT UNIQUE,
    edge_name TEXT NOT NULL,
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

-- Trigger to ensure Property Definition is assigned to the Node's Type (INSERT)
CREATE TRIGGER validate_node_property_type_insert
BEFORE INSERT ON NodePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition is not assigned to this NodeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Node
        JOIN NodeTypePropertyAssignment ON NodeTypePropertyAssignment.node_type_id_fk = Node.node_type_id_fk
        WHERE Node.id = NEW.node_id_fk
          AND NodeTypePropertyAssignment.node_property_definition_id_fk = NEW.node_property_definition_id_fk
    );
END;

-- Trigger to ensure Property Definition is assigned to the Node's Type (UPDATE)
CREATE TRIGGER validate_node_property_type_update
BEFORE UPDATE ON NodePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition is not assigned to this NodeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Node
        JOIN NodeTypePropertyAssignment ON NodeTypePropertyAssignment.node_type_id_fk = Node.node_type_id_fk
        WHERE Node.id = NEW.node_id_fk
          AND NodeTypePropertyAssignment.node_property_definition_id_fk = NEW.node_property_definition_id_fk
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
    AND NOT (
        (
            NEW.node_property_value NOT GLOB '*[^0-9.]*'
            AND NEW.node_property_value GLOB '[0-9]*'
            AND (LENGTH(NEW.node_property_value) - LENGTH(REPLACE(NEW.node_property_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.node_property_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.node_property_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.node_property_value) - LENGTH(REPLACE(NEW.node_property_value, '.', ''))) <= 1
        )
    );

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
    AND NOT (
        (
            NEW.node_property_value NOT GLOB '*[^0-9.]*'
            AND NEW.node_property_value GLOB '[0-9]*'
            AND (LENGTH(NEW.node_property_value) - LENGTH(REPLACE(NEW.node_property_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.node_property_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.node_property_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.node_property_value) - LENGTH(REPLACE(NEW.node_property_value, '.', ''))) <= 1
        )
    );

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

-- Trigger to ensure Property Definition is assigned to the Edge's Type (INSERT)
CREATE TRIGGER validate_edge_property_type_insert
BEFORE INSERT ON EdgePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition is not assigned to this EdgeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Edge
        JOIN EdgeTypePropertyAssignment ON EdgeTypePropertyAssignment.edge_type_id_fk = Edge.edge_type_id_fk
        WHERE Edge.id = NEW.edge_id_fk
          AND EdgeTypePropertyAssignment.edge_property_definition_id_fk = NEW.edge_property_definition_id_fk
    );
END;

-- Trigger to ensure Property Definition is assigned to the Edge's Type (UPDATE)
CREATE TRIGGER validate_edge_property_type_update
BEFORE UPDATE ON EdgePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Property Definition is not assigned to this EdgeType')
    WHERE NOT EXISTS (
        SELECT 1
        FROM Edge
        JOIN EdgeTypePropertyAssignment ON EdgeTypePropertyAssignment.edge_type_id_fk = Edge.edge_type_id_fk
        WHERE Edge.id = NEW.edge_id_fk
          AND EdgeTypePropertyAssignment.edge_property_definition_id_fk = NEW.edge_property_definition_id_fk
    );
END;

-- Trigger to validate Edge Property Value Types against Definitions (INSERT)
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
    AND NOT (
        (
            NEW.edge_property_value NOT GLOB '*[^0-9.]*'
            AND NEW.edge_property_value GLOB '[0-9]*'
            AND (LENGTH(NEW.edge_property_value) - LENGTH(REPLACE(NEW.edge_property_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.edge_property_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.edge_property_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.edge_property_value) - LENGTH(REPLACE(NEW.edge_property_value, '.', ''))) <= 1
        )
    );

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

-- Trigger to validate Edge Property Value Types against Definitions (UPDATE)
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
    AND NOT (
        (
            NEW.edge_property_value NOT GLOB '*[^0-9.]*'
            AND NEW.edge_property_value GLOB '[0-9]*'
            AND (LENGTH(NEW.edge_property_value) - LENGTH(REPLACE(NEW.edge_property_value, '.', ''))) <= 1
        )
        OR
        (
            NEW.edge_property_value GLOB '-[0-9]*'
            AND SUBSTR(NEW.edge_property_value, 2) NOT GLOB '*[^0-9.]*'
            AND (LENGTH(NEW.edge_property_value) - LENGTH(REPLACE(NEW.edge_property_value, '.', ''))) <= 1
        )
    );

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
-- REQUIRED PROPERTY PROTECTION TRIGGERS: Prevent NULL or deletion of required property values
-- NOTE: is_required now lives on the Assignment table, so lookups join through it.
-- ============================================================================

CREATE TRIGGER protect_required_node_property_value_null_insert
BEFORE INSERT ON NodePropertyValue
WHEN NEW.node_property_value IS NULL
BEGIN
    SELECT RAISE(ABORT, 'Cannot insert NULL for a required property value')
    WHERE EXISTS (
        SELECT 1 FROM NodeTypePropertyAssignment ntpa
        JOIN Node n ON n.node_type_id_fk = ntpa.node_type_id_fk AND n.id = NEW.node_id_fk
        WHERE ntpa.node_property_definition_id_fk = NEW.node_property_definition_id_fk
          AND ntpa.is_required = 1
    );
END;

CREATE TRIGGER protect_required_node_property_value_null_update
BEFORE UPDATE ON NodePropertyValue
WHEN NEW.node_property_value IS NULL
BEGIN
    SELECT RAISE(ABORT, 'Cannot set a required property value to NULL')
    WHERE EXISTS (
        SELECT 1 FROM NodeTypePropertyAssignment ntpa
        JOIN Node n ON n.node_type_id_fk = ntpa.node_type_id_fk AND n.id = NEW.node_id_fk
        WHERE ntpa.node_property_definition_id_fk = NEW.node_property_definition_id_fk
          AND ntpa.is_required = 1
    );
END;

CREATE TRIGGER protect_required_edge_property_value_null_insert
BEFORE INSERT ON EdgePropertyValue
WHEN NEW.edge_property_value IS NULL
BEGIN
    SELECT RAISE(ABORT, 'Cannot insert NULL for a required property value')
    WHERE EXISTS (
        SELECT 1 FROM EdgeTypePropertyAssignment etpa
        JOIN Edge e ON e.edge_type_id_fk = etpa.edge_type_id_fk AND e.id = NEW.edge_id_fk
        WHERE etpa.edge_property_definition_id_fk = NEW.edge_property_definition_id_fk
          AND etpa.is_required = 1
    );
END;

CREATE TRIGGER protect_required_edge_property_value_null_update
BEFORE UPDATE ON EdgePropertyValue
WHEN NEW.edge_property_value IS NULL
BEGIN
    SELECT RAISE(ABORT, 'Cannot set a required property value to NULL')
    WHERE EXISTS (
        SELECT 1 FROM EdgeTypePropertyAssignment etpa
        JOIN Edge e ON e.edge_type_id_fk = etpa.edge_type_id_fk AND e.id = NEW.edge_id_fk
        WHERE etpa.edge_property_definition_id_fk = NEW.edge_property_definition_id_fk
          AND etpa.is_required = 1
    );
END;

CREATE TRIGGER protect_required_node_property_value_delete
BEFORE DELETE ON NodePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete a required property value')
    WHERE EXISTS (
        SELECT 1 FROM NodeTypePropertyAssignment ntpa
        JOIN Node n ON n.node_type_id_fk = ntpa.node_type_id_fk AND n.id = OLD.node_id_fk
        WHERE ntpa.node_property_definition_id_fk = OLD.node_property_definition_id_fk
          AND ntpa.is_required = 1
    );
END;

CREATE TRIGGER protect_required_edge_property_value_delete
BEFORE DELETE ON EdgePropertyValue
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete a required property value')
    WHERE EXISTS (
        SELECT 1 FROM EdgeTypePropertyAssignment etpa
        JOIN Edge e ON e.edge_type_id_fk = etpa.edge_type_id_fk AND e.id = OLD.edge_id_fk
        WHERE etpa.edge_property_definition_id_fk = OLD.edge_property_definition_id_fk
          AND etpa.is_required = 1
    );
END;

-- ============================================================================
-- BOOLEAN NORMALISATION TRIGGERS: Normalise boolean values to '1'/'0' on INSERT/UPDATE
-- ============================================================================

CREATE TRIGGER normalise_node_property_value_boolean_insert
AFTER INSERT ON NodePropertyValue
WHEN NEW.node_property_value IN ('true', 'false')
  AND (
    SELECT node_property_definition_type FROM NodePropertyDefinition
    WHERE id = NEW.node_property_definition_id_fk
  ) = 'boolean'
BEGIN
    UPDATE NodePropertyValue
    SET node_property_value = CASE NEW.node_property_value WHEN 'true' THEN '1' ELSE '0' END
    WHERE id = NEW.id;
END;

CREATE TRIGGER normalise_node_property_value_boolean_update
AFTER UPDATE ON NodePropertyValue
WHEN NEW.node_property_value IN ('true', 'false')
  AND (
    SELECT node_property_definition_type FROM NodePropertyDefinition
    WHERE id = NEW.node_property_definition_id_fk
  ) = 'boolean'
BEGIN
    UPDATE NodePropertyValue
    SET node_property_value = CASE NEW.node_property_value WHEN 'true' THEN '1' ELSE '0' END
    WHERE id = NEW.id;
END;

CREATE TRIGGER normalise_edge_property_value_boolean_insert
AFTER INSERT ON EdgePropertyValue
WHEN NEW.edge_property_value IN ('true', 'false')
  AND (
    SELECT edge_property_definition_type FROM EdgePropertyDefinition
    WHERE id = NEW.edge_property_definition_id_fk
  ) = 'boolean'
BEGIN
    UPDATE EdgePropertyValue
    SET edge_property_value = CASE NEW.edge_property_value WHEN 'true' THEN '1' ELSE '0' END
    WHERE id = NEW.id;
END;

CREATE TRIGGER normalise_edge_property_value_boolean_update
AFTER UPDATE ON EdgePropertyValue
WHEN NEW.edge_property_value IN ('true', 'false')
  AND (
    SELECT edge_property_definition_type FROM EdgePropertyDefinition
    WHERE id = NEW.edge_property_definition_id_fk
  ) = 'boolean'
BEGIN
    UPDATE EdgePropertyValue
    SET edge_property_value = CASE NEW.edge_property_value WHEN 'true' THEN '1' ELSE '0' END
    WHERE id = NEW.id;
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

CREATE TRIGGER update_ntpa_modified_on
AFTER UPDATE ON NodeTypePropertyAssignment
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE NodeTypePropertyAssignment SET modified_on = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER update_etpa_modified_on
AFTER UPDATE ON EdgeTypePropertyAssignment
WHEN NEW.modified_on = OLD.modified_on
BEGIN
    UPDATE EdgeTypePropertyAssignment SET modified_on = datetime('now') WHERE id = NEW.id;
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
