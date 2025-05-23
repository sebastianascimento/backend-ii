import multiprocessing as mp
import time
import math
from datetime import datetime
import os

def is_prime(num):
    """Check if a number is prime (CPU-intensive function)."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    
    # Check divisibility up to the square root
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def find_primes_in_range(start, end):
    """Find all prime numbers in the specified range."""
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def process_chunk(chunk_range):
    """Process a chunk of numbers to find primes (used by multiprocessing)."""
    start, end = chunk_range
    return find_primes_in_range(start, end)

def sequential_prime_finder(max_num, num_chunks=1):
    """Find primes sequentially."""
    start_time = time.time()
    
    primes = find_primes_in_range(2, max_num)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return primes, execution_time

def process_based_prime_finder(max_num, num_chunks):
    """Find primes using multiple processes with Process class."""
    start_time = time.time()
    
    # Split the range into chunks
    chunk_size = math.ceil(max_num / num_chunks)
    chunks = [(i, min(i + chunk_size - 1, max_num)) 
              for i in range(2, max_num + 1, chunk_size)]
    
    # Create and start processes
    processes = []
    manager = mp.Manager()
    result_list = manager.list()
    
    # Define a worker function that adds results to the shared list
    def worker(chunk_range, result_list):
        primes = process_chunk(chunk_range)
        result_list.extend(primes)
    
    for chunk_range in chunks:
        p = mp.Process(target=worker, args=(chunk_range, result_list))
        processes.append(p)
        p.start()
        
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    # Combine and sort results
    all_primes = sorted(list(result_list))
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return all_primes, execution_time

def pool_based_prime_finder(max_num, num_chunks):
    """Find primes using a process pool."""
    start_time = time.time()
    
    # Split the range into chunks
    chunk_size = math.ceil(max_num / num_chunks)
    chunks = [(i, min(i + chunk_size - 1, max_num)) 
              for i in range(2, max_num + 1, chunk_size)]
    
    # Use Pool to parallelize the work
    with mp.Pool(processes=num_chunks) as pool:
        chunk_results = pool.map(process_chunk, chunks)
    
    # Combine and sort all primes
    all_primes = []
    for result in chunk_results:
        all_primes.extend(result)
    all_primes.sort()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return all_primes, execution_time

def print_results(method_name, primes, execution_time):
    """Print the results and performance metrics."""
    print(f"\n{method_name} Results:")
    print(f"- Found {len(primes)} prime numbers")
    print(f"- First few primes: {primes[:5]}...")
    print(f"- Last few primes: ...{primes[-5:]}")
    print(f"- Execution time: {execution_time:.4f} seconds")

def run_experiment(max_num=50000):
    """Run a comparative experiment between sequential and parallel approaches."""
    print(f"{'='*60}")
    print(f"Finding prime numbers up to {max_num}")
    print(f"{'='*60}")
    
    # Get the number of available CPU cores
    cpu_count = mp.cpu_count()
    print(f"Number of CPU cores available: {cpu_count}")
    
    # Run sequential version
    seq_primes, seq_time = sequential_prime_finder(max_num)
    print_results("Sequential", seq_primes, seq_time)
    
    # Run Process-based version
    proc_primes, proc_time = process_based_prime_finder(max_num, cpu_count)
    print_results("Process-based Multiprocessing", proc_primes, proc_time)
    
    # Run Pool-based version
    pool_primes, pool_time = pool_based_prime_finder(max_num, cpu_count)
    print_results("Pool-based Multiprocessing", pool_primes, pool_time)
    
    # Verify results are the same
    assert seq_primes == proc_primes == pool_primes, "Results don't match!"
    
    # Calculate and print speedup
    proc_speedup = seq_time / proc_time
    pool_speedup = seq_time / pool_time
    
    print("\nPerformance Comparison:")
    print(f"- Process-based speedup: {proc_speedup:.2f}x faster than sequential")
    print(f"- Pool-based speedup: {pool_speedup:.2f}x faster than sequential")
    
    # Show example of current process information
    print(f"\nCurrent process ID: {os.getpid()}")
    print(f"Current process name: {mp.current_process().name}")

if __name__ == "__main__":
    # Important: multiprocessing code must be under this guard
    # to avoid infinite recursion on Windows
    print(f"Starting multiprocessing demonstration at {datetime.now()}")
    
    # Adjust this number based on your computer's capability
    # Lower for faster results, higher for more pronounced differences
    MAX_NUMBER = 100000
    
    run_experiment(MAX_NUMBER)