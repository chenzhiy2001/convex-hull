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

def cc_triangle(pts):
    pts = list(set(pts))
    if len(pts) <= 1:
        return pts
    if len(pts) == 2:
        return sorted(pts)

    a, b, c = pts
    area = cross(a, b, c)

    if area > 0:      # CCW
        return [a, b, c]
    elif area < 0:    # CW → reverse
        return [a, c, b]
    else:             # Collinear → keep extremes
        return sorted(pts)

def divide_conquer(points):
    pts = sorted(set(points))        
    return dc_hull(pts)


def dc_hull(pts):
    n = len(pts)
    if n <= 3:
        return cc_triangle(pts)

    mid = n // 2
    left = dc_hull(pts[:mid])
    right = dc_hull(pts[mid:])

    return merge_hulls(left, right)


# ---------- Tangent Merge (O(h)) ----------

def merge_hulls(left, right):
    n1, n2 = len(left), len(right)

    # Rightmost point of left hull
    i = max(range(n1), key=lambda k: left[k][0])
    # Leftmost point of right hull
    j = min(range(n2), key=lambda k: right[k][0])

    # ---- Upper tangent ----
    i_u, j_u = i, j
    while True:
        moved = False
        while cross(right[j_u], left[i_u], left[(i_u + 1) % n1]) > 0:
            i_u = (i_u + 1) % n1
            moved = True
        while cross(left[i_u], right[j_u], right[(j_u - 1) % n2]) < 0:
            j_u = (j_u - 1) % n2
            moved = True
        if not moved:
            break

    # ---- Lower tangent ----
    i_l, j_l = i, j
    while True:
        moved = False
        while cross(right[j_l], left[i_l], left[(i_l - 1) % n1]) < 0:
            i_l = (i_l - 1) % n1
            moved = True
        while cross(left[i_l], right[j_l], right[(j_l + 1) % n2]) > 0:
            j_l = (j_l + 1) % n2
            moved = True
        if not moved:
            break

    # ---- Build merged hull (CCW) ----
    hull = []

    k = i_u
    hull.append(left[k])
    while k != i_l:
        k = (k + 1) % n1
        hull.append(left[k])

    k = j_l
    hull.append(right[k])
    while k != j_u:
        k = (k + 1) % n2
        hull.append(right[k])

    return hull

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
