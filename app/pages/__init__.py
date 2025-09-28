
# pages/__init__.py

modules_to_import = [
    'breakdowns',
    'dashboards',
    'edge_types',
    'edges',
    'help',
    'index',
    'networks',
    'nodes',
    'reports',
    'settings'
]

imported_modules = []

for module_name in modules_to_import:
    try:
        module = __import__(f'pages.{module_name}', fromlist=[module_name])
        imported_modules.append(module_name)
        globals()[module_name] = module
    except ImportError:
        print(f"Warning: {module_name} module not found - skipping import")

__all__ = imported_modules