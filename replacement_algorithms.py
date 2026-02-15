"""
Page Replacement Algorithms
Implements FIFO, LRU, LFU, and Optimal page replacement
"""

from collections import deque
from abc import ABC, abstractmethod


class PageReplacementAlgorithm(ABC):
    """Base class for page replacement algorithms"""
    
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = []  # List of page numbers currently in frames
        
    @abstractmethod
    def access_page(self, page_number, time, is_write=False):
        """
        Access a page and return whether a page fault occurred
        Returns: (page_fault, victim_page)
        """
        pass
    
    @abstractmethod
    def get_victim(self):
        """Select a page to evict"""
        pass
    
    def is_page_in_memory(self, page_number):
        """Check if page is already in physical memory"""
        return page_number in self.frames


class FIFO(PageReplacementAlgorithm):
    """First-In-First-Out page replacement"""
    
    def __init__(self, num_frames):
        super().__init__(num_frames)
        self.queue = deque()
        
    def access_page(self, page_number, time, is_write=False):
        if self.is_page_in_memory(page_number):
            return False, None  # No page fault
        
        # Page fault occurred
        victim = None
        if len(self.frames) >= self.num_frames:
            victim = self.get_victim()
            self.frames.remove(victim)
            self.queue.remove(victim)
        
        self.frames.append(page_number)
        self.queue.append(page_number)
        return True, victim
    
    def get_victim(self):
        """Remove oldest page (first in queue)"""
        return self.queue[0]


class LRU(PageReplacementAlgorithm):
    """Least Recently Used page replacement"""
    
    def __init__(self, num_frames):
        super().__init__(num_frames)
        self.access_times = {}  # page_number -> last_access_time
        
    def access_page(self, page_number, time, is_write=False):
        page_fault = not self.is_page_in_memory(page_number)
        victim = None
        
        if page_fault:
            if len(self.frames) >= self.num_frames:
                victim = self.get_victim()
                self.frames.remove(victim)
                del self.access_times[victim]
            
            self.frames.append(page_number)
        
        # Update access time
        self.access_times[page_number] = time
        return page_fault, victim
    
    def get_victim(self):
        """Remove least recently used page"""
        return min(self.access_times, key=self.access_times.get)


class LFU(PageReplacementAlgorithm):
    """Least Frequently Used page replacement"""
    
    def __init__(self, num_frames):
        super().__init__(num_frames)
        self.access_counts = {}  # page_number -> access_count
        self.access_times = {}   # For tie-breaking (use LRU)
        
    def access_page(self, page_number, time, is_write=False):
        page_fault = not self.is_page_in_memory(page_number)
        victim = None
        
        if page_fault:
            if len(self.frames) >= self.num_frames:
                victim = self.get_victim()
                self.frames.remove(victim)
                del self.access_counts[victim]
                del self.access_times[victim]
            
            self.frames.append(page_number)
            self.access_counts[page_number] = 0
        
        # Update access count and time
        self.access_counts[page_number] += 1
        self.access_times[page_number] = time
        return page_fault, victim
    
    def get_victim(self):
        """Remove least frequently used page (LRU for ties)"""
        min_count = min(self.access_counts.values())
        candidates = [p for p, count in self.access_counts.items() if count == min_count]
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Tie-break using LRU
        return min(candidates, key=lambda p: self.access_times[p])


class Optimal(PageReplacementAlgorithm):
    """Optimal page replacement (requires future knowledge)"""
    
    def __init__(self, num_frames, reference_string):
        super().__init__(num_frames)
        self.reference_string = reference_string
        self.current_index = 0
        
    def access_page(self, page_number, time, is_write=False):
        page_fault = not self.is_page_in_memory(page_number)
        victim = None
        
        if page_fault:
            if len(self.frames) >= self.num_frames:
                victim = self.get_victim()
                self.frames.remove(victim)
            
            self.frames.append(page_number)
        
        self.current_index += 1
        return page_fault, victim
    
    def get_victim(self):
        """Remove page that won't be used for longest time"""
        farthest_use = -1
        victim = None
        
        for page in self.frames:
            # Find next use of this page
            next_use = float('inf')
            for i in range(self.current_index, len(self.reference_string)):
                if self.reference_string[i] == page:
                    next_use = i
                    break
            
            if next_use > farthest_use:
                farthest_use = next_use
                victim = page
        
        return victim


class Clock(PageReplacementAlgorithm):
    """Clock (Second Chance) page replacement"""
    
    def __init__(self, num_frames):
        super().__init__(num_frames)
        self.reference_bits = {}  # page_number -> reference_bit
        self.clock_hand = 0
        
    def access_page(self, page_number, time, is_write=False):
        page_fault = not self.is_page_in_memory(page_number)
        victim = None
        
        if page_fault:
            if len(self.frames) >= self.num_frames:
                victim = self.get_victim()
                victim_index = self.frames.index(victim)
                self.frames[victim_index] = page_number
                del self.reference_bits[victim]
            else:
                self.frames.append(page_number)
        
        # Set reference bit
        self.reference_bits[page_number] = 1
        return page_fault, victim
    
    def get_victim(self):
        """Use clock algorithm to find victim"""
        while True:
            page = self.frames[self.clock_hand]
            
            if self.reference_bits[page] == 0:
                # Found victim
                victim = page
                self.clock_hand = (self.clock_hand + 1) % len(self.frames)
                return victim
            else:
                # Give second chance
                self.reference_bits[page] = 0
                self.clock_hand = (self.clock_hand + 1) % len(self.frames)
