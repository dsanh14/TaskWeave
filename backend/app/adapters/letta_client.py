"""Letta Cloud client adapter with in-memory fallback."""
from typing import Optional
import httpx
from app.config import settings
from app.util.logging import log_info, log_warning
from app.models.domain import MemoryPrefs


class LettaClient:
    """Client for Letta Cloud with in-memory fallback."""
    
    def __init__(self):
        self.api_key = settings.letta_api_key
        self.base_url = settings.letta_base_url
        # In-memory storage as fallback
        self._memory_store: dict[str, MemoryPrefs] = {}
        
    async def get_prefs(self, user_id: str) -> MemoryPrefs:
        """Get user preferences from Letta.
        
        Args:
            user_id: User ID
            
        Returns:
            MemoryPrefs: User preferences (defaults if not found)
        """
        if not self.api_key:
            log_warning("No Letta API key, using in-memory storage")
            return self._get_from_memory(user_id)
        
        try:
            # In a real implementation, this would call Letta API
            # For MVP, use in-memory storage
            log_warning("Letta Cloud integration pending, using in-memory")
            return self._get_from_memory(user_id)
            
        except Exception as e:
            log_warning(f"Letta API call failed: {e}, using in-memory")
            return self._get_from_memory(user_id)
    
    async def upsert_prefs(self, prefs: MemoryPrefs) -> MemoryPrefs:
        """Save user preferences to Letta.
        
        Args:
            prefs: Preferences to save
            
        Returns:
            MemoryPrefs: Saved preferences
        """
        if not self.api_key:
            log_warning("No Letta API key, using in-memory storage")
            return self._save_to_memory(prefs)
        
        try:
            # In a real implementation, this would call Letta API
            # For MVP, use in-memory storage
            log_warning("Letta Cloud integration pending, using in-memory")
            return self._save_to_memory(prefs)
            
        except Exception as e:
            log_warning(f"Letta API call failed: {e}, using in-memory")
            return self._save_to_memory(prefs)
    
    def _get_from_memory(self, user_id: str) -> MemoryPrefs:
        """Get preferences from in-memory store."""
        if user_id in self._memory_store:
            log_info(f"Retrieved memory for user {user_id}")
            return self._memory_store[user_id]
        
        log_info(f"No memory found for user {user_id}, returning defaults")
        return MemoryPrefs(user_id=user_id)
    
    def _save_to_memory(self, prefs: MemoryPrefs) -> MemoryPrefs:
        """Save preferences to in-memory store."""
        self._memory_store[prefs.user_id] = prefs
        log_info(f"Saved memory for user {prefs.user_id}")
        return prefs


# Global client instance
letta_client = LettaClient()

