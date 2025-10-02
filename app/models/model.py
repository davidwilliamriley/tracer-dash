#!/usr/bin/env python3

# models/model.py

# Imports
import os
import logging
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any, Union

# Dash-specific Logging
logger = logging.getLogger(__name__)

try:
    from pkg.config import DATABASE_CONFIG
    DEFAULT_DB_PATH = DATABASE_CONFIG["database"]
except ImportError:
    DEFAULT_DB_PATH = "db.sqlite"
    logger.warning("Could not import DATABASE_CONFIG, using default database path")

Base = declarative_base()

# ==================== SQLAlchemy Models ====================

class Edge(Base):
    __tablename__ = 'edges'
    
    id = Column(String, primary_key=True)
    identifier = Column(String, nullable=True)
    source_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    edge_type_id = Column(String, ForeignKey('edge_types.id'), nullable=False)
    target_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    description = Column(String, default='None')
    
    source_node = relationship("Node", foreign_keys=[source_node_id], back_populates="source_edges")  # type: ignore
    target_node = relationship("Node", foreign_keys=[target_node_id], back_populates="target_edges")  # type: ignore
    edge_type = relationship("EdgeType", back_populates="edges")
    
    @property
    def source(self) -> str:
        return self.source_node.name if self.source_node else 'Unknown'
    
    @property
    def target(self) -> str:
        return self.target_node.name if self.target_node else 'Unknown'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ID': self.id,
            'Identifier': self.identifier,
            'Source': self.source,
            'Edge Type': self.edge_type.name if self.edge_type else 'Unknown',
            'Target': self.target,
            'Description': self.description
        }

class Node(Base):
    __tablename__ = 'nodes'
    
    id = Column(String, primary_key=True)
    identifier = Column(String, nullable=True)
    name = Column(String, default='Default')
    description = Column(String, default='None')
    
    source_edges = relationship("Edge", foreign_keys="[Edge.source_node_id]", back_populates="source_node") # type: ignore
    target_edges = relationship("Edge", foreign_keys="[Edge.target_node_id]", back_populates="target_node") # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ID': self.id,
            'Identifier': self.identifier or '',
            'Name': self.name,
            'Description': self.description
        }

class EdgeType(Base):
    __tablename__ = 'edge_types'
    
    id = Column(String, primary_key=True)
    identifier = Column(String, nullable=True)
    name = Column(String, nullable=False, default='Default')
    description = Column(String, default='None')
    
    edges = relationship("Edge", back_populates="edge_type")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ID': self.id,
            'Identifier': self.identifier or '',
            'Name': self.name,
            'Description': self.description
        }

# ==================== Main Model Class ====================

