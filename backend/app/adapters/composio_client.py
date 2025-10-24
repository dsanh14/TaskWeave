"""Composio Toolrouter client adapter with dry-run fallback."""
import httpx
from app.config import settings
from app.util.logging import log_info, log_warning
from app.models.domain import EventBlock


class ComposioClient:
    """Client for Composio Toolrouter with dry-run fallback."""
    
    def __init__(self):
        self.api_key = settings.composio_api_key
        self.base_url = settings.composio_base_url
        
    async def apply_calendar(
        self,
        blocks: list[EventBlock],
        dry_run: bool = True
    ) -> int:
        """Apply event blocks to Google Calendar.
        
        Args:
            blocks: Event blocks to apply
            dry_run: If True, simulate without actual changes
            
        Returns:
            int: Number of blocks applied
        """
        if not self.api_key or dry_run:
            if not self.api_key:
                log_warning("No Composio API key, dry-run mode enabled")
            else:
                log_info("Dry-run mode: simulating calendar apply")
            return self._dry_run_apply(blocks)
        
        try:
            # In a real implementation, this would call Composio API
            # For MVP, always use dry-run
            log_warning("Composio integration pending, using dry-run")
            return self._dry_run_apply(blocks)
            
        except Exception as e:
            log_warning(f"Composio API call failed: {e}, using dry-run")
            return self._dry_run_apply(blocks)
    
    def _dry_run_apply(self, blocks: list[EventBlock]) -> int:
        """Simulate applying blocks to calendar."""
        log_info(f"DRY-RUN: Would apply {len(blocks)} blocks to calendar")
        
        for block in blocks:
            log_info(
                f"DRY-RUN: {block.title} | {block.start_iso} → {block.end_iso} | "
                f"source={block.source_agent}"
            )
        
        return len(blocks)


# Global client instance
composio_client = ComposioClient()

