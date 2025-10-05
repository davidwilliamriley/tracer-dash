# utils/network_cache.py

"""Centralized cache for the NetworkX Graph"""

_cached_network = None

def get_network():
    global _cached_network
    return _cached_network

def update_network_cache(graph):
    global _cached_network
    _cached_network = graph
    print(f"[update_network_cache] Cached network with {graph.number_of_nodes()} nodes")

def invalidate_network_cache():
    global _cached_network
    _cached_network = None
    print("[invalidate_network_cache] Cache cleared")