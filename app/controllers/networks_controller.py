# controllers/networks_controller.py - NetworkX-based controller for Networks Page

import networkx as nx
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import joinedload

from models.model import Model, Node, Edge

class NetworksController:
    """NetworkX-based controller for networks page - creates and analyzes graphs"""

    def __init__(self, model: Optional[Model] = None):
        """Initialise the controller with an instance of the Model"""
        self.model = model or Model()
        self._graph = None

    def get_network(self) -> nx.Graph:
        """Build NetworkX graph from database Nodes and Edges"""
        return self._build_network_from_database()

    def _build_network_from_database(self) -> nx.Graph:
        """Internal method to build the NetworkX Graph from the Database - used by GraphStore"""
        try:
            # Get a Session to ensure proper loading
            session = self.model._get_session()

            try:
                # Use eager loading to avoid lazy loading issues
                nodes = session.query(Node).all()
                edges = (
                    session.query(Edge)
                    .options(
                        joinedload(Edge.edge_type),
                        joinedload(Edge.source_node),
                        joinedload(Edge.target_node),
                    )
                    .all()
                )

                G = nx.Graph()

                # Add the Nodes
                for node in nodes:
                    G.add_node(
                        node.id,
                        identifier=node.identifier or "",
                        name=node.name or "",
                        description=node.description or "",
                    )

                # Add the Edges
                for edge in edges:
                    if G.has_node(edge.source_node_id) and G.has_node(
                        edge.target_node_id
                    ):
                        G.add_edge(
                            edge.source_node_id,
                            edge.target_node_id,
                            edge_id=edge.id,
                            relationship_type=(
                                edge.edge_type.name if edge.edge_type else "connects to"
                            ),
                            description=edge.description or "",
                        )

                return G

            finally:
                session.close()

        except Exception as e:
            # Handle any exceptions that might occur during graph building
            print(f"Error building NetworkX graph: {e}")
            raise

    def get_network_visualization_data(self) -> Dict[str, Any]:
        """Get the Network formatted for Cytoscape"""
        try:
            # Get a session to ensure proper loading
            session = self.model._get_session()

            try:
                # Use eager loading to avoid lazy loading issues
                nodes = session.query(Node).all()
                edges = (
                    session.query(Edge)
                    .options(
                        joinedload(Edge.edge_type),
                        joinedload(Edge.source_node),
                        joinedload(Edge.target_node),
                    )
                    .all()
                )

                G = nx.Graph()
                elements = []

                # Add nodes to both NetworkX graph and elements list
                for node in nodes:
                    G.add_node(
                        node.id,
                        identifier=node.identifier or "",
                        name=node.name or "",
                        description=node.description or "",
                    )

                    elements.append(
                        {
                            "group": "nodes",
                            "data": {
                                "id": str(node.id),
                                "label": node.name or node.identifier or "Unnamed",
                                "name": node.name or "",
                                "identifier": node.identifier or "",
                                "description": node.description or "",
                            },
                        }
                    )

                # Add edges to both NetworkX graph and elements list
                for edge in edges:
                    if G.has_node(edge.source_node_id) and G.has_node(
                        edge.target_node_id
                    ):
                        edge_type_name = (
                            edge.edge_type.name if edge.edge_type else "connects to"
                        )

                        G.add_edge(
                            edge.source_node_id,
                            edge.target_node_id,
                            edge_id=edge.id,
                            relationship_type=edge_type_name,
                            description=edge.description or "",
                        )

                        elements.append(
                            {
                                "group": "edges",
                                "data": {
                                    "id": str(edge.id),
                                    "identifier": edge.identifier or "",
                                    "source": str(edge.source_node_id),
                                    "label": edge_type_name,
                                    "target": str(edge.target_node_id),
                                    "description": edge_type_name,
                                },
                            }
                        )

                # Store the NetworkX graph for potential reuse
                self._graph = G

                return {"elements": elements}

            finally:
                session.close()

        except Exception as e:
            print(f"Error getting visualization data: {e}")
            return {"elements": []}

    def get_graph_for_cache(self):
        """
        Get graph data formatted for dcc.Store caching.

        Returns:
            Serialized graph data suitable for dcc.Store
        """
        try:
            graph = self.get_network()
            # return GraphCacheUtils.serialize_networkx_graph(graph)
        except Exception as e:
            print(f"Error serializing graph for cache: {e}")
            return {}

    def get_cache_metadata(self):
        # """Get metadata about the current graph for caching."""
        # try:
        #     # Get database counts
        #     session = self.model._get_session()
        #     try:
        #         nodes_count = session.query(Node).count()
        #         edges_count = session.query(Edge).count()

        #         # return GraphCacheUtils.create_cache_metadata(
        #         #     nodes_count, edges_count, {"source": "database"}
        #         # )
        #     finally:
        #         session.close()
        # except Exception as e:
        #     print(f"Error getting cache metadata: {e}")
        #     return {}
        pass

    def restore_graph_from_cache(
        self, cached_data: Dict[str, Any]
    ) -> Optional[nx.Graph]:
        """Restore NetworkX graph from dcc.Store cached data."""
        # return GraphCacheUtils.deserialize_networkx_graph(cached_data)
