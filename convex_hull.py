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
    """Divide and Conquer O(n log n) with O(h) tangent merge"""
    pts = sorted(set(map(tuple, points)))
    n = len(pts)
    if n <= 3: return graham_scan(pts)
    
    mid = n // 2
    left = divide_conquer(pts[:mid])
    right = divide_conquer(pts[mid:])
    
    # Merge using tangent lines - O(h) where h is combined hull size
    n1, n2 = len(left), len(right)
    
    # Find starting points with proper tie-breaking for same x
    ri = max(range(n1), key=lambda i: (left[i][0], -left[i][1]))
    li = min(range(n2), key=lambda i: (right[i][0], right[i][1]))
    
    # Upper tangent: move CCW on left (i++), CW on right (j--)
    u1, u2 = ri, li
    while True:
        moved = False
        while cross(left[u1], right[u2], left[(u1 + 1) % n1]) >= 0:
            if cross(left[u1], right[u2], left[(u1 + 1) % n1]) == 0:
                # Collinear: only move if it gets us higher
                if left[(u1 + 1) % n1][1] <= left[u1][1]:
                    break
            u1 = (u1 + 1) % n1
            moved = True
        while cross(left[u1], right[u2], right[(u2 - 1) % n2]) >= 0:
            if cross(left[u1], right[u2], right[(u2 - 1) % n2]) == 0:
                if right[(u2 - 1) % n2][1] <= right[u2][1]:
                    break
            u2 = (u2 - 1) % n2
            moved = True
        if not moved:
            break
    
    # Lower tangent: move CW on left (i--), CCW on right (j++)
    l1, l2 = ri, li
    while True:
        moved = False
        while cross(left[l1], right[l2], left[(l1 - 1) % n1]) <= 0:
            if cross(left[l1], right[l2], left[(l1 - 1) % n1]) == 0:
                if left[(l1 - 1) % n1][1] >= left[l1][1]:
                    break
            l1 = (l1 - 1) % n1
            moved = True
        while cross(left[l1], right[l2], right[(l2 + 1) % n2]) <= 0:
            if cross(left[l1], right[l2], right[(l2 + 1) % n2]) == 0:
                if right[(l2 + 1) % n2][1] >= right[l2][1]:
                    break
            l2 = (l2 + 1) % n2
            moved = True
        if not moved:
            break
    
    # Build merged hull (CCW): upper_left -> ... -> lower_left -> lower_right -> ... -> upper_right
    result = []
    i = u1
    while True:
        result.append(left[i])
        if i == l1:
            break
        i = (i + 1) % n1
    j = l2
    while True:
        result.append(right[j])
        if j == u2:
            break
        j = (j + 1) % n2
    
    # Remove collinear points
    final = []
    for p in result:
        while len(final) >= 2 and cross(final[-2], final[-1], p) == 0:
            final.pop()
        final.append(p)
    while len(final) >= 3 and cross(final[-2], final[-1], final[0]) == 0:
        final.pop()
    while len(final) >= 3 and cross(final[-1], final[0], final[1]) == 0:
        final.pop(0)
    return final

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
