"""Convex Hull: Graham Scan & Divide-and-Conquer"""
import time
import random

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def graham_scan(points):
    """Graham Scan O(n log n)"""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 1: return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def divide_conquer(points):
    """Divide and Conquer O(n log n)"""
    pts = sorted(set(map(tuple, points)))
    n = len(pts)
    if n <= 3: return graham_scan(pts)
    
    mid = n // 2
    left = divide_conquer(pts[:mid])
    right = divide_conquer(pts[mid:])
    
    # Merge two convex hulls - O(n) using linear merge on sorted points
    # Since hulls are convex and non-overlapping in x, we merge upper/lower chains
    all_pts = sorted(set(left + right))
    lower, upper = [], []
    for p in all_pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(all_pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def generate_random(n, max_coord=1000):
    return [(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]

def benchmark(points, runs=3):
    results = {}
    for name, algo in [("graham", graham_scan), ("divide_conquer", divide_conquer)]:
        times = []
        for _ in range(runs):
            start = time.perf_counter()
            hull = algo(points)
            times.append(time.perf_counter() - start)
        results[name] = {"avg_ms": sum(times)/len(times)*1000, "hull_size": len(hull)}
    return results

if __name__ == "__main__":
    for n in [100, 1000, 10000]:
        pts = generate_random(n)
        print(f"\nn={n}:")
        res = benchmark(pts)
        for algo, data in res.items():
            print(f"  {algo}: {data['avg_ms']:.3f}ms, hull={data['hull_size']}")
