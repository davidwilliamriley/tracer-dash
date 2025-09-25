#!/usr/bin/env python3

"""
Test module for models.

This module contains comprehensive tests for the models package including:
- Unit tests for Node, Edge, and EdgeType SQLAlchemy models
- Integration tests for the Model class and its CRUD operations
- Database integrity and validation tests
"""

import pytest
import tempfile
import os
import gc
import time
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the models and related classes
from models.model import Node, Edge, EdgeType, Model, Base


class TestSQLAlchemyModels:
    """Test the SQLAlchemy model classes (Node, Edge, EdgeType)"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        yield db_path
        # Cleanup with Windows-compatible approach
        try:
            # Force garbage collection to close any remaining connections
            gc.collect()
            # Small delay to allow file handles to close
            time.sleep(0.1)
            if os.path.exists(db_path):
                os.unlink(db_path)
        except (PermissionError, OSError):
            # On Windows, files might still be locked - that's okay for tests
            pass
    
    @pytest.fixture
    def session(self, temp_db):
        """Create a database session for testing"""
        engine = create_engine(f'sqlite:///{temp_db}', echo=False)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
        # Dispose engine to close all connections
        engine.dispose()
    
    def test_node_creation(self, session):
        """Test Node model creation and attributes"""
        node = Node(id="test_001", name="Test Node", description="A test node")
        session.add(node)
        session.commit()
        
        # Verify the node was created
        retrieved_node = session.query(Node).filter(Node.id == "test_001").first()
        assert retrieved_node is not None
        assert retrieved_node.id == "test_001"
        assert retrieved_node.name == "Test Node"
        assert retrieved_node.description == "A test node"
    
    def test_node_defaults(self, session):
        """Test Node model default values"""
        node = Node(id="test_002")
        session.add(node)
        session.commit()
        
        retrieved_node = session.query(Node).filter(Node.id == "test_002").first()
        assert retrieved_node.name == "Default"
        assert retrieved_node.description == "None"
    
    def test_edge_type_creation(self, session):
        """Test EdgeType model creation and attributes"""
        edge_type = EdgeType(id="et_test", name="Test Type", description="A test edge type")
        session.add(edge_type)
        session.commit()
        
        retrieved_edge_type = session.query(EdgeType).filter(EdgeType.id == "et_test").first()
        assert retrieved_edge_type is not None
        assert retrieved_edge_type.id == "et_test"
        assert retrieved_edge_type.name == "Test Type"
        assert retrieved_edge_type.description == "A test edge type"
    
    def test_edge_type_defaults(self, session):
        """Test EdgeType model default values"""
        edge_type = EdgeType(id="et_default")
        session.add(edge_type)
        session.commit()
        
        retrieved_edge_type = session.query(EdgeType).filter(EdgeType.id == "et_default").first()
        assert retrieved_edge_type.name == "Default"
        assert retrieved_edge_type.description == "None"
    
    def test_edge_creation_with_relationships(self, session):
        """Test Edge model creation with proper relationships"""
        # Create nodes and edge type first
        node1 = Node(id="n1", name="Node 1")
        node2 = Node(id="n2", name="Node 2")
        edge_type = EdgeType(id="et1", name="connects")
        
        session.add_all([node1, node2, edge_type])
        session.commit()
        
        # Create edge
        edge = Edge(
            id="e1",
            source_node_id="n1",
            target_node_id="n2",
            edge_type_id="et1",
            description="Test edge"
        )
        session.add(edge)
        session.commit()
        
        # Verify relationships
        retrieved_edge = session.query(Edge).filter(Edge.id == "e1").first()
        assert retrieved_edge is not None
        assert retrieved_edge.source_node.name == "Node 1"
        assert retrieved_edge.target_node.name == "Node 2"
        assert retrieved_edge.edge_type.name == "connects"
    
    def test_edge_properties(self, session):
        """Test Edge model properties (source and target)"""
        # Create test data
        node1 = Node(id="n1", name="Source Node")
        node2 = Node(id="n2", name="Target Node")
        edge_type = EdgeType(id="et1", name="connects")
        
        session.add_all([node1, node2, edge_type])
        session.commit()
        
        edge = Edge(
            id="e1",
            source_node_id="n1",
            target_node_id="n2",
            edge_type_id="et1"
        )
        session.add(edge)
        session.commit()
        
        # Test properties
        retrieved_edge = session.query(Edge).filter(Edge.id == "e1").first()
        assert retrieved_edge.source == "Source Node"
        assert retrieved_edge.target == "Target Node"
    
    def test_node_edge_relationships(self, session):
        """Test Node to Edge relationships"""
        # Create test data
        node1 = Node(id="n1", name="Node 1")
        node2 = Node(id="n2", name="Node 2")
        edge_type = EdgeType(id="et1", name="connects")
        
        session.add_all([node1, node2, edge_type])
        session.commit()
        
        # Create edges from node1 to node2 and back
        edge1 = Edge(id="e1", source_node_id="n1", target_node_id="n2", edge_type_id="et1")
        edge2 = Edge(id="e2", source_node_id="n2", target_node_id="n1", edge_type_id="et1")
        
        session.add_all([edge1, edge2])
        session.commit()
        
        # Test relationships
        node1 = session.query(Node).filter(Node.id == "n1").first()
        node2 = session.query(Node).filter(Node.id == "n2").first()
        
        assert len(node1.source_edges) == 1
        assert len(node1.target_edges) == 1
        assert len(node2.source_edges) == 1
        assert len(node2.target_edges) == 1


class TestModelClass:
    """Test the Model class and its operations"""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file path"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        yield db_path
        # Cleanup with Windows-compatible approach
        try:
            # Force garbage collection to close any remaining connections
            gc.collect()
            # Small delay to allow file handles to close
            time.sleep(0.1)
            if os.path.exists(db_path):
                os.unlink(db_path)
        except (PermissionError, OSError):
            # On Windows, files might still be locked - that's okay for tests
            pass
    
    @pytest.fixture
    def model(self, temp_db_path):
        """Create a Model instance with temporary database"""
        model_instance = Model(db_path=temp_db_path)
        yield model_instance
        # Explicitly dispose of the engine to close connections
        model_instance.engine.dispose()
    
    def test_model_initialization(self, temp_db_path):
        """Test Model class initialization"""
        model = Model(db_path=temp_db_path)
        assert model.db_path == temp_db_path
        assert model.engine is not None
        assert model.SessionLocal is not None
        
        # Verify default edge types were created
        edge_types = model.get_edge_types()
        assert len(edge_types) >= 3
        edge_type_names = [et.name for et in edge_types]
        assert "connects" in edge_type_names
        assert "depends_on" in edge_type_names
        assert "communicates_with" in edge_type_names
    
    def test_model_default_db_path(self):
        """Test Model with default database path"""
        model = Model()
        # Should use the path from config
        assert model.db_path is not None
    
    def test_create_node_success(self, model):
        """Test successful node creation"""
        success, message = model.create_node("test_001", "Test Node", "A test node")
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify node was created
        node = model.get_node_by_id("test_001")
        assert node is not None
        assert node.name == "Test Node"
        assert node.description == "A test node"
    
    def test_create_node_duplicate_id(self, model):
        """Test node creation with duplicate ID"""
        # Create first node
        model.create_node("dup_001", "First Node")
        
        # Try to create second node with same ID
        success, message = model.create_node("dup_001", "Second Node")
        assert success is False
        assert "already exists" in message
    
    def test_create_node_duplicate_name(self, model):
        """Test node creation with duplicate name"""
        # Create first node
        model.create_node("n1", "Unique Name")
        
        # Try to create second node with same name
        success, message = model.create_node("n2", "Unique Name")
        assert success is False
        assert "already exists" in message
    
    def test_create_edge_type_success(self, model):
        """Test successful edge type creation"""
        success, message = model.create_edge_type("custom_et", "Custom Type", "A custom edge type")
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify edge type was created
        edge_type = model.get_edge_type_by_id("custom_et")
        assert edge_type is not None
        assert edge_type.name == "Custom Type"
    
    def test_create_edge_success(self, model):
        """Test successful edge creation"""
        # Create prerequisite data
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        
        # Use existing edge type
        edge_types = model.get_edge_types()
        edge_type_id = edge_types[0].id
        
        # Create edge
        success, message = model.create_edge("e1", "n1", "n2", edge_type_id, "Test edge")
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify edge was created
        edge = model.get_edge_by_id("e1")
        assert edge is not None
        assert edge.source_node_id == "n1"
        assert edge.target_node_id == "n2"
    
    def test_create_edge_nonexistent_nodes(self, model):
        """Test edge creation with nonexistent nodes"""
        edge_types = model.get_edge_types()
        edge_type_id = edge_types[0].id
        
        success, message = model.create_edge("e1", "nonexistent1", "nonexistent2", edge_type_id)
        assert success is False
        assert "does not exist" in message
    
    def test_create_edge_duplicate_relationship(self, model):
        """Test creation of duplicate edge relationships"""
        # Setup
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        edge_types = model.get_edge_types()
        edge_type_id = edge_types[0].id
        
        # Create first edge
        model.create_edge("e1", "n1", "n2", edge_type_id)
        
        # Try to create duplicate relationship
        success, message = model.create_edge("e2", "n1", "n2", edge_type_id)
        assert success is False
        assert "already exists" in message
    
    def test_update_node_success(self, model):
        """Test successful node update"""
        # Create node
        model.create_node("n1", "Original Name", "Original Description")
        
        # Update node
        success, message = model.update_node("n1", "Updated Name", "Updated Description")
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify update
        node = model.get_node_by_id("n1")
        assert node.name == "Updated Name"
        assert node.description == "Updated Description"
    
    def test_update_node_nonexistent(self, model):
        """Test update of nonexistent node"""
        success, message = model.update_node("nonexistent", "New Name")
        assert success is False
        assert "not found" in message
    
    def test_delete_node_success(self, model):
        """Test successful node deletion"""
        # Create node
        model.create_node("n1", "Test Node")
        
        # Delete node
        success, message = model.delete_node("n1")
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify deletion
        node = model.get_node_by_id("n1")
        assert node is None
    
    def test_delete_node_with_edges(self, model):
        """Test deletion of node that has edges"""
        # Setup
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        edge_types = model.get_edge_types()
        model.create_edge("e1", "n1", "n2", edge_types[0].id)
        
        # Try to delete node with edges
        success, message = model.delete_node("n1")
        assert success is False
        assert "referenced by" in message
    
    def test_delete_edge_success(self, model):
        """Test successful edge deletion"""
        # Setup
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        edge_types = model.get_edge_types()
        model.create_edge("e1", "n1", "n2", edge_types[0].id)
        
        # Delete edge
        success, message = model.delete_edge("e1")
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify deletion
        edge = model.get_edge_by_id("e1")
        assert edge is None
    
    def test_get_operations(self, model):
        """Test all get operations"""
        # Setup test data
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        edge_types = model.get_edge_types()
        model.create_edge("e1", "n1", "n2", edge_types[0].id)
        
        # Test get operations
        nodes = model.get_nodes()
        assert len(nodes) >= 2
        
        edges = model.get_edges()
        assert len(edges) >= 1
        
        edge_types_retrieved = model.get_edge_types()
        assert len(edge_types_retrieved) >= 3  # Default ones + any custom
        
        # Test individual gets
        node = model.get_node_by_id("n1")
        assert node is not None
        assert node.name == "Node 1"
        
        edge = model.get_edge_by_id("e1")
        assert edge is not None
        assert edge.source_node_id == "n1"
    
    def test_batch_update_nodes(self, model):
        """Test batch node updates"""
        # Setup
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        
        # Batch update
        updates = [
            {"id": "n1", "name": "Updated Node 1", "description": "Updated desc 1"},
            {"id": "n2", "name": "Updated Node 2", "description": "Updated desc 2"}
        ]
        
        success, message = model.batch_update_nodes(updates)
        assert success is True
        assert "2 nodes" in message
        
        # Verify updates
        node1 = model.get_node_by_id("n1")
        node2 = model.get_node_by_id("n2")
        assert node1.name == "Updated Node 1"
        assert node2.name == "Updated Node 2"
    
    def test_validate_database_integrity_clean(self, model):
        """Test database integrity validation with clean data"""
        # Setup clean data
        model.create_node("n1", "Node 1")
        model.create_node("n2", "Node 2")
        edge_types = model.get_edge_types()
        model.create_edge("e1", "n1", "n2", edge_types[0].id)
        
        # Validate
        is_valid, issues = model.validate_database_integrity()
        assert is_valid is True
        assert len(issues) == 0
    
    def test_node_types_compatibility(self, model):
        """Test the get_node_types method for compatibility"""
        node_types = model.get_node_types()
        assert isinstance(node_types, list)
        assert len(node_types) == 0  # Should return empty list as per implementation


class TestModelEdgeCases:
    """Test edge cases and error conditions"""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file path"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        yield db_path
        # Cleanup with Windows-compatible approach
        try:
            # Force garbage collection to close any remaining connections
            gc.collect()
            # Small delay to allow file handles to close
            time.sleep(0.1)
            if os.path.exists(db_path):
                os.unlink(db_path)
        except (PermissionError, OSError):
            # On Windows, files might still be locked - that's okay for tests
            pass
    
    @pytest.fixture
    def model(self, temp_db_path):
        """Create a Model instance with temporary database"""
        model_instance = Model(db_path=temp_db_path)
        yield model_instance
        # Explicitly dispose of the engine to close connections
        model_instance.engine.dispose()
    
    def test_create_operations_with_empty_strings(self, model):
        """Test create operations with empty strings"""
        # Empty name should still work (will use default)
        success, message = model.create_node("n1", "", "Description")
        assert success is True
        
        node = model.get_node_by_id("n1")
        assert node.name == ""  # Empty string should be preserved
    
    def test_create_operations_with_none_values(self, model):
        """Test create operations with None values"""
        # This should work as the model handles None values
        success, message = model.create_node("n1", "Test", None)
        assert success is True
    
    def test_update_operations_partial(self, model):
        """Test partial updates (only some fields)"""
        # Setup
        model.create_node("n1", "Original Name", "Original Description")
        
        # Update only name
        success, message = model.update_node("n1", name="New Name")
        assert success is True
        
        node = model.get_node_by_id("n1")
        assert node.name == "New Name"
        assert node.description == "Original Description"
        
        # Update only description
        success, message = model.update_node("n1", description="New Description")
        assert success is True
        
        node = model.get_node_by_id("n1")
        assert node.name == "New Name"
        assert node.description == "New Description"
    
    def test_batch_operations_with_mixed_results(self, model):
        """Test batch operations with some successes and some failures"""
        # Setup some nodes
        model.create_node("n1", "Node 1")
        
        # Batch update with mix of existing and non-existing nodes
        updates = [
            {"id": "n1", "name": "Updated Node 1"},  # Should work
            {"id": "n_nonexistent", "name": "Should fail"},  # Should fail
            {"id": "", "name": "Empty ID"}  # Should be skipped
        ]
        
        success, message = model.batch_update_nodes(updates)
        # Should still return success but mention errors
        assert success is True
        assert "1 nodes" in message or "Errors" in message


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])