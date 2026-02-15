"""
Virtual Memory Simulator
Main simulator that combines page table, TLB, and replacement algorithms
"""

from collections import OrderedDict
from page_table import PageTable
from replacement_algorithms import *


class TLB:
    """Translation Lookaside Buffer - Cache for page table entries"""
    
    def __init__(self, size):
        self.size = size
        self.cache = OrderedDict()  # LRU cache
        self.hits = 0
        self.misses = 0
        
    def lookup(self, page_number):
        """Look up page in TLB"""
        if page_number in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(page_number)
            return self.cache[page_number]
        else:
            self.misses += 1
            return None
    
    def insert(self, page_number, frame_number):
        """Insert page-to-frame mapping in TLB"""
        if page_number in self.cache:
            self.cache.move_to_end(page_number)
        else:
            if len(self.cache) >= self.size:
                # Remove oldest entry
                self.cache.popitem(last=False)
            self.cache[page_number] = frame_number
    
    def invalidate(self, page_number):
        """Remove entry from TLB"""
        if page_number in self.cache:
            del self.cache[page_number]
    
    def get_hit_rate(self):
        """Calculate TLB hit rate"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0


class VirtualMemorySimulator:
    """Main Virtual Memory Simulator"""
    
    def __init__(self, num_pages, num_frames, page_size, tlb_size, algorithm_name, reference_string=None):
        """
        Initialize the simulator
        
        Args:
            num_pages: Number of virtual pages
            num_frames: Number of physical frames
            page_size: Size of each page in bytes
            tlb_size: Size of TLB
            algorithm_name: 'FIFO', 'LRU', 'LFU', 'Optimal', 'Clock'
            reference_string: Page reference sequence (required for Optimal)
        """
        self.num_pages = num_pages
        self.num_frames = num_frames
        self.page_size = page_size
        self.page_table = PageTable(num_pages)
        self.tlb = TLB(tlb_size)
        
        # Initialize replacement algorithm
        if algorithm_name == 'FIFO':
            self.algorithm = FIFO(num_frames)
        elif algorithm_name == 'LRU':
            self.algorithm = LRU(num_frames)
        elif algorithm_name == 'LFU':
            self.algorithm = LFU(num_frames)
        elif algorithm_name == 'Optimal':
            if reference_string is None:
                raise ValueError("Optimal algorithm requires reference_string")
            self.algorithm = Optimal(num_frames, reference_string)
        elif algorithm_name == 'Clock':
            self.algorithm = Clock(num_frames)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        
        self.algorithm_name = algorithm_name
        
        # Statistics
        self.page_faults = 0
        self.memory_accesses = 0
        self.tlb_hits = 0
        self.tlb_misses = 0
        self.current_time = 0
        
        # Track free frames
        self.free_frames = list(range(num_frames))
        self.page_to_frame = {}  # Current mapping
        
    def translate_address(self, virtual_address, is_write=False):
        """
        Translate virtual address to physical address
        
        Returns: (physical_address, page_fault_occurred, tlb_hit)
        """
        self.memory_accesses += 1
        self.current_time += 1
        
        # Extract page number and offset
        page_number = virtual_address // self.page_size
        offset = virtual_address % self.page_size
        
        # Check TLB first
        frame_number = self.tlb.lookup(page_number)
        tlb_hit = (frame_number is not None)
        
        page_fault = False
        
        if not tlb_hit:
            # TLB miss - check page table
            if not self.page_table.is_valid(page_number):
                # Page fault!
                page_fault = True
                self.page_faults += 1
                frame_number = self._handle_page_fault(page_number, is_write)
            else:
                # Page in memory, get from page table
                frame_number = self.page_table.get_frame_number(page_number)
            
            # Update TLB
            self.tlb.insert(page_number, frame_number)
        
        # Update page table access info
        self.page_table.update_access(page_number, self.current_time, is_write)
        
        # Calculate physical address
        physical_address = frame_number * self.page_size + offset
        
        return physical_address, page_fault, tlb_hit
    
    def _handle_page_fault(self, page_number, is_write):
        """Handle a page fault"""
        # Use replacement algorithm to access page
        fault_occurred, victim_page = self.algorithm.access_page(
            page_number, self.current_time, is_write
        )
        
        # Get a free frame or use victim's frame
        if victim_page is not None:
            # Evict victim page
            frame_number = self.page_to_frame[victim_page]
            self.page_table.invalidate(victim_page)
            self.tlb.invalidate(victim_page)
            del self.page_to_frame[victim_page]
        else:
            # Use a free frame
            frame_number = self.free_frames.pop(0)
        
        # Load page into frame
        self.page_table.set_frame(page_number, frame_number)
        self.page_to_frame[page_number] = frame_number
        
        return frame_number
    
    def run_trace(self, reference_string, write_operations=None):
        """
        Run simulation on a reference string
        
        Args:
            reference_string: List of page numbers to access
            write_operations: Set of indices in reference_string that are writes
        """
        write_operations = write_operations or set()
        
        for i, page_number in enumerate(reference_string):
            is_write = i in write_operations
            self.translate_address(page_number * self.page_size, is_write)
    
    def get_statistics(self):
        """Return simulation statistics"""
        page_fault_rate = (self.page_faults / self.memory_accesses * 100) if self.memory_accesses > 0 else 0
        
        return {
            'algorithm': self.algorithm_name,
            'total_accesses': self.memory_accesses,
            'page_faults': self.page_faults,
            'page_fault_rate': page_fault_rate,
            'tlb_hit_rate': self.tlb.get_hit_rate(),
            'tlb_hits': self.tlb.hits,
            'tlb_misses': self.tlb.misses
        }
    
    def print_statistics(self):
        """Print formatted statistics"""
        stats = self.get_statistics()
        print(f"\n{'='*60}")
        print(f"Virtual Memory Simulation Results - {stats['algorithm']}")
        print(f"{'='*60}")
        print(f"Total Memory Accesses:    {stats['total_accesses']}")
        print(f"Page Faults:              {stats['page_faults']}")
        print(f"Page Fault Rate:          {stats['page_fault_rate']:.2f}%")
        print(f"TLB Hits:                 {stats['tlb_hits']}")
        print(f"TLB Misses:               {stats['tlb_misses']}")
        print(f"TLB Hit Rate:             {stats['tlb_hit_rate']:.2f}%")
        print(f"{'='*60}\n")
