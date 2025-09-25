#!/usr/bin/env python3

"""
Test package for tracer-dash models.

This package contains comprehensive tests for the models module including:
- Unit tests for SQLAlchemy model classes
- Integration tests for the Model class operations
- Test utilities and fixtures
- Configuration for pytest

Test Structure:
- test_models.py: Main test module for all model functionality
- conftest.py: Shared fixtures and test configuration
- run_tests.py: Test runner script (in project root)
- pytest.ini: Pytest configuration (in project root)

Running Tests:
- python run_tests.py                    # All tests
- python run_tests.py --unit             # Unit tests only
- python run_tests.py --integration      # Integration tests only
- python run_tests.py --coverage         # With coverage report

Test Categories:
- Unit tests: Fast, isolated tests of individual components
- Integration tests: Tests that involve database operations
- Slow tests: Tests that take longer to run (batch operations, complex scenarios)
"""

__version__ = "1.0.0"
__author__ = "Tracer-Dash Development Team"

# Test configuration constants
DEFAULT_TEST_DB_NAME = "test_tracer.db"
TEST_TIMEOUT = 30  # seconds

# Export main test classes for easier imports
from .test_models import TestSQLAlchemyModels, TestModelClass, TestModelEdgeCases

__all__ = [
    "TestSQLAlchemyModels",
    "TestModelClass", 
    "TestModelEdgeCases",
    "DEFAULT_TEST_DB_NAME",
    "TEST_TIMEOUT"
]