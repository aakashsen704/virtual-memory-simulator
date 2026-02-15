"""
Demo Script - Virtual Memory Simulator
Demonstrates different page replacement algorithms and generates performance comparison
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from virtual_memory import VirtualMemorySimulator


def generate_reference_string(length, num_pages, pattern='random'):
    """
    Generate page reference string with different access patterns
    
    Patterns:
    - random: Completely random access
    - sequential: Sequential page access
    - locality: Temporal and spatial locality
    - loop: Repeated loop pattern
    """
    if pattern == 'random':
        return [random.randint(0, num_pages - 1) for _ in range(length)]
    
    elif pattern == 'sequential':
        refs = []
        for _ in range(length // num_pages + 1):
            refs.extend(range(num_pages))
        return refs[:length]
    
    elif pattern == 'locality':
        # 80% accesses to 20% of pages (locality of reference)
        refs = []
        hot_pages = random.sample(range(num_pages), num_pages // 5)
        
        for _ in range(length):
            if random.random() < 0.8:
                refs.append(random.choice(hot_pages))
            else:
                refs.append(random.randint(0, num_pages - 1))
        return refs
    
    elif pattern == 'loop':
        # Simulate loop accessing small working set
        working_set = random.sample(range(num_pages), min(10, num_pages))
        refs = []
        for _ in range(length // len(working_set) + 1):
            refs.extend(working_set)
        return refs[:length]
    
    else:
        raise ValueError(f"Unknown pattern: {pattern}")


def compare_algorithms(reference_string, num_frames_list, num_pages, page_size=4096, tlb_size=16):
    """Compare all algorithms across different frame counts"""
    
    algorithms = ['FIFO', 'LRU', 'LFU', 'Optimal', 'Clock']
    results = {alg: [] for alg in algorithms}
    
    for num_frames in num_frames_list:
        print(f"\nTesting with {num_frames} frames...")
        
        for alg in algorithms:
            try:
                sim = VirtualMemorySimulator(
                    num_pages=num_pages,
                    num_frames=num_frames,
                    page_size=page_size,
                    tlb_size=tlb_size,
                    algorithm_name=alg,
                    reference_string=reference_string if alg == 'Optimal' else None
                )
                
                sim.run_trace(reference_string)
                stats = sim.get_statistics()
                results[alg].append(stats['page_fault_rate'])
                
                print(f"  {alg:8s}: {stats['page_faults']} page faults ({stats['page_fault_rate']:.2f}%)")
                
            except Exception as e:
                print(f"  {alg:8s}: Error - {e}")
                results[alg].append(None)
    
    return results


def plot_comparison(results, num_frames_list, pattern_name):
    """Create visualization of algorithm comparison"""
    
    plt.figure(figsize=(12, 6))
    
    for alg, fault_rates in results.items():
        # Filter out None values
        valid_points = [(frames, rate) for frames, rate in zip(num_frames_list, fault_rates) if rate is not None]
        if valid_points:
            frames, rates = zip(*valid_points)
            plt.plot(frames, rates, marker='o', linewidth=2, label=alg, markersize=8)
    
    plt.xlabel('Number of Physical Frames', fontsize=12, fontweight='bold')
    plt.ylabel('Page Fault Rate (%)', fontsize=12, fontweight='bold')
    plt.title(f'Page Replacement Algorithm Comparison\nAccess Pattern: {pattern_name}', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = f'comparison_{pattern_name}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {filename}")
    
    return filename


def demo_single_algorithm(algorithm_name='LRU'):
    """Detailed demonstration of a single algorithm"""
    
    print(f"\n{'='*70}")
    print(f"DETAILED DEMONSTRATION: {algorithm_name} Algorithm")
    print(f"{'='*70}")
    
    # Configuration
    num_pages = 50
    num_frames = 5
    page_size = 4096
    tlb_size = 8
    reference_length = 100
    
    # Generate reference string with locality
    reference_string = generate_reference_string(reference_length, num_pages, 'locality')
    
    print(f"\nConfiguration:")
    print(f"  Virtual Pages: {num_pages}")
    print(f"  Physical Frames: {num_frames}")
    print(f"  Page Size: {page_size} bytes")
    print(f"  TLB Size: {tlb_size} entries")
    print(f"  Reference String Length: {reference_length}")
    print(f"\nFirst 20 page accesses: {reference_string[:20]}")
    
    # Run simulation
    sim = VirtualMemorySimulator(
        num_pages=num_pages,
        num_frames=num_frames,
        page_size=page_size,
        tlb_size=tlb_size,
        algorithm_name=algorithm_name,
        reference_string=reference_string if algorithm_name == 'Optimal' else None
    )
    
    sim.run_trace(reference_string)
    sim.print_statistics()
    
    return sim


def comprehensive_analysis():
    """Run comprehensive performance analysis"""
    
    print("\n" + "="*70)
    print("COMPREHENSIVE VIRTUAL MEMORY PERFORMANCE ANALYSIS")
    print("="*70)
    
    # Configuration
    num_pages = 100
    reference_length = 500
    page_size = 4096
    tlb_size = 16
    
    # Test different frame counts
    num_frames_list = [5, 10, 15, 20, 25, 30]
    
    # Test different access patterns
    patterns = {
        'Random Access': 'random',
        'Sequential Access': 'sequential',
        'Locality of Reference': 'locality',
        'Loop Pattern': 'loop'
    }
    
    plot_files = []
    
    for pattern_name, pattern_type in patterns.items():
        print(f"\n{'='*70}")
        print(f"Testing Pattern: {pattern_name}")
        print(f"{'='*70}")
        
        # Generate reference string
        reference_string = generate_reference_string(reference_length, num_pages, pattern_type)
        
        # Compare algorithms
        results = compare_algorithms(reference_string, num_frames_list, num_pages, page_size, tlb_size)
        
        # Plot results
        plot_file = plot_comparison(results, num_frames_list, pattern_name.replace(' ', '_'))
        plot_files.append(plot_file)
    
    return plot_files


if __name__ == "__main__":
    # Demo 1: Single algorithm detailed view
    print("\n" + "🔍 " * 35)
    print("DEMO 1: Detailed Algorithm Analysis")
    demo_single_algorithm('LRU')
    
    # Demo 2: Compare algorithms
    print("\n" + "📊 " * 35)
    print("DEMO 2: Algorithm Comparison (Locality Pattern)")
    reference_string = generate_reference_string(300, 50, 'locality')
    results = compare_algorithms(reference_string, [5, 10, 15, 20], 50)
    plot_comparison(results, [5, 10, 15, 20], 'Demo_Locality')
    
    # Demo 3: Comprehensive analysis
    print("\n" + "🎯 " * 35)
    print("DEMO 3: Comprehensive Performance Analysis")
    plot_files = comprehensive_analysis()
    
    print("\n" + "✅ " * 35)
    print("\nSimulation Complete!")
    print(f"Generated {len(plot_files)} performance comparison plots")
    print("\nFiles created in: /home/claude/virtual-memory-simulator/")