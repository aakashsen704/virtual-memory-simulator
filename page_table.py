"""
Page Table Implementation for Virtual Memory Simulator
Handles virtual-to-physical address translation
"""

class PageTableEntry:
    """Represents a single page table entry"""
    def __init__(self, frame_number=None):
        self.valid = False  # Is page in physical memory?
        self.frame_number = frame_number  # Physical frame number
        self.referenced = False  # For LRU algorithm
        self.modified = False  # Dirty bit
        self.last_access_time = 0  # For LRU tracking
        self.access_count = 0  # For LFU algorithm
        
    def __repr__(self):
        return f"PTE(valid={self.valid}, frame={self.frame_number}, ref={self.referenced})"


class PageTable:
    """Main page table structure"""
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.entries = [PageTableEntry() for _ in range(num_pages)]
        
    def get_entry(self, page_number):
        """Get page table entry for a virtual page"""
        if page_number >= self.num_pages:
            raise ValueError(f"Invalid page number: {page_number}")
        return self.entries[page_number]
    
    def is_valid(self, page_number):
        """Check if page is in physical memory"""
        return self.entries[page_number].valid
    
    def get_frame_number(self, page_number):
        """Get physical frame number for a page"""
        if not self.is_valid(page_number):
            return None
        return self.entries[page_number].frame_number
    
    def set_frame(self, page_number, frame_number):
        """Map virtual page to physical frame"""
        entry = self.entries[page_number]
        entry.valid = True
        entry.frame_number = frame_number
        
    def invalidate(self, page_number):
        """Mark page as not in memory"""
        self.entries[page_number].valid = False
        self.entries[page_number].frame_number = None
        
    def update_access(self, page_number, time, is_write=False):
        """Update access information for replacement algorithms"""
        entry = self.entries[page_number]
        entry.referenced = True
        entry.last_access_time = time
        entry.access_count += 1
        if is_write:
            entry.modified = True
