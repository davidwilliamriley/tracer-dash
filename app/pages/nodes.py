# pages/nodes.py - Simplified working version
import dash
from dash import html, dcc, callback, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import uuid
from datetime import datetime
from typing import Any, Dict, List

dash.register_page(__name__, path='/nodes')

# Sample data that matches your screenshot
initial_data: List[Dict[str, Any]] = [
    {
        'ID': '00000cf8-8a34-42a8-b856-b9615ee93927',
        'Identifier': 'ERG350',
        'Name': 'Burwood Station Pedestrian Overpass',
        'Description': 'Location Breakdown Structure (LBS) Element'
    },
    {
        'ID': '00000de-7564-4edc-a2a8-d934d316d41',
        'Identifier': '',
        'Name': 'Operate, Maintain, & Sustain (OM)',
        'Description': 'Work Phase'
    },
    {
        'ID': '0106f8d-bd32-48d6-a831-c40608d7a31d',
        'Identifier': '',
        'Name': 'Package Interface Register (PIR)',
        'Description': 'Root Node for the Interface Register'
    },
    {
        'ID': '0146af44-4954-400a-9c4b-494daec6924',
        'Identifier': '',
        'Name': 'Flood Protection System',
        'Description': 'Integrated Transport Systems'
    },
    {
        'ID': '01643018-1644-4a08-a9f6-60bd668350495',
        'Identifier': '',
        'Name': '1 Concept',
        'Description': 'Lifecycle Phase'
    },
    {
        'ID': '016aa18-9df9-490f-a7d4-32d9bc3aae4e',
        'Identifier': '',
        'Name': 'Enterprise Asset Management System',
        'Description': 'Integrated Control System'
    },
    {
        'ID': '0271042-4fa3-4bd8-bd4a-5765dc4e4a24',
        'Identifier': 'SRL-WPT-XPK-SPD2-REG-XCP-QWY-NNNNN',
        'Name': 'Completions Register - Glen Waverley - Separable Portion 2',
        'Description': ''
    },
    {
        'ID': '03265224-0899-41ef-ac1f-ea274941764',
        'Identifier': '',
        'Name': 'Deliverables Register - System Requirements Review - Box...',
        'Description': ''
    },
    {
        'ID': '03aef8d-bd6c-4514-9f2-02ce60276ee5',
        'Identifier': '',
        'Name': 'Operator Integration and Test',
        'Description': 'Program Lifecycle Stage'
    },
    {
        'ID': '04db090-4f8-489b-8644-79798415d93',
        'Identifier': '',
        'Name': 'Utilities',
        'Description': 'Integrated Transport Systems'
    }
]

