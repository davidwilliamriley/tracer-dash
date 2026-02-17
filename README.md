# Prism

**A Plotly Dash-based Systems Life Cycle Process Management Application**

## Project Description
Objective is to provide a Complete, Efficient, Robust and Resilient Network.

## Outstanding Items 
https://github.com/users/davidwilliamriley/projects/1

## Installation Instructions
Clone this Respository 

## Usage Examples

### Edges
[Placeholder]

### Nodes 
[Placeholder]

## Node Types

### Edge Types
[Placeholder]

## Schema Validation Test

Use the SQL smoke test at `app/data/sql_schema_validation_tests.sql` to validate schema constraints and triggers.

### Option 1: SQLite CLI

From the repository root:

```powershell
sqlite3 :memory: ".read app/data/sql_create_db_schema.sql" ".read app/data/sql_schema_validation_tests.sql"
```

Expected result: no errors.

### Option 2: Python (built-in sqlite3)

From the repository root:

```powershell
python -c "import sqlite3, pathlib; con=sqlite3.connect(':memory:'); con.executescript(pathlib.Path('app/data/sql_create_db_schema.sql').read_text(encoding='utf-8')); con.executescript(pathlib.Path('app/data/sql_schema_validation_tests.sql').read_text(encoding='utf-8')); print('OK: schema validation test passed')"
```

Expected result: `OK: schema validation test passed`

### Optional Negative Checks

In `app/data/sql_schema_validation_tests.sql`, uncomment one negative test at a time under `OPTIONAL NEGATIVE TESTS`. Each one should fail with a trigger validation error.

## Contributing Guidelines
Email the Owner

## License Information
Not Yet Licensed

