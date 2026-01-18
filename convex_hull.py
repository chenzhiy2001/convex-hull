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
    def merge_hulls(left, right):
        # Find rightmost of left and leftmost of right
        def upper_tangent(lh, rh):
            i, j = max(range(len(lh)), key=lambda k: lh[k][0]), min(range(len(rh)), key=lambda k: rh[k][0])
            n1, n2 = len(lh), len(rh)
            done = False
            while not done:
                done = True
                while cross(rh[j], lh[i], lh[(i-1)%n1]) >= 0:
                    i = (i - 1) % n1; done = False
                while cross(lh[i], rh[j], rh[(j+1)%n2]) <= 0:
                    j = (j + 1) % n2; done = False
            return i, j
        
        def lower_tangent(lh, rh):
            i, j = max(range(len(lh)), key=lambda k: lh[k][0]), min(range(len(rh)), key=lambda k: rh[k][0])
            n1, n2 = len(lh), len(rh)
            done = False
            while not done:
                done = True
                while cross(rh[j], lh[i], lh[(i+1)%n1]) <= 0:
                    i = (i + 1) % n1; done = False
                while cross(lh[i], rh[j], rh[(j-1)%n2]) >= 0:
                    j = (j - 1) % n2; done = False
            return i, j
        
        ui, uj = upper_tangent(left, right)
        li, lj = lower_tangent(left, right)
        
        # Build merged hull: upper tangent -> right hull -> lower tangent -> left hull
        result = []
        i = ui
        while True:
            result.append(left[i])
            if i == li: break
            i = (i + 1) % len(left)
        j = lj
        while True:
            result.append(right[j])
            if j == uj: break
            j = (j + 1) % len(right)
        return result
    
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 5: return graham_scan(pts)
    mid = len(pts) // 2
    left = divide_conquer(pts[:mid])
    right = divide_conquer(pts[mid:])
    if not left: return right
    if not right: return left
    return merge_hulls(left, right)

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
