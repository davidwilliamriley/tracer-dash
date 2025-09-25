#!/usr/bin/env python3

"""
Test configuration for the models test module.

This file contains test configuration, fixtures, and utilities
that are shared across all test modules in the project.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test database settings
TEST_DB_PREFIX = "test_tracer_"
TEST_DB_SUFFIX = ".sqlite3"


@pytest.fixture(scope="session")
def test_data_directory():
    """Create a temporary directory for test data files"""
    with tempfile.TemporaryDirectory(prefix="tracer_test_") as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_nodes():
    """Provide sample node data for testing"""
    return [
        {"id": "n001", "name": "Web Server", "description": "Frontend web server"},
        {"id": "n002", "name": "Database", "description": "PostgreSQL database"},
        {"id": "n003", "name": "API Gateway", "description": "REST API gateway"},
        {"id": "n004", "name": "Cache", "description": "Redis cache server"},
        {"id": "n005", "name": "Load Balancer", "description": "NGINX load balancer"}
    ]


@pytest.fixture
def sample_edge_types():
    """Provide sample edge type data for testing"""
    return [
        {"id": "et_connects", "name": "connects", "description": "Basic connection"},
        {"id": "et_depends", "name": "depends_on", "description": "Dependency relationship"},
        {"id": "et_communicates", "name": "communicates_with", "description": "Communication channel"},
        {"id": "et_manages", "name": "manages", "description": "Management relationship"},
        {"id": "et_monitors", "name": "monitors", "description": "Monitoring relationship"}
    ]


@pytest.fixture
def sample_edges():
    """Provide sample edge data for testing (requires nodes and edge types to exist)"""
    return [
        {"id": "e001", "source_node_id": "n001", "target_node_id": "n002", "edge_type_id": "et_connects"},
        {"id": "e002", "source_node_id": "n002", "target_node_id": "n004", "edge_type_id": "et_depends"},
        {"id": "e003", "source_node_id": "n003", "target_node_id": "n001", "edge_type_id": "et_communicates"},
        {"id": "e004", "source_node_id": "n005", "target_node_id": "n001", "edge_type_id": "et_manages"},
        {"id": "e005", "source_node_id": "n005", "target_node_id": "n003", "edge_type_id": "et_monitors"}
    ]


class TestDataBuilder:
    """Utility class for building test data scenarios"""
    
    @staticmethod
    def create_basic_graph(model):
        """Create a basic graph structure for testing"""
        # Create nodes
        nodes = [
            ("n1", "Node 1", "First test node"),
            ("n2", "Node 2", "Second test node"),
            ("n3", "Node 3", "Third test node")
        ]
        
        for node_id, name, desc in nodes:
            model.create_node(node_id, name, desc)
        
        # Get default edge types
        edge_types = model.get_edge_types()
        et_id = edge_types[0].id if edge_types else None
        
        if et_id:
            # Create edges
            model.create_edge("e1", "n1", "n2", et_id, "Edge from 1 to 2")
            model.create_edge("e2", "n2", "n3", et_id, "Edge from 2 to 3")
            model.create_edge("e3", "n1", "n3", et_id, "Edge from 1 to 3")
        
        return {"nodes": 3, "edges": 3 if et_id else 0}
    
    @staticmethod
    def create_complex_graph(model):
        """Create a more complex graph structure for testing"""
        # Create multiple edge types
        edge_types_data = [
            ("et_custom_1", "controls", "Control relationship"),
            ("et_custom_2", "feeds_data", "Data flow relationship"),
            ("et_custom_3", "inherits_from", "Inheritance relationship")
        ]
        
        for et_id, name, desc in edge_types_data:
            model.create_edge_type(et_id, name, desc)
        
        # Create nodes
        nodes = [
            ("system_1", "Authentication Service", "Handles user authentication"),
            ("system_2", "User Database", "Stores user information"),
            ("system_3", "Session Manager", "Manages user sessions"),
            ("system_4", "API Gateway", "Routes API requests"),
            ("system_5", "Logging Service", "Centralized logging")
        ]
        
        for node_id, name, desc in nodes:
            model.create_node(node_id, name, desc)
        
        # Create complex relationships
        edges = [
            ("edge_1", "system_1", "system_2", "et_custom_2", "Auth reads user data"),
            ("edge_2", "system_1", "system_3", "et_custom_1", "Auth controls sessions"),
            ("edge_3", "system_4", "system_1", "et_custom_2", "Gateway routes to auth"),
            ("edge_4", "system_5", "system_1", "et_custom_3", "Logging inherits from auth"),
            ("edge_5", "system_5", "system_4", "et_custom_3", "Logging inherits from gateway")
        ]
        
        for edge_id, source, target, et_id, desc in edges:
            model.create_edge(edge_id, source, target, et_id, desc)
        
        return {"nodes": 5, "edges": 5, "edge_types": 3}


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their names and content"""
    for item in items:
        # Add markers based on test names and class names
        if "TestSQLAlchemy" in str(item.cls) or "test_sqlalchemy" in item.name.lower():
            item.add_marker(pytest.mark.unit)
        elif "TestModel" in str(item.cls) and "TestSQLAlchemy" not in str(item.cls):
            item.add_marker(pytest.mark.integration)
        elif "integration" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.name.lower():
            item.add_marker(pytest.mark.unit)
        
        # Mark tests that use complex data as slow
        if "complex" in item.name.lower() or "batch" in item.name.lower():
            item.add_marker(pytest.mark.slow)