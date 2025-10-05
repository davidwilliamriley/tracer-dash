#!/usr/bin/env python3

# models/model.py

# Table of Contents
# 1. Imports
# 2. SQLAlchemy Models
# 3. Database Configuration
# 4. CRUD Operations
# 5. Batch Operations
# 6. Data Formatting Methods
# 7. Dash Statistics and Analytics
# 8. Utility Methods

# Imports
import os
import logging
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

# Dash-specific Logging
logger = logging.getLogger(__name__)

try:
    from pkg.config import DATABASE_CONFIG
    DEFAULT_DB_PATH = DATABASE_CONFIG["database"]
except ImportError:
    DEFAULT_DB_PATH = "db.sqlite"
    logger.warning("Could not import DATABASE_CONFIG, using default Database Path")

Base = declarative_base()

# ==================== SQLAlchemy Models ====================

class Edge(Base):
    __tablename__ = 'edges'
    
    id = Column(String, primary_key=True)
    identifier = Column(String, nullable=True)
    source_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    edge_type_id = Column(String, ForeignKey('edge_types.id'), nullable=False)
    weight = Column(Integer, default=1)
    target_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    description = Column(String, nullable=True, default=None)

    # Indexes for Performance
    __table_args__ = (
        Index('idx_edge_source', 'source_node_id'),
        Index('idx_edge_target', 'target_node_id'),
        Index('idx_edge_type', 'edge_type_id'),
    )
    
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
            'Weight': self.weight,
            'Target': self.target,
            'Description': self.description
        }