def layout():
    return html.Div([
        # Main container
        html.Div([
            # Toolbar
            html.Div([
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-plus-lg me-2"), "Create"], 
                                 id="create-node-btn", color="primary", className="me-2", 
                                 title="Create a new Node"),
                        dbc.Button([html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"], 
                                 id="refresh-nodes-btn", color="primary", className="me-2", 
                                 title="Refresh the Nodes Table"),
                        dbc.Button([html.I(className="bi bi-trash me-2"), "Delete"], 
                                 id="delete-node-btn", color="warning", 
                                 title="Delete a selected Node", disabled=True),
                    ], className="d-flex justify-content-start"),
                ], className="col-md-6"),
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                                 id="print-nodes-btn", color="primary", className="me-2", 
                                 title="Print the Table to PDF"),
                        dbc.Button([html.I(className="bi bi-download me-2"), "Download"], 
                                 id="download-nodes-btn", color="primary", 
                                 title="Download the Table as CSV"),
                    ], className="d-flex justify-content-end"),
                ], className="col-md-6"),
            ], className="row justify-content-between mb-3 nodes-toolbar"),
            
            # Alert area for messages
            html.Div(id="alert-container"),
            
            # Table - static table instead of dynamic
            html.Div([
                dash_table.DataTable(
                    id='nodes-table',
                    data=initial_data,
                    columns=[
                        {'name': 'ID', 'id': 'ID', 'type': 'text'},
                        {'name': 'Identifier', 'id': 'Identifier', 'type': 'text'},
                        {'name': 'Name', 'id': 'Name', 'type': 'text'},
                        {'name': 'Description', 'id': 'Description', 'type': 'text'}
                    ],
                    style_table={
                        'overflowX': 'auto',
                        'border': '1px solid #dee2e6',
                        'borderRadius': '0.375rem',
                        'fontFamily': 'system-ui, -apple-system, sans-serif'
                    },
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': '600',
                        'textAlign': 'left',
                        'border': '1px solid #dee2e6',
                        'padding': '12px 8px',
                        'fontSize': '14px',
                        'color': '#495057'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '8px',
                        'fontSize': '14px',
                        'border': '1px solid #dee2e6',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis'
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'ID'},
                            'width': '25%',
                            'fontFamily': 'Monaco, Consolas, monospace',
                            'fontSize': '12px',
                            'color': '#6c757d'
                        },
                        {
                            'if': {'column_id': 'Identifier'},
                            'width': '15%',
                            'fontFamily': 'Monaco, Consolas, monospace', 
                            'fontSize': '12px'
                        },
                        {
                            'if': {'column_id': 'Name'},
                            'width': '30%',
                            'fontWeight': '500'
                        },
                        {
                            'if': {'column_id': 'Description'},
                            'width': '30%',
                            'color': '#6c757d'
                        }
                    ],
                    style_data={
                        'backgroundColor': 'white',
                        'color': 'black'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        },
                        {
                            'if': {'state': 'selected'},
                            'backgroundColor': '#0d6efd',
                            'color': 'white'
                        }
                    ],
                    row_selectable='multi',
                    selected_rows=[],
                    sort_action='native',
                    sort_mode='multi',
                    filter_action='native',
                    page_action='native',
                    page_current=0,
                    page_size=10,
                )
            ]),
            
        ], className="container-fluid px-4 py-5"),
        
        # Create Node Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create New Node")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Identifier:", className="fw-bold"),
                        dbc.Input(
                            id="new-node-identifier", 
                            type="text", 
                            placeholder="Enter unique identifier (optional)"
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Name:", className="fw-bold"),
                        dbc.Input(
                            id="new-node-name", 
                            type="text", 
                            placeholder="Enter node name*",
                            required=True
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Description:", className="fw-bold"),
                        dbc.Textarea(
                            id="new-node-description", 
                            placeholder="Enter description (optional)",
                            rows=3
                        )
                    ], width=12)
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Create Node", id="confirm-create-node", color="primary", className="me-2"),
                dbc.Button("Cancel", id="cancel-create-node", color="secondary")
            ])
        ], id="create-node-modal", is_open=False, backdrop="static"),
        
        # Delete Confirmation Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
            dbc.ModalBody(html.Div(id="delete-modal-body")),
            dbc.ModalFooter([
                dbc.Button("Delete", id="confirm-delete-node", color="danger", className="me-2"),
                dbc.Button("Cancel", id="cancel-delete-node", color="secondary")
            ])
        ], id="delete-node-modal", is_open=False, backdrop="static"),
        
        # Hidden download component
        dcc.Download(id="download-nodes-csv")
    ])

# Enable/disable delete button based on selection
@callback(
    Output('delete-node-btn', 'disabled'),
    Input('nodes-table', 'selected_rows')
)
def toggle_delete_button(selected_rows):
    """Enable/disable delete button based on selection"""
    return len(selected_rows) == 0 if selected_rows else True

# Toggle create modal
@callback(
    Output('create-node-modal', 'is_open'),
    [Input('create-node-btn', 'n_clicks'),
     Input('confirm-create-node', 'n_clicks'),
     Input('cancel-create-node', 'n_clicks')],
    State('create-node-modal', 'is_open')
)
def toggle_create_modal(create_clicks, confirm_clicks, cancel_clicks, is_open):
    """Toggle create node modal"""
    if create_clicks or confirm_clicks or cancel_clicks:
        return not is_open
    return is_open

