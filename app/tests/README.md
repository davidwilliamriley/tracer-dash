# Model Tests for Tracer-Dash

This directory contains comprehensive tests for the tracer-dash models package.

## Test Structure

- **`test_models.py`** - Main test module containing all model functionality tests
- **`conftest.py`** - Shared fixtures and test configuration  
- **`__init__.py`** - Package initialization with exports
- **`../run_tests.py`** - Test runner script with various options
- **`../pytest.ini`** - Pytest configuration
- **`../requirements-test.txt`** - Testing dependencies

## Test Categories

### Unit Tests (Fast, Isolated)
- `TestSQLAlchemyModels` - Tests for SQLAlchemy model classes (Node, Edge, EdgeType)
- Tests individual component behavior without database operations

### Integration Tests (Database Dependent)
- `TestModelClass` - Tests for the main Model class and its CRUD operations
- `TestModelEdgeCases` - Edge cases and error condition testing
- Tests full database interactions and business logic

## Running Tests

### Using the Test Runner Script (Recommended)

```bash
# Run all tests
python run_tests.py

# Run only unit tests (fast)
python run_tests.py --unit

# Run only integration tests 
python run_tests.py --integration

# Run with coverage report
python run_tests.py --coverage

# Run specific test file
python run_tests.py --file app/tests/test_models.py

# Run specific test function
python run_tests.py --test test_create_node_success

# Skip slow tests
python run_tests.py --no-slow

# Verbose output
python run_tests.py --verbose
```

### Using Pytest Directly

```bash
# Run all tests
pytest app/tests/

# Run with specific markers
pytest app/tests/ -m unit
pytest app/tests/ -m integration
pytest app/tests/ -m "not slow"

# Run specific test class
pytest app/tests/test_models.py::TestModelClass

# Run specific test method
pytest app/tests/test_models.py::TestModelClass::test_create_node_success

# Run with coverage
pytest app/tests/ --cov=app/models --cov-report=html
```

## Test Dependencies

Install testing dependencies:

```bash
pip install -r requirements-test.txt
```

Core dependencies:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

Optional dependencies:
- `pytest-timeout` - Test timeout protection
- `pytest-sugar` - Better output formatting
- `pytest-xdist` - Parallel test execution

## Test Features

### Comprehensive Coverage
- ✅ SQLAlchemy model creation and validation
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Relationship testing between models
- ✅ Batch operations
- ✅ Database integrity validation
- ✅ Error handling and edge cases
- ✅ Data validation and constraints

### Windows Compatibility
- ✅ Proper handling of SQLite file locking on Windows
- ✅ Graceful cleanup of temporary database files
- ✅ Engine disposal to prevent connection leaks

### Test Utilities
- Sample data fixtures for consistent testing
- Test data builders for complex scenarios  
- Temporary database creation and cleanup
- Automatic test categorization and marking

## Test Results

All tests should pass:

```
29 passed, 2 warnings in 6.78s
```

The warnings are about SQLAlchemy deprecations and can be safely ignored.

## Extending Tests

### Adding New Tests

1. Add test methods to existing test classes in `test_models.py`
2. Use appropriate fixtures (`model`, `temp_db_path`, `session`)
3. Follow naming conventions: `test_<functionality>_<scenario>`

### Adding Test Utilities

1. Add fixtures to `conftest.py` for reusable test components
2. Add sample data generators to `TestDataBuilder` class
3. Update markers in `pytest_collection_modifyitems` for automatic categorization

### Example New Test

```python
def test_new_functionality(self, model):
    """Test new functionality description"""
    # Setup
    model.create_node("test_id", "Test Node")
    
    # Action
    result = model.new_method("test_id")
    
    # Assert
    assert result is not None
    assert result.name == "Test Node"
```

## Troubleshooting

### File Permission Errors
If you see permission errors on Windows, the test fixtures handle this gracefully. The errors can be ignored as they don't affect test execution.

### SQLAlchemy Warnings
The warnings about `declarative_base()` can be ignored - they're about future SQLAlchemy 2.0+ migration.

### Database Locked Errors
The tests use proper engine disposal and session management to prevent database locks. If you encounter issues, ensure you're using the provided fixtures.

## Performance

- **Unit tests**: ~1.75s (7 tests)
- **Integration tests**: ~6.73s (22 tests) 
- **All tests**: ~6.78s (29 tests)

The test suite is optimized for both speed and thoroughness, with proper isolation between test categories.