class Model:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path if db_path is not None else DEFAULT_DB_PATH
        logger.info(f"Initializing Model with Database at {self.db_path}")
        self._initialize_database()
        self._ensure_default_data()

    def _initialize_database(self):
        try:
            self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def _ensure_default_data(self):
    #     session = self.SessionLocal()
    #     try:
    #         edge_type_count = session.query(EdgeType).count()
    #         if edge_type_count == 0:
    #             default_edge_types = [
    #                 EdgeType(id="et_001", identifier="CONN", name="connects", description="Basic connection between nodes"),
    #                 EdgeType(id="et_002", identifier="DEP", name="depends_on", description="Dependency relationship"),
    #                 EdgeType(id="et_003", identifier="COMM", name="communicates_with", description="Communication relationship")
    #             ]
    #             for et in default_edge_types:
    #                 session.add(et)
    #             session.commit()
    #             logger.info("Created default edge types for Dash application")
    #     except Exception as e:
    #         session.rollback()
    #         logger.error(f"Error creating default data: {e}")
    #     finally:
    #         session.close()
        pass

    def _get_session(self):
        return self.SessionLocal()

    # ==================== CREATE EDGE, NODE & EDGE_TYPE OPERATIONS ====================

    def create_node(self, 
                    node_id: str, 
                    identifier: str, 
                    name: str, 
                    description: str = 'None') -> Dict[str, Any]:

        session = self._get_session()

        try:
            existing_node = session.query(Node).filter(Node.id == node_id).first()
            if existing_node:
                return {
                    'success': False,
                    'message': f"Found existing Node with ID '{node_id}'."
                }

            new_node = Node(id=node_id, identifier=identifier, name=name, description=description)
            session.add(new_node)
            session.commit()
            
            return {
                'success': True,
                'message': "Successfully created Node",
                'data': new_node.to_dict()
            }
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating Node: {str(e)}")
            return {
                'success': False,
                'message': f"Error creating Node: {str(e)}"
            }
        finally:
            session.close()

    def create_edge(self, 
                    edge_id: str, 
                    identifier: str, 
                    source_node_id: str, 
                    target_node_id: str, 
                    edge_type_id: str, 
                    description: str = 'None') -> tuple:
        
        session = self._get_session()

        try:
            existing_edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if existing_edge:
                return False, f"Found existing Edge with ID '{edge_id}'."
            
            source_node = session.query(Node).filter(Node.id == source_node_id).first()
            target_node = session.query(Node).filter(Node.id == target_node_id).first()
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            
            if not source_node:
                return False, f"Unable to find existing Source Node '{source_node_id}'."
            if not target_node:
                return False, f"Unable to find existing Target Node '{target_node_id}'."
            if not edge_type:
                return False, f"Unable to find existing Edge Type '{edge_type_id}'."

            duplicate = session.query(Edge).filter(
                Edge.source_node_id == source_node_id,
                Edge.target_node_id == target_node_id,
                Edge.edge_type_id == edge_type_id
            ).first()
            
            if duplicate:
                return False, f"Found existing Edge between '{source_node.name}' and '{target_node.name}' with Edge Type '{edge_type.name}'"
            
            new_edge = Edge(
                id=edge_id,
                identifier=identifier,
                source_node_id=source_node_id,
                target_node_id=target_node_id,
                edge_type_id=edge_type_id,
                description=description
            )
            session.add(new_edge)
            session.commit()
            return True, "Successfully created Edge"
        except Exception as e:
            session.rollback()
            return False, f"Error creating Edge: {str(e)}"
        finally:
            session.close()

    def create_edge_type(self, 
                         edge_type_id: str, 
                         identifier: str, 
                         name: str, 
                         description: str = 'None') -> tuple:
        
        session = self._get_session()

        try:
            existing_edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if existing_edge_type:
                return False, f"Found existing Edge Type with ID '{edge_type_id}'."

            new_edge_type = EdgeType(id=edge_type_id, identifier=identifier, name=name, description=description)
            session.add(new_edge_type)
            session.commit()
            return True, "Successfully created Edge Type"
        except Exception as e:
            session.rollback()
            return False, f"Error creating Edge Type: {str(e)}"
        finally:
            session.close()

    # ==================== READ EDGES, NODES & EDGE TYPE OPERATIONS ======================

    def get_edges(self):
        """Get all Edges from the Database"""
        session = self._get_session()
        try:
            return session.query(Edge).all()
        finally:
            session.close()

    def get_edge_by_id(self, edge_id: str):
        """Get a specific Edge by ID"""
        session = self._get_session()
        try:
            return session.query(Edge).filter(Edge.id == edge_id).first()
        finally:
            session.close()
    
    def get_nodes(self):
        session = self._get_session()
        try:
            return session.query(Node).all()
        finally:
            session.close()

    def get_node_by_id(self, node_id: str):
        session = self._get_session()
        try:
            return session.query(Node).filter(Node.id == node_id).first()
        finally:
            session.close()

    def get_edge_types(self):
        session = self._get_session()
        try:
            return session.query(EdgeType).all()
        finally:
            session.close()

    def get_edge_type_by_id(self, edge_type_id: str):
        session = self._get_session()
        try:
            return session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
        finally:
            session.close()

    # ==================== Data Formatting Methods ====================

    def get_nodes_for_editor(self) -> List[Dict[str, Any]]:
        """Get Nodes for the Editor"""
        session = self._get_session()
        try:
            nodes = session.query(Node).all()
            result = []
            for node in nodes:
                result.append({
                    'ID': str(node.id),
                    'Identifier': node.identifier or '',
                    'Name': node.name,
                    'Description': node.description
                })
            return result
        finally:
            session.close() 

    def get_edges_for_editor(self) -> List[Dict[str, Any]]:
        """Get Edges for the Editor"""
        session = self._get_session()
        try:
            edges = session.query(Edge).all()
            result = []
            for edge in edges:
                result.append({
                    'ID': str(edge.id),
                    'Identifier': edge.identifier,
                    'Source': str(edge.source_node.id),
                    'Target': str(edge.target_node.id),
                    'Edge Type': str(edge.edge_type.id),
                    'Description': edge.description
                })
            return result
        finally:
            session.close()

    def get_edge_types_for_editor(self) -> List[Dict[str, Any]]:
        """Get Edge Types for the Editor"""
        session = self.SessionLocal()
        try:
            edge_types = session.query(EdgeType).all()
            result = []
            for et in edge_types:
                result.append({
                    'ID': str(et.id),
                    'Identifier': et.identifier or '',
                    'Name': et.name,
                    'Description': et.description
                })
            return result
        finally:
            session.close()

    # ==================== UPDATE OPERATIONS ====================

    def update_node_field(self, node_id: str, field_name: str, new_value: str) -> bool:
        session = self.SessionLocal()
        try:
            node = session.query(Node).filter(Node.id == node_id).first()
            if not node:
                logger.error(f"Node with ID '{node_id}' not found")
                return False
            
            # Update the specified field
            if field_name == 'identifier':
                node.identifier = new_value  # type: ignore
            elif field_name == 'name':
                node.name = new_value  # type: ignore
            elif field_name == 'description':
                node.description = new_value  # type: ignore
            else:
                logger.error(f"Unknown field name: {field_name}")
                return False
            
            session.commit()
            logger.info(f"Successfully updated {field_name} for node {node_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating node field: {str(e)}")
            return False
        finally:
            session.close()

    def update_node(self, 
                    node_id: str, 
                    identifier: Optional[str] = None, 
                    name: Optional[str] = None, 
                    description: Optional[str] = None) -> Dict[str, Any]:
        
        session = self.SessionLocal()

        try:
            node = session.query(Node).filter(Node.id == node_id).first()
            if not node:
                return {
                    'success': False,
                    'message': f"Unable to find Node '{node_id}'."
                }

            if identifier is not None:
                node.identifier = identifier  # type: ignore

            if name is not None:
                node.name = name  # type: ignore
                
            if description is not None:
                node.description = description  # type: ignore
            
            session.commit()
            return {
                'success': True,
                'message': "Node updated successfully",
                'data': node.to_dict()
            }
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating node: {str(e)}")
            return {
                'success': False,
                'message': f"Error updating node: {str(e)}"
            }
        finally:
            session.close()

    def update_edge_type(self, 
                         edge_type_id: str, 
                         identifier: Optional[str] = None, 
                         name: Optional[str] = None, 
                         description: Optional[str] = None) -> tuple:
        
        session = self.SessionLocal()

        try:
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if not edge_type:
                return False, f"Edge type with ID '{edge_type_id}' not found"
            
            # Check for name conflicts if name is being updated
            if name is not None and name != edge_type.name:
                existing_name = session.query(EdgeType).filter(EdgeType.name == name, EdgeType.id != edge_type_id).first()
                if existing_name:
                    return False, f"Edge type with name '{name}' already exists"
                edge_type.name = name  # type: ignore
                
            if description is not None:
                edge_type.description = description  # type: ignore
            
            session.commit()
            return True, "Edge type updated successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error updating edge type: {str(e)}"
        finally:
            session.close()

    def update_edge(self, edge_id: str, 
                    identifier: Optional[str] = None, 
                    source_node_id: Optional[str] = None, 
                    target_node_id: Optional[str] = None,
                    edge_type_id: Optional[str] = None, 
                    description: Optional[str] = None) -> tuple:
        
        session = self.SessionLocal()
        try:
            edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if not edge:
                return False, f"Unable to find Edge with ID '{edge_id}'."
            
            # Validate nodes and edge type if they're being updated
            if source_node_id is not None:
                source_node = session.query(Node).filter(Node.id == source_node_id).first()
                if not source_node:
                    return False, f"Source node '{source_node_id}' does not exist"
                edge.source_node_id = source_node_id  # type: ignore
            
            if target_node_id is not None:
                target_node = session.query(Node).filter(Node.id == target_node_id).first()
                if not target_node:
                    return False, f"Target node '{target_node_id}' does not exist"
                edge.target_node_id = target_node_id  # type: ignore
            
            if edge_type_id is not None:
                edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
                if not edge_type:
                    return False, f"Edge type '{edge_type_id}' does not exist"
                edge.edge_type_id = edge_type_id  # type: ignore
            
            if description is not None:
                edge.description = description  # type: ignore
            
            session.commit()
            return True, "Edge updated successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error updating edge: {str(e)}"
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

    # ==================== BATCH OPERATIONS (Keep your existing implementation) ====================

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

    # ==================== Dash Statistics and Analytics ====================

    def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Get statistics formatted for Dash dashboard components"""
        session = self.SessionLocal()
        try:
            node_count = session.query(Node).count()
            edge_count = session.query(Edge).count()
            edge_type_count = session.query(EdgeType).count()
            
            # Get top edge types by usage
            from sqlalchemy import func
            edge_type_usage = session.query(
                EdgeType.name,
                func.count(Edge.id).label('count')
            ).join(Edge).group_by(EdgeType.name).order_by(func.count(Edge.id).desc()).limit(5).all()
            
            return {
                'success': True,
                'data': {
                    'totals': {
                        'nodes': node_count,
                        'edges': edge_count,
                        'edge_types': edge_type_count
                    },
                    'top_edge_types': [
                        {'name': et.name, 'count': et.count} for et in edge_type_usage
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Error getting dashboard statistics: {str(e)}")
            return {
                'success': False,
                'message': f"Error retrieving statistics: {str(e)}"
            }
        finally:
            session.close()

    # ==================== UTILITY METHODS ====================

    def get_node_types(self):
        """Placeholder method for compatibility - returns empty list since NodeType table doesn't exist"""
        return []

    def validate_database_integrity(self) -> Dict[str, Any]:

        session = self.SessionLocal()

        try:
            issues = []
            
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
            
            if len(issues) == 0:
                return {
                    'success': True,
                    'message': "Database integrity validation passed - no issues found",
                    'data': {'issues': []}
                }
            else:
                return {
                    'success': False,
                    'message': f"Database integrity validation found {len(issues)} issue(s)",
                    'data': {'issues': issues}
                }
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                'success': False,
                'message': f"Validation error: {str(e)}"
            }
        finally:
            session.close()