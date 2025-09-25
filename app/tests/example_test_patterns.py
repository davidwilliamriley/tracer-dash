#!/usr/bin/env python3

"""
Example test module demonstrating how to write tests for tracer-dash models.

This file shows patterns and best practices for writing model tests.
Use this as a template when adding new tests.
"""

import pytest
from models.model import Model


class TestExamplePatterns:
    """Example test patterns and best practices"""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file path"""
        import tempfile
        import os
        import gc
        import time
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        yield db_path
        
        # Cleanup with Windows-compatible approach
        try:
            gc.collect()
            time.sleep(0.1)
            if os.path.exists(db_path):
                os.unlink(db_path)
        except (PermissionError, OSError):
            pass  # Ignore cleanup errors on Windows
    
    @pytest.fixture
    def model(self, temp_db_path):
        """Create a Model instance with temporary database"""
        model_instance = Model(db_path=temp_db_path)
        yield model_instance
        model_instance.engine.dispose()
    
    def test_basic_crud_pattern(self, model):
        """Example: Testing basic CRUD operations"""
        # Create
        success, message = model.create_node("example_01", "Example Node", "Test description")
        assert success is True
        assert "successfully" in message.lower()
        
        # Read
        node = model.get_node_by_id("example_01")
        assert node is not None
        assert node.name == "Example Node"
        assert node.description == "Test description"
        
        # Update
        success, message = model.update_node("example_01", "Updated Name")
        assert success is True
        
        updated_node = model.get_node_by_id("example_01")
        assert updated_node.name == "Updated Name"
        
        # Delete
        success, message = model.delete_node("example_01")
        assert success is True
        
        deleted_node = model.get_node_by_id("example_01")
        assert deleted_node is None
    
    def test_error_handling_pattern(self, model):
        """Example: Testing error conditions"""
        # Test duplicate creation
        model.create_node("dup_01", "First Node")
        success, message = model.create_node("dup_01", "Second Node")
        
        assert success is False
        assert "already exists" in message
    
    def test_relationship_pattern(self, model):
        """Example: Testing relationships between models"""
        # Setup related data
        model.create_node("source_01", "Source Node")
        model.create_node("target_01", "Target Node")
        
        # Get edge types
        edge_types = model.get_edge_types()
        assert len(edge_types) > 0
        
        # Create relationship
        success, message = model.create_edge(
            "rel_01", 
            "source_01", 
            "target_01", 
            edge_types[0].id,
            "Test relationship"
        )
        assert success is True
        
        # Verify relationship
        edge = model.get_edge_by_id("rel_01")
        assert edge is not None
        assert edge.source_node_id == "source_01"
        assert edge.target_node_id == "target_01"
        assert edge.description == "Test relationship"
    
    def test_data_validation_pattern(self, model):
        """Example: Testing data validation"""
        # Test with empty values
        success, message = model.create_node("empty_01", "", "")
        assert success is True  # Empty strings should be allowed
        
        node = model.get_node_by_id("empty_01")
        assert node.name == ""
        assert node.description == ""
    
    def test_batch_operations_pattern(self, model):
        """Example: Testing batch operations"""
        # Create test nodes
        model.create_node("batch_01", "Node 1")
        model.create_node("batch_02", "Node 2")
        model.create_node("batch_03", "Node 3")
        
        # Batch update
        updates = [
            {"id": "batch_01", "name": "Updated Node 1"},
            {"id": "batch_02", "name": "Updated Node 2"},
            {"id": "batch_03", "name": "Updated Node 3"}
        ]
        
        success, message = model.batch_update_nodes(updates)
        assert success is True
        assert "3 nodes" in message
        
        # Verify updates
        for i, node_id in enumerate(["batch_01", "batch_02", "batch_03"], 1):
            node = model.get_node_by_id(node_id)
            assert node.name == f"Updated Node {i}"
    
    @pytest.mark.slow
    def test_performance_pattern(self, model):
        """Example: Testing with larger datasets (marked as slow)"""
        # Create many nodes
        node_count = 100
        for i in range(node_count):
            model.create_node(f"perf_{i:03d}", f"Performance Node {i}")
        
        # Verify all were created
        nodes = model.get_nodes()
        created_nodes = [n for n in nodes if n.id.startswith("perf_")]
        assert len(created_nodes) == node_count
    
    def test_complex_scenario_pattern(self, model):
        """Example: Testing complex business scenarios"""
        # Create a mini network topology
        components = [
            ("web_server", "Web Server", "Frontend server"),
            ("app_server", "Application Server", "Business logic server"),
            ("database", "Database", "Data storage"),
            ("cache", "Cache Server", "Redis cache")
        ]
        
        # Create all components
        for comp_id, name, desc in components:
            success, _ = model.create_node(comp_id, name, desc)
            assert success is True
        
        # Create connections
        edge_types = model.get_edge_types()
        connects_type = next(et for et in edge_types if et.name == "connects")
        
        connections = [
            ("conn_01", "web_server", "app_server", "Web to App"),
            ("conn_02", "app_server", "database", "App to DB"),
            ("conn_03", "app_server", "cache", "App to Cache")
        ]
        
        for conn_id, source, target, desc in connections:
            success, _ = model.create_edge(conn_id, source, target, connects_type.id, desc)
            assert success is True
        
        # Verify the network
        edges = model.get_edges()
        created_edges = [e for e in edges if e.id.startswith("conn_")]
        assert len(created_edges) == 3
        
        # Test integrity
        is_valid, issues = model.validate_database_integrity()
        assert is_valid is True
        assert len(issues) == 0


# This would typically be in a separate file, but shown here as an example
class TestCustomModelMethods:
    """Example: Testing custom methods you might add to the Model class"""
    
    @pytest.fixture
    def temp_db_path(self):
        """Reusable fixture pattern"""
        import tempfile
        import os
        import gc
        import time
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        yield db_path
        
        try:
            gc.collect()
            time.sleep(0.1)
            if os.path.exists(db_path):
                os.unlink(db_path)
        except (PermissionError, OSError):
            pass
    
    @pytest.fixture
    def model(self, temp_db_path):
        """Reusable model fixture pattern"""
        model_instance = Model(db_path=temp_db_path)
        yield model_instance
        model_instance.engine.dispose()
    
    def test_hypothetical_search_method(self, model):
        """Example: How you might test a search method if you added one"""
        # Setup test data
        model.create_node("search_01", "Database Server", "Main database")
        model.create_node("search_02", "Web Server", "Frontend server") 
        model.create_node("search_03", "Cache Server", "Redis cache")
        
        # This method doesn't exist, but shows how you'd test it
        # results = model.search_nodes_by_name("Server")
        # assert len(results) == 3
        # 
        # results = model.search_nodes_by_name("Database")
        # assert len(results) == 1
        # assert results[0].name == "Database Server"
    
    def test_hypothetical_export_method(self, model):
        """Example: How you might test an export method if you added one"""
        # Setup test data
        model.create_node("exp_01", "Node 1", "First node")
        model.create_node("exp_02", "Node 2", "Second node")
        
        # This method doesn't exist, but shows how you'd test it
        # export_data = model.export_to_dict()
        # 
        # assert "nodes" in export_data
        # assert len(export_data["nodes"]) == 2
        # assert any(node["id"] == "exp_01" for node in export_data["nodes"])


if __name__ == "__main__":
    # Example of running these tests directly
    pytest.main([__file__, "-v"])