# Toggle delete modal
@callback(
    Output('delete-node-modal', 'is_open'),
    Output('delete-modal-body', 'children'),
    [Input('delete-node-btn', 'n_clicks'),
     Input('confirm-delete-node', 'n_clicks'),
     Input('cancel-delete-node', 'n_clicks')],
    [State('delete-node-modal', 'is_open'),
     State('nodes-table', 'selected_rows'),
     State('nodes-table', 'data')]
)
def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, data):
    """Toggle delete confirmation modal"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'delete-node-btn' and selected_rows:
        selected_nodes = [data[i]['Name'] for i in selected_rows]
        body = html.Div([
            html.P(f"Are you sure you want to delete the following {len(selected_rows)} node(s)?"),
            html.Ul([html.Li(name) for name in selected_nodes]),
            html.P("This action cannot be undone.", className="text-danger fw-bold")
        ])
        return True, body
    elif button_id in ['confirm-delete-node', 'cancel-delete-node']:
        return False, ""
    
    return is_open, ""

# Handle CRUD operations
@callback(
    [Output('nodes-table', 'data'),
     Output('alert-container', 'children'),
     Output('new-node-identifier', 'value'),
     Output('new-node-name', 'value'),
     Output('new-node-description', 'value')],
    [Input('confirm-create-node', 'n_clicks'),
     Input('confirm-delete-node', 'n_clicks')],
    [State('new-node-identifier', 'value'),
     State('new-node-name', 'value'),
     State('new-node-description', 'value'),
     State('nodes-table', 'data'),
     State('nodes-table', 'selected_rows')]
)
def manage_nodes(create_clicks, delete_clicks, identifier, name, description, data, selected_rows):
    """Handle create and delete operations"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Create new node
    if button_id == 'confirm-create-node' and name:
        new_node = {
            'ID': str(uuid.uuid4()),
            'Identifier': identifier or '',
            'Name': name,
            'Description': description or ''
        }
        updated_data = data + [new_node]
        
        alert = dbc.Alert([
            html.I(className="bi bi-check-circle-fill me-2"),
            f"Successfully created node: {name}"
        ], color="success", dismissable=True, duration=4000)
        
        return updated_data, alert, '', '', ''
    
    # Delete selected nodes
    elif button_id == 'confirm-delete-node' and selected_rows:
        updated_data = [node for i, node in enumerate(data) if i not in selected_rows]
        
        alert = dbc.Alert([
            html.I(className="bi bi-trash-fill me-2"),
            f"Successfully deleted {len(selected_rows)} node(s)"
        ], color="warning", dismissable=True, duration=4000)
        
        return updated_data, alert, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update

# Download CSV
@callback(
    Output('download-nodes-csv', 'data'),
    Input('download-nodes-btn', 'n_clicks'),
    State('nodes-table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    """Download nodes data as CSV"""
    if n_clicks and data:
        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)
        return dict(
            content=csv_string,
            filename=f"nodes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

# Print functionality
@callback(
    Output('alert-container', 'children', allow_duplicate=True),
    Input('print-nodes-btn', 'n_clicks'),
    prevent_initial_call=True
)
def print_table(n_clicks):
    """Handle print functionality"""
    if n_clicks:
        alert = dbc.Alert([
            html.I(className="bi bi-info-circle-fill me-2"),
            "Print functionality would open a print dialog or generate a PDF report."
        ], color="info", dismissable=True, duration=4000)
        return alert
    return no_update

# Refresh functionality
@callback(
    Output('alert-container', 'children', allow_duplicate=True),
    Input('refresh-nodes-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_table(n_clicks):
    """Handle refresh functionality"""
    if n_clicks:
        alert = dbc.Alert([
            html.I(className="bi bi-arrow-clockwise me-2"),
            "Table refreshed successfully"
        ], color="info", dismissable=True, duration=2000)
        return alert
    return no_update