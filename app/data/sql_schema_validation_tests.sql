-- ============================================================================
-- TRACER: Schema Validation Smoke Tests
-- Usage:
--   1) Load schema first (sql_create_db_schema.sql)
--   2) Run this script to validate happy-path integrity and trigger behavior
--
-- Notes:
--   - This script is idempotent for test IDs (it deletes/reinserts test rows).
--   - Optional negative tests are included at the bottom (commented out).
-- ============================================================================

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- --------------------------------------------------------------------------
-- Cleanup (safe re-run)
-- --------------------------------------------------------------------------
DELETE FROM EdgePropertyValue WHERE id IN ('t_epv_1');
DELETE FROM NodePropertyValue WHERE id IN ('t_npv_1', 't_npv_2', 't_npv_3');

DELETE FROM EdgePropertyDefinition WHERE id IN ('t_epd_bool', 't_epd_dt');
DELETE FROM NodePropertyDefinition WHERE id IN ('t_npd_int', 't_npd_date', 't_npd_dt');

DELETE FROM Edge WHERE id IN ('t_edge_1');
DELETE FROM Node WHERE id IN ('t_node_1', 't_node_2');

DELETE FROM EdgeType WHERE id IN ('t_et_1');
DELETE FROM NodeType WHERE id IN ('t_nt_1');

-- --------------------------------------------------------------------------
-- Core seed data
-- --------------------------------------------------------------------------
INSERT INTO NodeType (id, node_type_identifier, node_type_name)
VALUES ('t_nt_1', 'test.node.type.1', 'Test Node Type 1');

INSERT INTO EdgeType (id, edge_type_identifier, edge_type_name)
VALUES ('t_et_1', 'test.edge.type.1', 'Test Edge Type 1');

INSERT INTO Node (id, node_type_id_fk, node_identifier, node_name)
VALUES
('t_node_1', 't_nt_1', 'test.node.1', 'Test Node 1'),
('t_node_2', 't_nt_1', 'test.node.2', 'Test Node 2');

INSERT INTO Edge (id, edge_type_id_fk, source_node_id_fk, target_node_id_fk)
VALUES ('t_edge_1', 't_et_1', 't_node_1', 't_node_2');

-- --------------------------------------------------------------------------
-- Property definitions (validate default-value trigger happy path)
-- --------------------------------------------------------------------------
INSERT INTO NodePropertyDefinition (
    id,
    node_type_id_fk,
    node_property_definition_name,
    node_property_definition_type,
    node_property_definition_default_value
)
VALUES
('t_npd_int', 't_nt_1', 'test_int_default', 'integer', '42'),
('t_npd_date', 't_nt_1', 'test_date_default', 'date', '2026-12-31'),
('t_npd_dt', 't_nt_1', 'test_dt_default', 'datetime', '2026-12-31 23:59:59');

INSERT INTO EdgePropertyDefinition (
    id,
    edge_type_id_fk,
    edge_property_definition_name,
    edge_property_definition_type,
    edge_property_definition_default_value
)
VALUES
('t_epd_bool', 't_et_1', 'test_bool_default', 'boolean', 'true'),
('t_epd_dt', 't_et_1', 'test_dt_default', 'datetime', '2026-12-31 23:59:59');

-- --------------------------------------------------------------------------
-- Property values (validate value trigger happy path)
-- --------------------------------------------------------------------------
INSERT INTO NodePropertyValue (
    id,
    node_id_fk,
    node_property_definition_id_fk,
    node_property_value
)
VALUES
('t_npv_1', 't_node_1', 't_npd_int', '7'),
('t_npv_2', 't_node_1', 't_npd_date', '2026-01-15'),
('t_npv_3', 't_node_1', 't_npd_dt', '2026-01-15 14:30:45');

INSERT INTO EdgePropertyValue (
    id,
    edge_id_fk,
    edge_property_definition_id_fk,
    edge_property_value
)
VALUES ('t_epv_1', 't_edge_1', 't_epd_bool', 'false');

-- --------------------------------------------------------------------------
-- Assertions (abort transaction if expectations are not met)
-- --------------------------------------------------------------------------
CREATE TEMP TABLE _assert_success (ok INTEGER CHECK (ok = 1));

INSERT INTO _assert_success(ok)
SELECT CASE
    WHEN EXISTS (
        SELECT 1 FROM Edge
        WHERE id = 't_edge_1'
          AND source_node_id_fk = 't_node_1'
          AND target_node_id_fk = 't_node_2'
    ) THEN 1 ELSE 0
END;

INSERT INTO _assert_success(ok)
SELECT CASE
    WHEN EXISTS (
        SELECT 1 FROM NodePropertyDefinition
        WHERE id = 't_npd_int'
          AND node_property_definition_default_value = '42'
    ) THEN 1 ELSE 0
END;

INSERT INTO _assert_success(ok)
SELECT CASE
    WHEN EXISTS (
        SELECT 1 FROM EdgePropertyDefinition
        WHERE id = 't_epd_bool'
          AND edge_property_definition_default_value = 'true'
    ) THEN 1 ELSE 0
END;

INSERT INTO _assert_success(ok)
SELECT CASE
    WHEN EXISTS (
        SELECT 1 FROM NodePropertyValue
        WHERE id = 't_npv_3'
          AND node_property_value = '2026-01-15 14:30:45'
    ) THEN 1 ELSE 0
END;

INSERT INTO _assert_success(ok)
SELECT CASE
    WHEN EXISTS (
        SELECT 1 FROM EdgePropertyValue
        WHERE id = 't_epv_1'
          AND edge_property_value = 'false'
    ) THEN 1 ELSE 0
END;

DROP TABLE _assert_success;

COMMIT;

-- ============================================================================
-- OPTIONAL NEGATIVE TESTS (UNCOMMENT ONE AT A TIME; each should FAIL)
-- ============================================================================
-- INSERT INTO NodePropertyDefinition (
--     id, node_type_id_fk, node_property_definition_name,
--     node_property_definition_type, node_property_definition_default_value
-- ) VALUES ('t_npd_bad_int', 't_nt_1', 'bad_int_default', 'integer', '1.0');
--
-- INSERT INTO NodePropertyValue (
--     id, node_id_fk, node_property_definition_id_fk, node_property_value
-- ) VALUES ('t_npv_bad_date', 't_node_1', 't_npd_date', '2026-19-39');
--
-- INSERT INTO EdgePropertyDefinition (
--     id, edge_type_id_fk, edge_property_definition_name,
--     edge_property_definition_type, edge_property_definition_default_value
-- ) VALUES ('t_epd_bad_dt', 't_et_1', 'bad_dt_default', 'datetime', '2026-19-39 23:59:59');
