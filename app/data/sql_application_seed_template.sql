-- ============================================================================
-- TRACER APPLICATION SEED TEMPLATE
--
-- Purpose:
--   Populate this template with application-specific data (types, properties,
--   assignments, nodes, edges, and property values).
--
-- Usage:
--   1) Replace placeholders in {{DOUBLE_BRACES}}.
--   2) Keep IDs unique (UUIDs recommended).
--   3) Run after creating the DB with Schema
-- ============================================================================

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- ============================================================================
-- 1) NODE TYPES
-- ============================================================================

-- Repeat per node type required by your application.
INSERT INTO NodeType (
    id,
    node_type_identifier,
    node_type_name,
    node_type_description,
    created_by
) VALUES
('{{NODE_TYPE_ID_1}}', '{{NODE_TYPE_IDENTIFIER_1}}', '{{NODE_TYPE_NAME_1}}', '{{NODE_TYPE_DESCRIPTION_1}}', '{{CREATED_BY}}');

-- Example additional row:
-- ('{{NODE_TYPE_ID_2}}', '{{NODE_TYPE_IDENTIFIER_2}}', '{{NODE_TYPE_NAME_2}}', '{{NODE_TYPE_DESCRIPTION_2}}', '{{CREATED_BY}}');

-- ============================================================================
-- 2) EDGE TYPES
-- ============================================================================

INSERT INTO EdgeType (
    id,
    edge_type_identifier,
    edge_type_name,
    edge_type_description,
    created_by
) VALUES
('{{EDGE_TYPE_ID_1}}', '{{EDGE_TYPE_IDENTIFIER_1}}', '{{EDGE_TYPE_NAME_1}}', '{{EDGE_TYPE_DESCRIPTION_1}}', '{{CREATED_BY}}');

-- ============================================================================
-- 3) PROPERTY DEFINITIONS (TYPE-INDEPENDENT)
-- ============================================================================

-- Allowed types: text, integer, float, boolean, date, datetime

INSERT INTO NodePropertyDefinition (
    id,
    node_property_definition_identifier,
    node_property_definition_name,
    node_property_definition_description,
    node_property_definition_type,
    node_property_definition_default_value,
    created_by
) VALUES
(
    '{{NODE_PROP_DEF_ID_1}}',
    '{{NODE_PROP_DEF_IDENTIFIER_1}}',
    '{{NODE_PROP_DEF_NAME_1}}',
    '{{NODE_PROP_DEF_DESCRIPTION_1}}',
    '{{NODE_PROP_DEF_TYPE_1}}',
    {{NODE_PROP_DEF_DEFAULT_VALUE_1_OR_NULL}},
    '{{CREATED_BY}}'
);

INSERT INTO EdgePropertyDefinition (
    id,
    edge_property_definition_identifier,
    edge_property_definition_name,
    edge_property_definition_description,
    edge_property_definition_type,
    edge_property_definition_default_value,
    created_by
) VALUES
(
    '{{EDGE_PROP_DEF_ID_1}}',
    '{{EDGE_PROP_DEF_IDENTIFIER_1}}',
    '{{EDGE_PROP_DEF_NAME_1}}',
    '{{EDGE_PROP_DEF_DESCRIPTION_1}}',
    '{{EDGE_PROP_DEF_TYPE_1}}',
    {{EDGE_PROP_DEF_DEFAULT_VALUE_1_OR_NULL}},
    '{{CREATED_BY}}'
);

-- ============================================================================
-- 4) PROPERTY ASSIGNMENTS (LINK DEFINITIONS TO TYPES)
-- ============================================================================

INSERT INTO NodeTypePropertyAssignment (
    id,
    node_type_id_fk,
    node_property_definition_id_fk,
    is_required,
    default_value,
    sort_order,
    created_by
) VALUES
(
    '{{NTPA_ID_1}}',
    '{{NODE_TYPE_ID_1}}',
    '{{NODE_PROP_DEF_ID_1}}',
    {{NTPA_IS_REQUIRED_0_OR_1}},
    {{NTPA_DEFAULT_VALUE_OR_NULL}},
    {{NTPA_SORT_ORDER}},
    '{{CREATED_BY}}'
);

INSERT INTO EdgeTypePropertyAssignment (
    id,
    edge_type_id_fk,
    edge_property_definition_id_fk,
    is_required,
    default_value,
    sort_order,
    created_by
) VALUES
(
    '{{ETPA_ID_1}}',
    '{{EDGE_TYPE_ID_1}}',
    '{{EDGE_PROP_DEF_ID_1}}',
    {{ETPA_IS_REQUIRED_0_OR_1}},
    {{ETPA_DEFAULT_VALUE_OR_NULL}},
    {{ETPA_SORT_ORDER}},
    '{{CREATED_BY}}'
);

-- ============================================================================
-- 5) NODES
-- ============================================================================

INSERT INTO Node (
    id,
    node_type_id_fk,
    node_identifier,
    node_name,
    created_by
) VALUES
(
    '{{NODE_ID_1}}',
    '{{NODE_TYPE_ID_1}}',
    '{{NODE_IDENTIFIER_1}}',
    '{{NODE_NAME_1}}',
    '{{CREATED_BY}}'
);

-- ============================================================================
-- 6) EDGES
-- ============================================================================

INSERT INTO Edge (
    id,
    edge_type_id_fk,
    edge_identifier,
    edge_name,
    source_node_id_fk,
    target_node_id_fk,
    created_by
) VALUES
(
    '{{EDGE_ID_1}}',
    '{{EDGE_TYPE_ID_1}}',
    '{{EDGE_IDENTIFIER_1}}',
    '{{EDGE_NAME_1}}',
    '{{SOURCE_NODE_ID_1}}',
    '{{TARGET_NODE_ID_1}}',
    '{{CREATED_BY}}'
);

-- ============================================================================
-- 7) NODE PROPERTY VALUES
-- ============================================================================

INSERT INTO NodePropertyValue (
    id,
    node_id_fk,
    node_property_definition_id_fk,
    node_property_value,
    created_by
) VALUES
(
    '{{NODE_PROP_VALUE_ID_1}}',
    '{{NODE_ID_1}}',
    '{{NODE_PROP_DEF_ID_1}}',
    {{NODE_PROPERTY_VALUE_1}},
    '{{CREATED_BY}}'
);

-- ============================================================================
-- 8) EDGE PROPERTY VALUES
-- ============================================================================

INSERT INTO EdgePropertyValue (
    id,
    edge_id_fk,
    edge_property_definition_id_fk,
    edge_property_value,
    created_by
) VALUES
(
    '{{EDGE_PROP_VALUE_ID_1}}',
    '{{EDGE_ID_1}}',
    '{{EDGE_PROP_DEF_ID_1}}',
    {{EDGE_PROPERTY_VALUE_1}},
    '{{CREATED_BY}}'
);

COMMIT;

-- ============================================================================
-- QUICK NOTES
-- - Use NULL (without quotes) for null values.
-- - Use quoted text values, e.g. 'My Value'.
-- - Boolean values accepted by triggers: '0', '1', 'true', 'false'.
-- - Date format: YYYY-MM-DD
-- - Datetime format: YYYY-MM-DD HH:MM:SS
-- ============================================================================
