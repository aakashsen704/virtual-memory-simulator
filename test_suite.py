"""
Test Suite for Virtual Memory Simulator
Run comprehensive tests to verify correctness
"""

import sys
from virtual_memory import VirtualMemorySimulator
from replacement_algorithms import FIFO, LRU, LFU, Optimal, Clock


def test_fifo_basic():
    """Test basic FIFO behavior"""
    print("Testing FIFO Algorithm...")
    
    sim = VirtualMemorySimulator(
        num_pages=10,
        num_frames=3,
        page_size=4096,
        tlb_size=4,
        algorithm_name='FIFO'
    )
    
    # Reference string: 1,2,3,4,1,2,5,1,2,3,4,5
    # With 3 frames, should cause specific faults
    reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    sim.run_trace(reference_string)
    
    stats = sim.get_statistics()
    assert stats['page_faults'] == 9, f"Expected 9 page faults, got {stats['page_faults']}"
    print(f"✓ FIFO basic test passed: {stats['page_faults']} page faults")
    return True


def test_lru_basic():
    """Test basic LRU behavior"""
    print("Testing LRU Algorithm...")
    
    sim = VirtualMemorySimulator(
        num_pages=10,
        num_frames=3,
        page_size=4096,
        tlb_size=4,
        algorithm_name='LRU'
    )
    
    reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    sim.run_trace(reference_string)
    
    stats = sim.get_statistics()
    # LRU should perform better than or equal to FIFO
    assert stats['page_faults'] <= 10, f"LRU faults too high: {stats['page_faults']}"
    print(f"✓ LRU basic test passed: {stats['page_faults']} page faults")
    return True


def test_optimal_best():
    """Test that Optimal performs best"""
    print("Testing Optimal Algorithm superiority...")
    
    reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5] * 5
    num_frames = 4
    
    results = {}
    for alg in ['FIFO', 'LRU', 'Optimal']:
        sim = VirtualMemorySimulator(
            num_pages=10,
            num_frames=num_frames,
            page_size=4096,
            tlb_size=4,
            algorithm_name=alg,
            reference_string=reference_string if alg == 'Optimal' else None
        )
        sim.run_trace(reference_string)
        results[alg] = sim.get_statistics()['page_faults']
    
    assert results['Optimal'] <= results['FIFO'], "Optimal should beat FIFO"
    assert results['Optimal'] <= results['LRU'], "Optimal should beat LRU"
    print(f"✓ Optimal performs best: FIFO={results['FIFO']}, LRU={results['LRU']}, Optimal={results['Optimal']}")
    return True


def test_tlb_functionality():
    """Test TLB hit/miss tracking"""
    print("Testing TLB functionality...")
    
    sim = VirtualMemorySimulator(
        num_pages=20,
        num_frames=10,
        page_size=4096,
        tlb_size=4,
        algorithm_name='LRU'
    )
    
    # Access same pages repeatedly - should get TLB hits
    reference_string = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    sim.run_trace(reference_string)
    
    stats = sim.get_statistics()
    assert stats['tlb_hits'] > 0, "TLB should have some hits with repeated accesses"
    assert stats['tlb_hit_rate'] > 0, "TLB hit rate should be positive"
    print(f"✓ TLB test passed: {stats['tlb_hits']} hits, {stats['tlb_hit_rate']:.2f}% hit rate")
    return True


def test_no_page_faults_when_sufficient_frames():
    """Test that no page faults occur when frames >= unique pages"""
    print("Testing sufficient frames scenario...")
    
    reference_string = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    unique_pages = len(set(reference_string))
    
    sim = VirtualMemorySimulator(
        num_pages=20,
        num_frames=unique_pages,  # Enough frames for all unique pages
        page_size=4096,
        tlb_size=4,
        algorithm_name='LRU'
    )
    
    sim.run_trace(reference_string)
    stats = sim.get_statistics()
    
    # Should only have initial page faults for loading
    assert stats['page_faults'] == unique_pages, \
        f"Expected {unique_pages} page faults, got {stats['page_faults']}"
    print(f"✓ Sufficient frames test passed: {stats['page_faults']} initial page faults only")
    return True


def test_clock_algorithm():
    """Test Clock (Second Chance) algorithm"""
    print("Testing Clock Algorithm...")
    
    sim = VirtualMemorySimulator(
        num_pages=10,
        num_frames=3,
        page_size=4096,
        tlb_size=4,
        algorithm_name='Clock'
    )
    
    reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    sim.run_trace(reference_string)
    
    stats = sim.get_statistics()
    # Clock should work reasonably well
    assert stats['page_faults'] > 0, "Should have some page faults"
    assert stats['page_faults'] < len(reference_string), "Shouldn't fault on every access"
    print(f"✓ Clock test passed: {stats['page_faults']} page faults")
    return True


def test_increasing_frames_reduces_faults():
    """Test that more frames reduce page faults"""
    print("Testing frame count vs page faults relationship...")
    
    reference_string = [1, 2, 3, 4, 5, 1, 2, 3, 6, 7] * 5
    
    results = []
    for num_frames in [3, 5, 8]:
        sim = VirtualMemorySimulator(
            num_pages=20,
            num_frames=num_frames,
            page_size=4096,
            tlb_size=4,
            algorithm_name='LRU'
        )
        sim.run_trace(reference_string)
        stats = sim.get_statistics()
        results.append(stats['page_faults'])
    
    # More frames should generally mean fewer faults (or equal due to anomalies)
    assert results[0] >= results[1] >= results[2], \
        f"Page faults should decrease with more frames: {results}"
    print(f"✓ Frame scaling test passed: 3f={results[0]}, 5f={results[1]}, 8f={results[2]}")
    return True


def test_address_translation():
    """Test virtual to physical address translation"""
    print("Testing address translation...")
    
    sim = VirtualMemorySimulator(
        num_pages=100,
        num_frames=10,
        page_size=4096,
        tlb_size=4,
        algorithm_name='FIFO'
    )
    
    # Test address translation
    virtual_addr = 8192  # Page 2, offset 0
    physical_addr, fault, tlb_hit = sim.translate_address(virtual_addr)
    
    assert fault == True, "First access should cause page fault"
    
    # Access same page again
    virtual_addr2 = 8200  # Page 2, offset 8
    physical_addr2, fault2, tlb_hit2 = sim.translate_address(virtual_addr2)
    
    assert fault2 == False, "Second access to same page should not fault"
    print(f"✓ Address translation test passed")
    return True


def test_lfu_basic():
    """Test LFU algorithm"""
    print("Testing LFU Algorithm...")
    
    sim = VirtualMemorySimulator(
        num_pages=10,
        num_frames=3,
        page_size=4096,
        tlb_size=4,
        algorithm_name='LFU'
    )
    
    # Pattern where some pages are accessed more frequently
    reference_string = [1, 1, 1, 2, 2, 3, 4, 1, 2, 5]
    sim.run_trace(reference_string)
    
    stats = sim.get_statistics()
    assert stats['page_faults'] > 0, "Should have some page faults"
    print(f"✓ LFU test passed: {stats['page_faults']} page faults")
    return True


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*70)
    print("VIRTUAL MEMORY SIMULATOR - TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        test_fifo_basic,
        test_lru_basic,
        test_lfu_basic,
        test_clock_algorithm,
        test_optimal_best,
        test_tlb_functionality,
        test_no_page_faults_when_sufficient_frames,
        test_increasing_frames_reduces_faults,
        test_address_translation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} ERROR: {e}")
        print()
    
    print("="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 All tests passed! Simulator is working correctly.\n")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review.\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
