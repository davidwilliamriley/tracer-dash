# views/view.py

# Imports
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config


class View:
    def __init__(self, controller):
        self.controller = controller

    def render_header(self):
        st.title("🔍 Tracer")
        st.write("Welcome to Tracer - System Configuration Information Manager")

    def render_sidebar(self):
        with st.sidebar:
            st.title("📦 Tracer")

            if 'current_page' not in st.session_state:
                st.session_state.current_page = "Network"

            selection = st.radio(
                "", 
                ["Networks", "Reports", "Nodes & Edges", "Settings"],
                index=["Networks", "Reports", "Nodes & Edges", "Settings"].index(st.session_state.current_page),
                key="page_selection"
            )
       
            if selection != st.session_state.current_page:
                st.session_state.current_page = selection
                st.rerun()
        
        return st.session_state.current_page

    def render_content(self):
        current_page = self.render_sidebar()

        if current_page == "Networks":
            self.render_network()
        elif current_page == "Reports":
            self.render_reports()
        elif current_page == "Nodes & Edges":
            self.render_data()
        elif current_page == "Settings":
            self.render_settings()

    def render_network(self):
        st.header("🦠 Network Configuration")

        with st.expander("⚙️ Filter & Sort the Graph", expanded=True):

            # Filter by Graph
            fbg_label, fbg_select, fbg_submit, fbg_reset = st.columns([1, 6, 1, 1])

            with fbg_label:
                st.markdown("<p style='margin-top: 3px;'>📂 Filter by Graph:</p>", unsafe_allow_html=True)

            with fbg_select:
                option = st.selectbox(
                    "Select the Graph Root", 
                    ["Option 1", "Option 2", "Option 3", "Option 4"],
                    index=None,
                    placeholder="Select a Graph Root...", 
                    key="fbg_select", 
                    label_visibility="collapsed", 
                    accept_new_options=False, 
                    help="Select the Root Node for your Graph"
                    )

            with fbg_submit:
                if st.button("Submit", key="select_button", use_container_width=True):
                    print('Submit')

            with fbg_reset:
                if st.button("Reset", key="reset_button", use_container_width=True):
                    pass

            # label, select, submit, reset = st.columns([1, 5, 1, 1])

            # with label:
            #     st.markdown("<p style='margin-top: 32px; margin-bottom: 0px;'><b>Filter by Graph:</b></p>", 
            #             unsafe_allow_html=True)

            # with select:
            #     option = st.selectbox("", ["Option 1", "Option 2", "Option 3", "Option 4"], key="dropdown1")

            # with submit:
            #     st.markdown("<div style='margin-top: 26px;'>", unsafe_allow_html=True)
            #     if st.button("Submit", key="select_button", use_container_width=True):
            #         pass  # Handle success message elsewhere if needed
            #     st.markdown("</div>", unsafe_allow_html=True)

            # with reset:
            #     st.markdown("<div style='margin-top: 26px;'>", unsafe_allow_html=True)
            #     if st.button("Reset", key="reset_button", use_container_width=True):
            #         pass  # Handle success message elsewhere if needed
            #     st.markdown("</div>", unsafe_allow_html=True)

            # label, select, submit, reset = st.columns([1, 5, 1, 1])

            # with label:
            #     st.markdown("<p style='margin-top: 32px; margin-bottom: 0px;'><b>Filter by Graph:</b></p>", 
            #             unsafe_allow_html=True)

            # with select:
            #     option = st.selectbox("", ["Option 1", "Option 2", "Option 3", "Option 4"], key="dropdown2")

            # with submit:
            #     st.markdown("<div style='margin-top: 26px;'>", unsafe_allow_html=True)
            #     if st.button("Submit", key="select_button2", use_container_width=True):
            #         pass  # Handle success message elsewhere if needed
            #     st.markdown("</div>", unsafe_allow_html=True)

            # with reset:
            #     st.markdown("<div style='margin-top: 26px;'>", unsafe_allow_html=True)
            #     if st.button("Reset", key="reset_button2", use_container_width=True):
            #         pass  # Handle success message elsewhere if needed
            #     st.markdown("</div>", unsafe_allow_html=True)

            # label, select, submit, reset = st.columns([1, 5, 1, 1])

            # with label:
            #     st.markdown("<p style='margin-top: 32px; margin-bottom: 0px;'><b>Filter by Graph:</b></p>", 
            #             unsafe_allow_html=True)

            # with select:
            #     option = st.selectbox("", ["Option 1", "Option 2", "Option 3", "Option 4"], key="dropdown3")

            # with submit:
            #     st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
            #     if st.button("Submit", key="select_button3", use_container_width=True):
            #         pass
            #     st.markdown("</div>", unsafe_allow_html=True)

            # with reset:
            #     st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
            #     if st.button("Reset", key="reset_button3", use_container_width=True):
            #         pass
            #     st.markdown("</div>", unsafe_allow_html=True)

            # # Main container with data-view attribute
            # st.markdown('<div data-view="networks" class="container-fluid px-4 py-5">', unsafe_allow_html=True)

            # # Filter container
            # st.markdown('<div class="container-fluid mb-0">', unsafe_allow_html=True)

            # # Filter by Graph Name (Single Line, Full Width)
            # st.markdown('''
            # <div class="row mb-3">
            #     <div class="col-12 d-flex align-items-center justify-content-between">
            # ''', unsafe_allow_html=True)

            # st.markdown('<label for="filterGraph" class="col-form-label col-md-1 me-2">Filter by Graph:</label>', unsafe_allow_html=True)

            # # Mock graphs data (replace with your actual data)
            # graphs = [
            #     {"id": "1", "name": "Network Graph 1"},
            #     {"id": "2", "name": "Social Network"},
            #     {"id": "3", "name": "Knowledge Graph"},
            #     {"id": "4", "name": "Transport Network"}
            # ]

            # # Graph selection dropdown
            # graph_options = ["All Graphs"] + [graph["name"] for graph in graphs]
            # selected_graph = st.selectbox(
            #     "Graph",
            #     graph_options,
            #     key="filterGraph",
            #     label_visibility="collapsed"
            # )

            # if st.button("Reset Selection", key="reset_graph", type="primary"):
            #     st.session_state.filterGraph = "All Graphs"
            #     st.rerun()

            # st.markdown('''
            #     </div>
            # </div>
            # ''', unsafe_allow_html=True)

            # # Filters (Single Line, Full Width)
            # st.markdown('''
            # <div class="row mb-0">
            #     <div class="col-12 d-flex align-items-center justify-content-between mb-3">
            # ''', unsafe_allow_html=True)

            # # Filter by Element
            # st.markdown('<label for="filterElement" class="col-form-label col-md-1 me-2">Filter by Element:</label>', unsafe_allow_html=True)

            # element_options = ["All Elements", "Node", "Edges"]
            # selected_element = st.selectbox(
            #     "Element",
            #     element_options,
            #     key="filterElement",
            #     label_visibility="collapsed"
            # )

            # # Filter by Property
            # st.markdown('<label for="filterProperty" class="col-form-label col-md-1 me-2">Filter by Property:</label>', unsafe_allow_html=True)

            # property_options = ["All Properties", "ID", "Identifier", "Name"]
            # selected_property = st.selectbox(
            #     "Property",
            #     property_options,
            #     key="filterProperty",
            #     label_visibility="collapsed"
            # )

            # # Filter by Value
            # st.markdown('<label for="filterValue" class="col-form-label col-md-1 me-2">Filter by Value:</label>', unsafe_allow_html=True)

            # filter_value = st.text_input(
            #     "Value",
            #     placeholder="Enter a Value",
            #     key="filterValue",
            #     label_visibility="collapsed"
            # )

            # # Reset Selection Button
            # if st.button("Reset Selection", key="reset_filter_values", type="primary"):
            #     st.session_state.filterElement = "All Elements"
            #     st.session_state.filterProperty = "All Properties"
            #     st.session_state.filterValue = ""
            #     st.rerun()

            # st.markdown('''
            #     </div>
            # </div>
            # ''', unsafe_allow_html=True)

            # # Close filter container
            # st.markdown('</div>', unsafe_allow_html=True)

            # # Close main container
            # st.markdown('</div>', unsafe_allow_html=True)

            # col1, col2, col3 = st.columns(3)
            # with col1:
            #     if st.button("Apply Filters", type="primary"):
            #         st.success("Filters applied to network visualization!")
                    
            # with col2:
            #     if st.button("Clear All Filters", type="secondary"):
            #         st.session_state.filterGraph = "All Graphs"
            #         st.session_state.filterElement = "All Elements"
            #         st.session_state.filterProperty = "All Properties"
            #         st.session_state.filterValue = ""
            #         st.success("All filters cleared!")
            #         st.rerun()

            # with col3:
            #     if st.button("Export Network Data"):
            #         # Mock export functionality
            #         network_data = {
            #             "filters": {
            #                 "graph": selected_graph,
            #                 "element": selected_element,
            #                 "property": selected_property,
            #                 "value": filter_value
            #             },
            #             "timestamp": st.session_state.get("timestamp", "2024-01-01")
            #         }
            #         st.json(network_data)

        with st.expander("ℹ️ About the Graph", expanded=True):
            st.write("💡 To-Do : Add a Description of the Network and the applied Filters")
            st.write("💡 To-Do : Add Network Metrics")
            st.write("💡 To-Do : Add Option to export Configuration & Filters")

        with st.container(border=True):
            st.subheader("Network Topology")
            self.render_network_graph("detailed")

    def render_network_graph(self, graph_type="simple"):
        """Render network graph using controller data"""
        try:
            graph_data = self.controller.get_network_graph_data(graph_type)
            
            if 'error' in graph_data:
                st.error(f"Error rendering graph: {graph_data['error']}")
                st.write(f"📊 Network Graph ({graph_data.get('fallback_message', 'Fallback')})")
                return
            
            # Convert controller data to agraph format
            nodes = [Node(id=n["id"], label=n["label"], size=n["size"], color=n["color"]) 
                    for n in graph_data["nodes"]]
            
            edges = []
            for e in graph_data["edges"]:
                edge_kwargs = {"source": e["source"], "target": e["target"], "color": e["color"]}
                if "width" in e:
                    edge_kwargs["width"] = e["width"]
                edges.append(Edge(**edge_kwargs))
            
            # Create config object
            config_data = graph_data["config"]
            config = Config(**config_data)
            
            # Render the graph
            return_value = agraph(nodes=nodes, edges=edges, config=config)
            
            # Display information about selected node
            if return_value:
                st.write(f"Selected: {return_value}")
            
            # Display stats if available (for detailed graph)
            # if "stats" in graph_data:
            #     stats = graph_data["stats"]
            #     col1, col2, col3 = st.columns(3)
            #     with col1:
            #         st.metric("Total Nodes", stats["total_nodes"])
            #     with col2:
            #         st.metric("Total Connections", stats["total_connections"])
            #     with col3:
            #         st.metric("Network Layers", stats["network_layers"])
                
        except ImportError:
            st.warning("streamlit-agraph not installed. Install with: pip install streamlit-agraph")
            fallback_message = "📊 Network Graph (Install streamlit-agraph for visualization)"
            if graph_type == "detailed":
                fallback_message = "📊 Detailed Network Topology (Install streamlit-agraph for visualization)"
                st.write(fallback_message)
                st.write("Network Layers: Core → Distribution → Access")
                st.write("13 nodes, 16 connections across 3 network layers")
            else:
                st.write(fallback_message)
                st.write("Nodes: Server A, Server B, Database, Load Balancer, Client, Cache")
                st.write("Connections: 7 active connections")
        except Exception as e:
            st.error(f"Error rendering graph: {e}")

    def render_reports(self):
        st.header("📄 Reports")
        
        available_reports = self.controller.get_available_reports()
        selected_report = st.selectbox("", available_reports)
        
        result = self.controller.generate_report(selected_report)
        self._display_action_result(result)

    def render_data(self):
        """Render the Node and Edge Data Management Interface"""
        st.header("📊 Data Management")

        self.render_data_toolbar()

        edges, nodes, edge_types = st.tabs(["Edges", "Nodes", "Edge Types"])

        with edges:
            self.render_edges_data_editor()

        with nodes:
            self.render_nodes_data_editor()

        with edge_types:
            self.render_edge_types_data_editor()

    def render_data_toolbar(self):
        """Render data management toolbar"""
        st.subheader("Data Management Tools")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Refresh Data", help="Refresh all data from database"):
                st.rerun()
        
        with col2:
            if st.button("✅ Validate Integrity", help="Check database integrity"):
                result = self.controller.validate_database_integrity()
                self._display_action_result(result)
        
        with col3:
            if st.button("📈 Show Statistics", help="Display data statistics"):
                result = self.controller.get_data_statistics()
                if result['status'] == 'success':
                    self.show_data_statistics(result['data'])
                else:
                    self._display_action_result(result)
        
        with col4:
            if st.button("📥 Export All", help="Export all data"):
                st.info("Export functionality available per table")

    def show_data_statistics(self, stats):
        """Display data statistics in an expander"""
        with st.expander("📈 Data Statistics", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Basic Statistics")
                st.write(f"**Total Nodes:** {stats.get('total_nodes', 0)}")
                st.write(f"**Total Edges:** {stats.get('total_edges', 0)}")
                st.write(f"**Edge Types:** {stats.get('edge_types_count', 0)}")
                st.write(f"**Average Node Degree:** {stats.get('avg_node_degree', 0)}")
                st.write(f"**Max Node Degree:** {stats.get('max_node_degree', 0)}")
                st.write(f"**Isolated Nodes:** {stats.get('isolated_nodes', 0)}")
            
            with col2:
                st.subheader("Edge Type Distribution")
                edge_dist = stats.get('edge_type_distribution', {})
                for edge_type, count in edge_dist.items():
                    st.write(f"**{edge_type}:** {count}")

    def render_edges_data_editor(self):
        st.subheader("🔗 Edges Data")
        
        result, error = self.controller.prepare_edges_for_editor()
        
        if error:
            if "Error" in error:
                st.error(error)
            else:
                st.info(error)
            return
        
        # Store original data for change detection
        original_data = result['data'].copy()
        df_edges = pd.DataFrame(result['data'])
        
        # Create toolbar for edges
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Add New Edge", key="add_edge"):
                # Initialize session state for new edge form
                st.session_state.show_add_edge_form = True
        
        with col2:
            if st.button("💾 Save Changes", key="save_edges"):
                if 'edges_editor' in st.session_state:
                    edited_df = st.session_state.edges_editor['edited_rows']
                    if edited_df or st.session_state.edges_editor.get('added_rows'):
                        # Get the current dataframe from session state
                        current_df = pd.DataFrame(st.session_state.edges_editor['data'])
                        result = self.controller.handle_edges_data_changes(current_df, original_data)
                        self._display_action_result(result)
                        if result['status'] == 'success':
                            st.rerun()
                    else:
                        st.info("No changes to save")
        
        with col3:
            selected_edge_ids = st.multiselect(
                "Select edges to delete:",
                options=[row['ID'] for row in original_data],
                key="edges_to_delete"
            )
            
            if selected_edge_ids and st.button("🗑️ Delete Selected", key="delete_edges"):
                self.handle_bulk_delete_edges(selected_edge_ids)

        # Show add edge form if requested
        if st.session_state.get('show_add_edge_form', False):
            self.render_add_edge_form(result)
        
        # Column configuration for the data editor
        column_config = {
            "ID": st.column_config.TextColumn("ID", width="small", disabled=True),
            "Source ID": None,  # Hide this column
            "Source": st.column_config.SelectboxColumn(
                "Source",
                options=result['node_options'],
                required=True,
                width="medium"
            ),
            "Edge Type": st.column_config.SelectboxColumn(
                "Edge Type",
                options=result['edge_type_options'],
                required=True,
                width="medium"
            ),
            "Target ID": None,  # Hide this column
            "Target": st.column_config.SelectboxColumn(
                "Target", 
                options=result['node_options'],
                required=True,
                width="medium"
            ),
            "Description": st.column_config.TextColumn("Description", width="large")
        }

        # Data editor
        edited_df = st.data_editor(
            df_edges,
            width='stretch',
            num_rows="dynamic",
            disabled=["ID", "Source ID", "Target ID"],
            column_config=column_config,
            key="edges_editor",
            use_container_width=True
        )

    def render_add_edge_form(self, result):
        """Render form to add a new edge"""
        with st.form("add_edge_form"):
            st.subheader("Add New Edge")
            
            col1, col2 = st.columns(2)
            
            with col1:
                source = st.selectbox("Source Node", result['node_options'])
                edge_type = st.selectbox("Edge Type", result['edge_type_options'])
            
            with col2:
                target = st.selectbox("Target Node", result['node_options'])
                description = st.text_input("Description", value="None")
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("Create Edge")
            
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                if source and target and edge_type:
                    result = self.controller.create_edge(source, target, edge_type, description)
                    self._display_action_result(result)
                    if result['status'] == 'success':
                        st.session_state.show_add_edge_form = False
                        st.rerun()
                else:
                    st.error("Please fill in all required fields")
            
            if cancel:
                st.session_state.show_add_edge_form = False
                st.rerun()

    def handle_bulk_delete_edges(self, edge_ids):
        """Handle bulk deletion of edges"""
        success_count = 0
        error_count = 0
        
        for edge_id in edge_ids:
            result = self.controller.delete_edge(edge_id)
            if result['status'] == 'success':
                success_count += 1
            else:
                error_count += 1
        
        if success_count > 0:
            st.success(f"Successfully deleted {success_count} edge(s)")
        if error_count > 0:
            st.error(f"Failed to delete {error_count} edge(s)")
        
        if success_count > 0:
            st.rerun()

    def render_nodes_data_editor(self):
        st.subheader("🔵 Nodes Data")
        
        result, error = self.controller.prepare_nodes_for_editor()
        
        if error:
            if "Error" in error:
                st.error(error)
            else:
                st.info(error)
            return
        
        # Store original data for change detection
        original_data = result['data'].copy()
        df_nodes = pd.DataFrame(result['data'])
        
        # Create toolbar for nodes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Add New Node", key="add_node"):
                st.session_state.show_add_node_form = True
        
        with col2:
            if st.button("💾 Save Changes", key="save_nodes"):
                if 'nodes_editor' in st.session_state:
                    edited_df = st.session_state.nodes_editor['edited_rows']
                    if edited_df or st.session_state.nodes_editor.get('added_rows'):
                        current_df = pd.DataFrame(st.session_state.nodes_editor['data'])
                        result = self.controller.handle_nodes_data_changes(current_df, original_data)
                        self._display_action_result(result)
                        if result['status'] == 'success':
                            st.rerun()
                    else:
                        st.info("No changes to save")
        
        with col3:
            selected_node_ids = st.multiselect(
                "Select nodes to delete:",
                options=[row['ID'] for row in original_data],
                key="nodes_to_delete"
            )
            
            if selected_node_ids and st.button("🗑️ Delete Selected", key="delete_nodes"):
                self.handle_bulk_delete_nodes(selected_node_ids)

        # Show add node form if requested
        if st.session_state.get('show_add_node_form', False):
            self.render_add_node_form()
        
        # Column configuration
        column_config = {
            "ID": st.column_config.TextColumn("ID", width="small", disabled=True),
            "Name": st.column_config.TextColumn("Name", width="medium", required=True),
            "Description": st.column_config.TextColumn("Description", width="large")
        }

        # Data editor
        edited_df = st.data_editor(
            df_nodes,
            width='stretch',
            num_rows="dynamic",
            disabled=["ID"],
            column_config=column_config,
            key="nodes_editor",
            use_container_width=True
        )

    def render_add_node_form(self):
        """Render form to add a new node"""
        with st.form("add_node_form"):
            st.subheader("Add New Node")
            
            name = st.text_input("Name", placeholder="Enter node name")
            description = st.text_area("Description", value="None")
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("Create Node")
            
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                if name:
                    result = self.controller.create_node(name, description)
                    self._display_action_result(result)
                    if result['status'] == 'success':
                        st.session_state.show_add_node_form = False
                        st.rerun()
                else:
                    st.error("Please enter a node name")
            
            if cancel:
                st.session_state.show_add_node_form = False
                st.rerun()

    def handle_bulk_delete_nodes(self, node_ids):
        """Handle bulk deletion of nodes"""
        success_count = 0
        error_count = 0
        
        for node_id in node_ids:
            result = self.controller.delete_node(node_id)
            if result['status'] == 'success':
                success_count += 1
            else:
                error_count += 1
        
        if success_count > 0:
            st.success(f"Successfully deleted {success_count} node(s)")
        if error_count > 0:
            st.error(f"Failed to delete {error_count} node(s)")
        
        if success_count > 0:
            st.rerun()

    def render_edge_types_data_editor(self):
        st.subheader("🏷️ Edge Types Data")
        
        result, error = self.controller.prepare_edge_types_for_editor()
        
        if error:
            if "Error" in error:
                st.error(error)
            else:
                st.info(error)
                if "No edge types found" in error:
                    if st.button("Add Sample Edge Type", key="add_sample_edge_type"):
                        sample_result = self.controller.create_edge_type("connects", "Basic connection type")
                        self._display_action_result(sample_result)
                        if sample_result['status'] == 'success':
                            st.rerun()
            return
        
        # Store original data for change detection
        original_data = result['data'].copy()
        df_edge_types = pd.DataFrame(result['data'])
        
        # Create toolbar for edge types
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Add New Edge Type", key="add_edge_type"):
                st.session_state.show_add_edge_type_form = True
        
        with col2:
            if st.button("💾 Save Changes", key="save_edge_types"):
                if 'edge_types_editor' in st.session_state:
                    edited_df = st.session_state.edge_types_editor['edited_rows']
                    if edited_df or st.session_state.edge_types_editor.get('added_rows'):
                        current_df = pd.DataFrame(st.session_state.edge_types_editor['data'])
                        result = self.controller.handle_edge_types_data_changes(current_df, original_data)
                        self._display_action_result(result)
                        if result['status'] == 'success':
                            st.rerun()
                    else:
                        st.info("No changes to save")
        
        with col3:
            selected_edge_type_ids = st.multiselect(
                "Select edge types to delete:",
                options=[row['ID'] for row in original_data],
                key="edge_types_to_delete"
            )
            
            if selected_edge_type_ids and st.button("🗑️ Delete Selected", key="delete_edge_types"):
                self.handle_bulk_delete_edge_types(selected_edge_type_ids)

        # Show add edge type form if requested
        if st.session_state.get('show_add_edge_type_form', False):
            self.render_add_edge_type_form()
        
        # Column configuration
        column_config = {
            "ID": st.column_config.TextColumn("ID", width="small", disabled=True),
            "Name": st.column_config.TextColumn("Name", width="medium", required=True),
            "Description": st.column_config.TextColumn("Description", width="large")
        }

        # Data editor
        edited_df = st.data_editor(
            df_edge_types,
            width='stretch',
            num_rows="dynamic",
            disabled=["ID"],
            column_config=column_config,
            key="edge_types_editor",
            use_container_width=True
        )

    def render_add_edge_type_form(self):
        """Render form to add a new edge type"""
        with st.form("add_edge_type_form"):
            st.subheader("Add New Edge Type")
            
            name = st.text_input("Name", placeholder="Enter edge type name")
            description = st.text_area("Description", value="None")
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("Create Edge Type")
            
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                if name:
                    result = self.controller.create_edge_type(name, description)
                    self._display_action_result(result)
                    if result['status'] == 'success':
                        st.session_state.show_add_edge_type_form = False
                        st.rerun()
                else:
                    st.error("Please enter an edge type name")
            
            if cancel:
                st.session_state.show_add_edge_type_form = False
                st.rerun()

    def handle_bulk_delete_edge_types(self, edge_type_ids):
        """Handle bulk deletion of edge types"""
        success_count = 0
        error_count = 0
        
        for edge_type_id in edge_type_ids:
            result = self.controller.delete_edge_type(edge_type_id)
            if result['status'] == 'success':
                success_count += 1
            else:
                error_count += 1
        
        if success_count > 0:
            st.success(f"Successfully deleted {success_count} edge type(s)")
        if error_count > 0:
            st.error(f"Failed to delete {error_count} edge type(s)")
        
        if success_count > 0:
            st.rerun()

    def render_settings(self):
        st.header("⚙️ Settings")
        st.subheader("Application Settings")
        
        current_settings = self.controller.get_app_settings()
        
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], 
                           index=["Light", "Dark", "Auto"].index(current_settings.get('theme', 'Light')))
        notifications = st.checkbox("Enable Notifications", value=current_settings.get('notifications', True))
        auto_save = st.checkbox("Auto-save Changes", value=current_settings.get('auto_save', True))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Settings"):
                result = self.controller.save_app_settings(theme, notifications, auto_save)
                self._display_action_result(result)
        
        with col2:
            if st.button("Reset to Default"):
                result = self.controller.reset_app_settings()
                self._display_action_result(result)

    # ==================== HELPER METHODS ====================

    def _display_action_result(self, result):
        """Helper method to display action results consistently"""
        if not result or result.get("status") == "none":
            return
        
        status = result.get("status", "info")
        message = result.get("message", "")
        
        if status == "success":
            st.success(message)
        elif status == "error":
            st.error(message)
        elif status == "warning":
            st.warning(message)
        elif status == "info":
            st.info(message)

    def show_message(self, message, message_type="info"):
        """Display messages to the user"""
        if message_type == "info":
            st.info(message)
        elif message_type == "error":
            st.error(message)
        elif message_type == "success":
            st.success(message)
        elif message_type == "warning":
            st.warning(message)

    def show_loading(self, message="Loading..."):
        """Show loading spinner"""
        return st.spinner(message)

    def show_progress(self, value, message=""):
        """Show progress bar"""
        st.progress(value)
        if message:
            st.write(message)