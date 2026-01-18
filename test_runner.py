#!/usr/bin/env python3
"""Batch test runner for convex hull algorithms"""
import sys
import json
from convex_hull import graham_scan, divide_conquer, generate_random, benchmark

def run_batch(test_sizes=[100, 500, 1000, 5000, 10000, 50000]):
    print("=" * 60)
    print(f"{'n':>8} | {'Graham (ms)':>12} | {'D&C (ms)':>12} | Hull Size")
    print("=" * 60)
    for n in test_sizes:
        pts = generate_random(n)
        res = benchmark(pts)
        print(f"{n:>8} | {res['graham']['avg_ms']:>12.3f} | {res['divide_conquer']['avg_ms']:>12.3f} | {res['graham']['hull_size']}")
    print("=" * 60)

def test_from_file(filename):
    with open(filename) as f:
        pts = json.load(f)
    print(f"Testing {len(pts)} points from {filename}")
    res = benchmark(pts)
    for algo, data in res.items():
        print(f"  {algo}: {data['avg_ms']:.3f}ms, hull={data['hull_size']}")

def verify_correctness():
    """Verify both algorithms produce same results"""
    print("Verifying correctness...")
    for n in [10, 50, 100, 500]:
        pts = generate_random(n, 100)
        h1 = set(graham_scan(pts))
        h2 = set(divide_conquer(pts))
        status = "✓" if h1 == h2 else "✗"
        print(f"  n={n}: {status}")
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--verify":
            verify_correctness()
        else:
            test_from_file(sys.argv[1])
    else:
        run_batch()
