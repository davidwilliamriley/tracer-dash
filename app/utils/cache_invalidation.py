#!/usr/bin/env python3

# utils/cache_invalidation.py - Utilities for invalidating graph caches when data changes

from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CacheInvalidationManager:
    """
    Manages cache invalidation for graph data stored in dcc.Store components.
    This class provides utilities to trigger cache updates when underlying data changes.
    """
    
    @staticmethod
    def create_invalidation_signal(reason: str, affected_entities: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create an invalidation signal that can trigger cache updates.
        
        Args:
            reason: Reason for cache invalidation (e.g., 'node_created', 'edge_deleted')
            affected_entities: Optional dict of entities that were affected
            
        Returns:
            Dictionary containing invalidation signal data
        """
        return {
            'invalidation_id': f"{reason}_{int(datetime.now().timestamp())}",
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'affected_entities': affected_entities or {},
            'cache_version_required': '1.0'
        }
    
    @staticmethod
    def should_invalidate_cache(current_signal: Optional[Dict[str, Any]], 
                              last_cache_signal: Optional[Dict[str, Any]]) -> bool:
        """
        Determine if cache should be invalidated based on signals.
        
        Args:
            current_signal: Current invalidation signal
            last_cache_signal: Signal from when cache was last updated
            
        Returns:
            True if cache should be invalidated
        """
        if not current_signal:
            return False
            
        if not last_cache_signal:
            return True
            
        # Compare invalidation IDs to see if there's been a change
        current_id = current_signal.get('invalidation_id')
        last_id = last_cache_signal.get('invalidation_id')
        
        return current_id != last_id
    
    @staticmethod
    def get_node_change_signal(node_id: str, action: str) -> Dict[str, Any]:
        """Create invalidation signal for node changes."""
        return CacheInvalidationManager.create_invalidation_signal(
            f"node_{action}",
            {'entity_type': 'node', 'entity_id': node_id, 'action': action}
        )
    
    @staticmethod
    def get_edge_change_signal(edge_id: str, action: str) -> Dict[str, Any]:
        """Create invalidation signal for edge changes."""
        return CacheInvalidationManager.create_invalidation_signal(
            f"edge_{action}",
            {'entity_type': 'edge', 'entity_id': edge_id, 'action': action}
        )
    
    @staticmethod
    def get_bulk_change_signal(changes: Dict[str, int]) -> Dict[str, Any]:
        """Create invalidation signal for bulk changes."""
        return CacheInvalidationManager.create_invalidation_signal(
            "bulk_changes",
            changes
        )