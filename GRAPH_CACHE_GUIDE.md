# Graph Store with dcc.Store Components

This documentation explains how to use the new `dcc.Store`-based graph caching system for the Tracer-Dash application.

## Overview

The graph caching system uses Dash's native `dcc.Store` components to cache NetworkX graph data on the client-side, improving performance by avoiding unnecessary database queries and graph rebuilding operations.

## Components

### 1. dcc.Store Components

The following stores are used in the networks page:

- `network-data-store`: Stores the current network visualization data (Cytoscape format)
- `graph-cache-store`: Caches serialized NetworkX graph data
- `graph-metadata-store`: Stores metadata about cached graphs (node counts, timestamps, etc.)
- `cache-timestamp-store`: Tracks when caches were last updated
- `cache-invalidation-store`: Manages cache invalidation signals

### 2. Utility Classes

#### GraphCacheUtils

Provides utilities for working with NetworkX graphs in dcc.Store:

```python
from utils.graph_cache_utils import GraphCacheUtils

# Serialize a NetworkX graph for dcc.Store
serialized_data = GraphCacheUtils.serialize_networkx_graph(graph)

# Deserialize graph data from dcc.Store
graph = GraphCacheUtils.deserialize_networkx_graph(serialized_data)

# Check if cached data is still valid
is_valid = GraphCacheUtils.is_cache_valid(cache_data, max_age_seconds=300)

# Convert Cytoscape data to NetworkX
graph = GraphCacheUtils.convert_cytoscape_to_networkx(cytoscape_data)
```

#### CacheInvalidationManager

Manages cache invalidation when data changes:

```python
from utils.cache_invalidation import CacheInvalidationManager

# Create invalidation signal for node changes
signal = CacheInvalidationManager.get_node_change_signal("node_123", "created")

# Check if cache should be invalidated
should_invalidate = CacheInvalidationManager.should_invalidate_cache(current_signal, last_signal)
```

### 3. NetworksController Updates

The `NetworksController` now includes methods for cache management:

```python
controller = NetworksController()

# Get graph data formatted for caching
cache_data = controller.get_graph_for_cache()

# Get cache metadata
metadata = controller.get_cache_metadata()

# Restore graph from cached data
graph = controller.restore_graph_from_cache(cached_data)
```

## Usage Examples

### Basic Caching

The system automatically caches graph data when the networks page is loaded. The cache is stored in the browser session and will persist until the session ends.

### Cache Invalidation

To invalidate the cache when data changes (e.g., after creating/updating nodes or edges):

```python
from utils.cache_invalidation import CacheInvalidationManager

# In your callback that modifies data:
@callback(
    Output('cache-invalidation-store', 'data'),
    Input('some-button', 'n_clicks')
)
def handle_data_change(n_clicks):
    if n_clicks:
        # Perform data modification
        # ...
        
        # Create invalidation signal
        signal = CacheInvalidationManager.get_node_change_signal("node_id", "created")
        return signal
    
    return no_update
```

### Custom Cache Management

You can create custom callbacks to manage caching behavior:

```python
@callback(
    Output('graph-cache-store', 'data'),
    [Input('cache-invalidation-store', 'data'),
     Input('network-data-store', 'data')],
    State('graph-cache-store', 'data')
)
def manage_custom_cache(invalidation_signal, network_data, current_cache):
    # Custom logic for cache management
    if CacheInvalidationManager.should_invalidate_cache(invalidation_signal, current_cache_signal):
        # Rebuild cache
        return new_cache_data
    
    return no_update
```

## Benefits

1. **Performance**: Avoids rebuilding NetworkX graphs from database on every page load
2. **Client-side Storage**: Uses browser storage, reducing server load
3. **Session Persistence**: Cache persists during browser session
4. **Native Integration**: Uses Dash's built-in storage mechanisms
5. **Flexible Invalidation**: Easy to invalidate cache when data changes

## Configuration

### Cache Expiration

Default cache expiration is 5 minutes (300 seconds). You can adjust this:

```python
is_valid = GraphCacheUtils.is_cache_valid(cache_data, max_age_seconds=600)  # 10 minutes
```

### Storage Types

- `memory`: Data cleared when page refreshes
- `session`: Data persists during browser session
- `local`: Data persists across browser sessions

Choose the appropriate storage type based on your needs:

```python
dcc.Store(id='my-cache-store', storage_type='local')  # Persistent across sessions
```

## Best Practices

1. **Cache Validation**: Always check if cached data is valid before using it
2. **Error Handling**: Wrap cache operations in try-catch blocks
3. **Metadata**: Store metadata alongside cached data for better management
4. **Selective Invalidation**: Only invalidate cache when necessary to maintain performance
5. **Size Limits**: Be aware of browser storage limits for large graphs

## Migration Notes

This system replaces the previous GraphStore singleton approach with a more Dash-native solution using dcc.Store components. The benefits include:

- Better integration with Dash's reactive system
- Client-side storage reducing server memory usage
- Easier debugging through Dash dev tools
- More flexible cache management options