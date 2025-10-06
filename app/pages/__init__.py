# pages/__init__.py

# Import all page modules to register them with Dash
from . import index
from . import dashboards  
from . import networks
from . import breakdowns
from . import edges
from . import nodes
from . import edge_types
from . import help
from . import reports
from . import settings

__all__ = [
    'index',
    'dashboards', 
    'networks',
    'breakdowns',
    'edges', 
    'nodes',
    'edge_types',
    'help',
    'reports',
    'settings'
]