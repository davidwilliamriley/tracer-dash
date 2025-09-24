#!/usr/bin/env python3

# models/model.py

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any
import os

try:
    from pkg.config import DATABASE_CONFIG
    DEFAULT_DB_PATH = DATABASE_CONFIG["database"]
except ImportError:
    DEFAULT_DB_PATH = "db.sqlite"

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'
    
    id = Column(String, primary_key=True)
    name = Column(String, default='Default')
    description = Column(String, default='None')

class Edge(Base):
    __tablename__ = 'edges'
    
    id = Column(String, primary_key=True)
    source_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    edge_type_id = Column(String, ForeignKey('edge_types.id'), nullable=False)
    target_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    description = Column(String, default='None')

class EdgeType(Base):
    __tablename__ = 'edge_types'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, default='Default')
    description = Column(String, default='None')

class Model:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path if db_path is not None else DEFAULT_DB_PATH
        self._initialize_database()

    def _initialize_database(self):
        try:
            self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
        except Exception as e:
            print(f"Database initialization error : {e}")

    # ==================== READ OPERATIONS ====================

    def get_nodes(self):
        session = self.SessionLocal()
        try:
            nodes = session.query(Node).all()
            return nodes
        finally:
            session.close()

    def get_edges(self):
        session = self.SessionLocal()
        try:
            edges = session.query(Edge).all()
            return edges
        finally:
            session.close()

    def get_edge_types(self):
        session = self.SessionLocal()
        try:
            edge_types = session.query(EdgeType).all()
            return edge_types
        finally:
            session.close()

    def get_node_by_id(self, node_id: str):
        session = self.SessionLocal()
        try:
            node = session.query(Node).filter(Node.id == node_id).first()
            return node
        finally:
            session.close()

    def get_edge_by_id(self, edge_id: str):
        session = self.SessionLocal()
        try:
            edge = session.query(Edge).filter(Edge.id == edge_id).first()
            return edge
        finally:
            session.close()

    def get_edge_type_by_id(self, edge_type_id: str):
        session = self.SessionLocal()
        try:
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            return edge_type
        finally:
            session.close()

    # ==================== CREATE OPERATIONS ====================

    def create_node(self, node_id: str, name: str, description: str = 'None') -> bool:
        session = self.SessionLocal()
        try:
            # Check if node already exists
            existing_node = session.query(Node).filter(Node.id == node_id).first()
            if existing_node:
                return False, f"Node with ID '{node_id}' already exists"
            
            new_node = Node(id=node_id, name=name, description=description)
            session.add(new_node)
            session.commit()
            return True, "Node created successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error creating node: {str(e)}"
        finally:
            session.close()

    def create_edge(self, edge_id: str, source_node_id: str, target_node_id: str, 
                   edge_type_id: str, description: str = 'None') -> bool:
        session = self.SessionLocal()
        try:
            # Check if edge already exists
            existing_edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if existing_edge:
                return False, f"Edge with ID '{edge_id}' already exists"
            
            # Validate source and target nodes exist
            source_node = session.query(Node).filter(Node.id == source_node_id).first()
            target_node = session.query(Node).filter(Node.id == target_node_id).first()
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            
            if not source_node:
                return False, f"Source node '{source_node_id}' does not exist"
            if not target_node:
                return False, f"Target node '{target_node_id}' does not exist"
            if not edge_type:
                return False, f"Edge type '{edge_type_id}' does not exist"
            
            new_edge = Edge(
                id=edge_id,
                source_node_id=source_node_id,
                target_node_id=target_node_id,
                edge_type_id=edge_type_id,
                description=description
            )
            session.add(new_edge)
            session.commit()
            return True, "Edge created successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error creating edge: {str(e)}"
        finally:
            session.close()

    def create_edge_type(self, edge_type_id: str, name: str, description: str = 'None') -> bool:
        session = self.SessionLocal()
        try:
            # Check if edge type already exists
            existing_edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if existing_edge_type:
                return False, f"Edge type with ID '{edge_type_id}' already exists"
            
            new_edge_type = EdgeType(id=edge_type_id, name=name, description=description)
            session.add(new_edge_type)
            session.commit()
            return True, "Edge type created successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error creating edge type: {str(e)}"
        finally:
            session.close()

    # ==================== UPDATE OPERATIONS ====================

    def update_node(self, node_id: str, name: str = None, description: str = None) -> tuple:
        session = self.SessionLocal()
        try:
            node = session.query(Node).filter(Node.id == node_id).first()
            if not node:
                return False, f"Node with ID '{node_id}' not found"
            
            if name is not None:
                node.name = name
            if description is not None:
                node.description = description
            
            session.commit()
            return True, "Node updated successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error updating node: {str(e)}"
        finally:
            session.close()

    def update_edge(self, edge_id: str, source_node_id: str = None, target_node_id: str = None,
                   edge_type_id: str = None, description: str = None) -> tuple:
        session = self.SessionLocal()
        try:
            edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if not edge:
                return False, f"Edge with ID '{edge_id}' not found"
            
            # Validate nodes and edge type if they're being updated
            if source_node_id is not None:
                source_node = session.query(Node).filter(Node.id == source_node_id).first()
                if not source_node:
                    return False, f"Source node '{source_node_id}' does not exist"
                edge.source_node_id = source_node_id
            
            if target_node_id is not None:
                target_node = session.query(Node).filter(Node.id == target_node_id).first()
                if not target_node:
                    return False, f"Target node '{target_node_id}' does not exist"
                edge.target_node_id = target_node_id
            
            if edge_type_id is not None:
                edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
                if not edge_type:
                    return False, f"Edge type '{edge_type_id}' does not exist"
                edge.edge_type_id = edge_type_id
            
            if description is not None:
                edge.description = description
            
            session.commit()
            return True, "Edge updated successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error updating edge: {str(e)}"
        finally:
            session.close()

    def update_edge_type(self, edge_type_id: str, name: str = None, description: str = None) -> tuple:
        session = self.SessionLocal()
        try:
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if not edge_type:
                return False, f"Edge type with ID '{edge_type_id}' not found"
            
            if name is not None:
                edge_type.name = name
            if description is not None:
                edge_type.description = description
            
            session.commit()
            return True, "Edge type updated successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error updating edge type: {str(e)}"
        finally:
            session.close()

    # ==================== DELETE OPERATIONS ====================

    def delete_node(self, node_id: str) -> tuple:
        session = self.SessionLocal()
        try:
            node = session.query(Node).filter(Node.id == node_id).first()
            if not node:
                return False, f"Node with ID '{node_id}' not found"
            
            # Check if node is referenced by any edges
            referencing_edges = session.query(Edge).filter(
                (Edge.source_node_id == node_id) | (Edge.target_node_id == node_id)
            ).count()
            
            if referencing_edges > 0:
                return False, f"Cannot delete node '{node_id}': it is referenced by {referencing_edges} edge(s)"
            
            session.delete(node)
            session.commit()
            return True, "Node deleted successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error deleting node: {str(e)}"
        finally:
            session.close()

    def delete_edge(self, edge_id: str) -> tuple:
        session = self.SessionLocal()
        try:
            edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if not edge:
                return False, f"Edge with ID '{edge_id}' not found"
            
            session.delete(edge)
            session.commit()
            return True, "Edge deleted successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error deleting edge: {str(e)}"
        finally:
            session.close()

    def delete_edge_type(self, edge_type_id: str) -> tuple:
        session = self.SessionLocal()
        try:
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if not edge_type:
                return False, f"Edge type with ID '{edge_type_id}' not found"
            
            # Check if edge type is referenced by any edges
            referencing_edges = session.query(Edge).filter(Edge.edge_type_id == edge_type_id).count()
            
            if referencing_edges > 0:
                return False, f"Cannot delete edge type '{edge_type_id}': it is referenced by {referencing_edges} edge(s)"
            
            session.delete(edge_type)
            session.commit()
            return True, "Edge type deleted successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error deleting edge type: {str(e)}"
        finally:
            session.close()

    # ==================== BATCH OPERATIONS ====================

    def batch_update_nodes(self, updates: List[Dict[str, Any]]) -> tuple:
        """Batch update multiple nodes"""
        session = self.SessionLocal()
        try:
            updated_count = 0
            errors = []
            
            for update in updates:
                node_id = update.get('id')
                if not node_id:
                    continue
                    
                node = session.query(Node).filter(Node.id == node_id).first()
                if node:
                    if 'name' in update:
                        node.name = update['name']
                    if 'description' in update:
                        node.description = update['description']
                    updated_count += 1
                else:
                    errors.append(f"Node '{node_id}' not found")
            
            session.commit()
            
            if errors:
                return True, f"Updated {updated_count} nodes. Errors: {'; '.join(errors)}"
            else:
                return True, f"Successfully updated {updated_count} nodes"
                
        except Exception as e:
            session.rollback()
            return False, f"Batch update failed: {str(e)}"
        finally:
            session.close()

    def batch_update_edges(self, updates: List[Dict[str, Any]]) -> tuple:
        """Batch update multiple edges"""
        session = self.SessionLocal()
        try:
            updated_count = 0
            errors = []
            
            for update in updates:
                edge_id = update.get('id')
                if not edge_id:
                    continue
                    
                edge = session.query(Edge).filter(Edge.id == edge_id).first()
                if edge:
                    # Validate references before updating
                    valid_update = True
                    
                    if 'source_node_id' in update:
                        source_exists = session.query(Node).filter(Node.id == update['source_node_id']).first()
                        if not source_exists:
                            errors.append(f"Source node '{update['source_node_id']}' not found for edge '{edge_id}'")
                            valid_update = False
                    
                    if 'target_node_id' in update:
                        target_exists = session.query(Node).filter(Node.id == update['target_node_id']).first()
                        if not target_exists:
                            errors.append(f"Target node '{update['target_node_id']}' not found for edge '{edge_id}'")
                            valid_update = False
                    
                    if 'edge_type_id' in update:
                        edge_type_exists = session.query(EdgeType).filter(EdgeType.id == update['edge_type_id']).first()
                        if not edge_type_exists:
                            errors.append(f"Edge type '{update['edge_type_id']}' not found for edge '{edge_id}'")
                            valid_update = False
                    
                    if valid_update:
                        if 'source_node_id' in update:
                            edge.source_node_id = update['source_node_id']
                        if 'target_node_id' in update:
                            edge.target_node_id = update['target_node_id']
                        if 'edge_type_id' in update:
                            edge.edge_type_id = update['edge_type_id']
                        if 'description' in update:
                            edge.description = update['description']
                        updated_count += 1
                else:
                    errors.append(f"Edge '{edge_id}' not found")
            
            session.commit()
            
            if errors:
                return True, f"Updated {updated_count} edges. Errors: {'; '.join(errors[:5])}" + (f" and {len(errors)-5} more..." if len(errors) > 5 else "")
            else:
                return True, f"Successfully updated {updated_count} edges"
                
        except Exception as e:
            session.rollback()
            return False, f"Batch update failed: {str(e)}"
        finally:
            session.close()

    def batch_update_edge_types(self, updates: List[Dict[str, Any]]) -> tuple:
        """Batch update multiple edge types"""
        session = self.SessionLocal()
        try:
            updated_count = 0
            errors = []
            
            for update in updates:
                edge_type_id = update.get('id')
                if not edge_type_id:
                    continue
                    
                edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
                if edge_type:
                    if 'name' in update:
                        edge_type.name = update['name']
                    if 'description' in update:
                        edge_type.description = update['description']
                    updated_count += 1
                else:
                    errors.append(f"Edge type '{edge_type_id}' not found")
            
            session.commit()
            
            if errors:
                return True, f"Updated {updated_count} edge types. Errors: {'; '.join(errors)}"
            else:
                return True, f"Successfully updated {updated_count} edge types"
                
        except Exception as e:
            session.rollback()
            return False, f"Batch update failed: {str(e)}"
        finally:
            session.close()

    # ==================== UTILITY METHODS ====================

    def get_node_types(self):
        """Placeholder method for compatibility - returns empty list since NodeType table doesn't exist"""
        return []

    def validate_database_integrity(self) -> tuple:
        """Validate referential integrity of the database"""
        session = self.SessionLocal()
        try:
            issues = []
            
            # Check for edges with invalid node references
            edges = session.query(Edge).all()
            for edge in edges:
                source_exists = session.query(Node).filter(Node.id == edge.source_node_id).first()
                target_exists = session.query(Node).filter(Node.id == edge.target_node_id).first()
                edge_type_exists = session.query(EdgeType).filter(EdgeType.id == edge.edge_type_id).first()
                
                if not source_exists:
                    issues.append(f"Edge '{edge.id}' references non-existent source node '{edge.source_node_id}'")
                if not target_exists:
                    issues.append(f"Edge '{edge.id}' references non-existent target node '{edge.target_node_id}'")
                if not edge_type_exists:
                    issues.append(f"Edge '{edge.id}' references non-existent edge type '{edge.edge_type_id}'")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]
        finally:
            session.close()