class Node(Base):
    __tablename__ = 'nodes'
    
    id = Column(String, primary_key=True)
    identifier = Column(String, nullable=True)
    name = Column(String, default='Default')
    description = Column(String, nullable=True, default=None)

    __table_args__ = (
        Index('idx_node_identifier', 'identifier'),
        Index('idx_node_name', 'name'),
    )
    
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
    description = Column(String, nullable=True, default=None)
    
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
        pass

    def _get_session(self):
        return self.SessionLocal()

    # ==================== CREATE EDGE, NODE & EDGE_TYPE OPERATIONS ====================

    # Create Edge Function

    def create_edge(self, 
                    edge_id: str, 
                    identifier: str, 
                    source_node_id: str, 
                    edge_type_id: str, 
                    target_node_id: str, 
                    description: Optional[str] = None) -> Dict[str, Any]:
        
        session = self._get_session()

        try:
            existing_edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if existing_edge:
                return {
                    'success': False,
                    'message': f"Found existing Edge with ID '{edge_id}'.",
                    'data': None
                }

            source_node = session.query(Node).filter(Node.id == source_node_id).first()
            target_node = session.query(Node).filter(Node.id == target_node_id).first()
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            
            if not source_node:
                return {
                    'success': False,
                    'message': f"Unable to find existing Source Node '{source_node_id}'.",
                    'data': None
                }
            if not target_node:
                return {
                    'success': False,
                    'message': f"Unable to find existing Target Node '{target_node_id}'.",
                    'data': None
                }
            if not edge_type:
                return {
                    'success': False,
                    'message': f"Unable to find existing Edge Type '{edge_type_id}'.",
                    'data': None
                }

            duplicate = session.query(Edge).filter(
                Edge.source_node_id == source_node_id,
                Edge.target_node_id == target_node_id,
                Edge.edge_type_id == edge_type_id
            ).first()
            
            if duplicate:
                return {
                    'success': False,
                    'message': f"Found existing Edge between '{source_node.name}' and '{target_node.name}' with Edge Type '{edge_type.name}'",
                    'data': None
                }

            new_edge = Edge(
                id=edge_id,
                identifier=identifier,
                source_node_id=source_node_id,
                edge_type_id=edge_type_id,
                target_node_id=target_node_id,
                description=description
            )

            session.add(new_edge)
            session.commit()

            return {
                'success': True,
                'message': "Successfully created Edge",
                'data': new_edge.to_dict()
            }
        
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error creating Edge: {str(e)}",
                'data': None
            }
        finally:
            session.close()


    # Create Node Function

    def create_node(self, 
                    node_id: str, 
                    identifier: str, 
                    name: str, 
                    description: Optional[str] = None) -> Dict[str, Any]:

        session = self._get_session()

        try:
            existing_node = session.query(Node).filter(Node.id == node_id).first()
            if existing_node:
                return {
                    'success': False,
                    'message': f"Found existing Node with ID '{node_id}'.",
                    'data': None
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
                'message': f"Error creating Node: {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # Create Edge Type Function

    def create_edge_type(self, 
                         edge_type_id: str, 
                         identifier: str, 
                         name: str, 
                         description: Optional[str] = None) -> Dict[str, Any]: 
        
        session = self._get_session()

        try:
            existing_edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if existing_edge_type:
                return {
                    'success': False,
                    'message': f"Found existing Edge Type with ID '{edge_type_id}'.",
                    'data': None
                }

            new_edge_type = EdgeType(id=edge_type_id, identifier=identifier, name=name, description=description)
            session.add(new_edge_type)
            session.commit()

            return {
                'success': True,
                'message': "Successfully created Edge Type",
                'data': new_edge_type.to_dict()
            }
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error creating Edge Type: {str(e)}",
                'data': None
            }
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

    # Update Edge Function

    def update_edge(self, edge_id: str, 
                    identifier: Optional[str] = None, 
                    source_node_id: Optional[str] = None, 
                    edge_type_id: Optional[str] = None, 
                    target_node_id: Optional[str] = None,
                    description: Optional[str] = None) -> Dict[str, Any]: 
        
        session = self.SessionLocal()

        try:
            edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if not edge:
                return {
                    'success': False,
                    'message': f"Unable to find Edge with ID '{edge_id}'.",
                    'data': None
                }

            if source_node_id is not None:
                source_node = session.query(Node).filter(Node.id == source_node_id).first()
                if not source_node:
                    return {
                        'success': False,
                        'message': f"Unable to find Source Node '{source_node_id}'.",
                        'data': None
                    }

                edge.source_node_id = source_node_id  # type: ignore
            
            if edge_type_id is not None:
                edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
                if not edge_type:
                    return {
                        'success': False,
                        'message': f"Unable to find Edge Type '{edge_type_id}'.",
                        'data': None
                    }
                edge.edge_type_id = edge_type_id  # type: ignore

            if target_node_id is not None:
                target_node = session.query(Node).filter(Node.id == target_node_id).first()
                if not target_node:
                    return {
                        'success': False,
                        'message': f"Unable to find Target Node '{target_node_id}'.",
                        'data': None
                    }
                edge.target_node_id = target_node_id  # type: ignore
            
            if identifier is not None:
                edge.identifier = identifier  # type: ignore
            
            if description is not None:
                edge.description = description  # type: ignore
            
            session.commit()
            return {
                'success': True,
                'message': "Successfully updated Edge",
                'data': edge.to_dict()
            }
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error updating Edge {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # Update Node Function

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
                    'message': f"Unable to find Node '{node_id}'.",
                    'data': None
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
                'message': f"Error updating node: {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # Update Edge Type Function

    def update_edge_type(self, 
                         edge_type_id: str, 
                         identifier: Optional[str] = None, 
                         name: Optional[str] = None, 
                         description: Optional[str] = None) -> Dict[str, Any]:
        
        session = self.SessionLocal()

        try:
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if not edge_type:
                return {
                    'success': False,
                    'message': f"Unable to find Edge Type with ID '{edge_type_id}'.",
                    'data': None
                }

            # Update identifier if provided
            if identifier is not None:
                edge_type.identifier = identifier  # type: ignore

            # Check for name conflicts if name is being updated
            if name is not None and name != edge_type.name:
                existing_name = session.query(EdgeType).filter(EdgeType.name == name, EdgeType.id != edge_type_id).first()
                if existing_name:
                    return {
                        'success': False,
                        'message': f"Found existing Edge Type with name '{name}'.",
                        'data': None
                    }
                edge_type.name = name  # type: ignore
                
            if description is not None:
                edge_type.description = description  # type: ignore
            
            session.commit()

            return {
                'success': True,
                'message': "Successfully updated Edge Type",
                'data': edge_type.to_dict()
            }
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error updating Edge Type: {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # ==================== DELETE OPERATIONS ====================

    # Delete Edge Function

    def delete_edge(self, edge_id: str) -> Dict[str, Any]: 
        session = self.SessionLocal()
        try:
            edge = session.query(Edge).filter(Edge.id == edge_id).first()
            if not edge:
                return {
                    'success': False,
                    'message': f"Unable to find Edge with ID '{edge_id}'",
                    'data': None
                }
            
            session.delete(edge)
            session.commit()
            return {
                'success': True,
                'message': "Successfully deleted Edge",
                'data': None
            }
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error deleting Edge: {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # Delete Node Function

    def delete_node(self, node_id: str) -> Dict[str, Any]: 
        session = self.SessionLocal()
        try:
            node = session.query(Node).filter(Node.id == node_id).first()
            if not node:
                return {
                    'success': False,
                    'message': f"Unable to find Node with ID '{node_id}'",
                    'data': None
                }
            
            referencing_edges = session.query(Edge).filter(
                (Edge.source_node_id == node_id) | (Edge.target_node_id == node_id)
            ).count()
            
            if referencing_edges > 0:
                return {
                    'success': False,
                    'message': f"Cannot delete Node '{node_id}': it is referenced by {referencing_edges} edge(s)",
                    'data': None
                }
            
            session.delete(node)
            session.commit()
            return {
                'success': True,
                'message': "Successfully deleted Node",
                'data': None
            }
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error deleting Node {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # Delete Edge Type Function

    def delete_edge_type(self, edge_type_id: str) -> Dict[str, Any]:
        session = self.SessionLocal()
        try:
            edge_type = session.query(EdgeType).filter(EdgeType.id == edge_type_id).first()
            if not edge_type:
                return {
                    'success': False,
                    'message': f"Unable to find Edge Type with ID '{edge_type_id}'",
                    'data': None
                }
            
            referencing_edges = session.query(Edge).filter(Edge.edge_type_id == edge_type_id).count()
            
            if referencing_edges > 0:
                return {
                    'success': False,
                    'message': f"Cannot delete Edge Type '{edge_type_id}': it is referenced by {referencing_edges} edge(s)",
                    'data': None
                }

            session.delete(edge_type)
            session.commit()
            return {
                'success': True,
                'message': "Successfully deleted Edge Type",
                'data': None
            }
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Error deleting Edge Type {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # ==================== BATCH OPERATIONS ====================

    # Batch Update Edges Function

    def batch_update_edges(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]: 
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
                return {
                    'success': True,    
                    'message': f"Updated {updated_count} edges. Errors: {'; '.join(errors[:5])}" + (f" and {len(errors)-5} more..." if len(errors) > 5 else "")
                }
            else:
                return {
                    'success': True,
                    'message': f"Successfully updated {updated_count} edges"
                }

        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Batch update failed: {str(e)}",
                'data': None
            }
        finally:
            session.close()

    # Batch Update Nodes Function

    def batch_update_nodes(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                return {
                    'success': True,
                    'message': f"Updated {updated_count} nodes. Errors: {'; '.join(errors)}",
                    'data': {'updated': updated_count, 'errors': errors}
                }
            else:
                return {
                    'success': True,
                    'message': f"Successfully updated {updated_count} nodes",
                    'data': {'updated': updated_count}
                }

        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Batch update failed: {str(e)}",
                'data': None
            }
        finally:
            session.close()


    # Batch Update Edge Types Function

    def batch_update_edge_types(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                return {
                    'success': True,
                    'message': f"Updated {updated_count} edge types. Errors: {'; '.join(errors)}",
                    'data': {'updated': updated_count, 'errors': errors}
                }
            else:
                return {
                    'success': True,
                    'message': f"Successfully updated {updated_count} edge types",
                    'data': {'updated': updated_count}
                }

        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f"Batch update failed: {str(e)}",
                'data': None
            }
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
        """Validate all foreign key relationships in the database"""
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