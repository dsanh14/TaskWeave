"""Timeline service for merging and managing event blocks."""
from datetime import datetime, time
from typing import Optional
from app.models.domain import EventBlock, MemoryPrefs
from app.util.logging import log_info


class TimelineService:
    """Service for timeline management with conflict resolution."""
    
    def merge_blocks(
        self,
        blocks: list[EventBlock],
        memory: MemoryPrefs
    ) -> list[EventBlock]:
        """Merge event blocks with conflict resolution.
        
        Rules:
        1. Never schedule inside [sleep_start, sleep_end)
        2. Resolve overlaps by shifting forward to next free slot
        3. Keep events within 08:00–22:00
        4. Sort by start time, then agent name
        
        Args:
            blocks: Raw event blocks from agents
            memory: User preferences
            
        Returns:
            list[EventBlock]: Merged, conflict-free timeline
        """
        log_info(f"Merging {len(blocks)} blocks")
        
        # Parse sleep window
        sleep_start = self._parse_time(memory.sleep_start)
        sleep_end = self._parse_time(memory.sleep_end)
        work_start = time(8, 0)
        work_end = time(22, 0)
        
        # Filter out blocks in sleep window
        valid_blocks = []
        for block in blocks:
            block_time = datetime.fromisoformat(block.start_iso).time()
            
            # Check if block starts during sleep
            if self._is_in_sleep_window(block_time, sleep_start, sleep_end):
                log_info(f"Skipping block in sleep window: {block.title}")
                continue
            
            # Check if block is in work hours
            if not (work_start <= block_time <= work_end):
                log_info(f"Skipping block outside work hours: {block.title}")
                continue
                
            valid_blocks.append(block)
        
        # Sort by start time, then source agent
        sorted_blocks = sorted(
            valid_blocks,
            key=lambda b: (b.start_iso, b.source_agent)
        )
        
        # Resolve overlaps
        merged: list[EventBlock] = []
        
        for block in sorted_blocks:
            if not merged:
                merged.append(block)
                continue
            
            last_block = merged[-1]
            last_end = datetime.fromisoformat(last_block.end_iso)
            current_start = datetime.fromisoformat(block.start_iso)
            
            # Check for overlap
            if current_start < last_end:
                # Shift block to end of last block
                duration = datetime.fromisoformat(block.end_iso) - current_start
                new_start = last_end
                new_end = new_start + duration
                
                # Update block times
                block.start_iso = new_start.isoformat()
                block.end_iso = new_end.isoformat()
                
                log_info(f"Shifted overlapping block: {block.title}")
            
            merged.append(block)
        
        log_info(f"Merged timeline has {len(merged)} blocks")
        return merged
    
    def _parse_time(self, time_str: str) -> time:
        """Parse HH:MM time string."""
        try:
            hour, minute = map(int, time_str.split(":"))
            return time(hour, minute)
        except Exception:
            return time(0, 0)
    
    def _is_in_sleep_window(
        self,
        check_time: time,
        sleep_start: time,
        sleep_end: time
    ) -> bool:
        """Check if a time falls in the sleep window.
        
        Handles overnight sleep (e.g., 23:00 - 07:00).
        """
        if sleep_start < sleep_end:
            # Same day (e.g., 01:00 - 05:00)
            return sleep_start <= check_time < sleep_end
        else:
            # Overnight (e.g., 23:00 - 07:00)
            return check_time >= sleep_start or check_time < sleep_end


# Global timeline service instance
timeline_service = TimelineService()

