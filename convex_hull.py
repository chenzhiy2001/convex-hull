"""Convex Hull: Graham Scan & Divide-and-Conquer"""
import time
import random


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


# -------------------- Graham (correct, unchanged) --------------------

def graham_scan(points):
    """Graham Scan O(n log n)"""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 1:
        return pts

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


# -------------------- Divide & Conquer (fixed) --------------------

def cc_triangle(pts):
    """
    Base-case hull for <=3 points.
    Must return a CCW hull, and for collinear triples must return ONLY extremes.
    """
    pts = sorted(set(map(tuple, pts)))
    if len(pts) <= 1:
        return pts
    if len(pts) == 2:
        return pts

    a, b, c = pts
    area = cross(a, b, c)

    if area > 0:      # CCW
        return [a, b, c]
    elif area < 0:    # CW -> swap b,c
        return [a, c, b]
    else:             # Collinear -> keep extremes only
        return [pts[0], pts[-1]]


def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def remove_collinear_ccw(hull):
    """Remove consecutive collinear points from a cyclic CCW hull."""
    if len(hull) <= 2:
        out = []
        for p in hull:
            if not out or p != out[-1]:
                out.append(p)
        return out

    # remove consecutive duplicates
    clean = []
    for p in hull:
        if not clean or p != clean[-1]:
            clean.append(p)
    hull = clean

    # 1-2 passes are enough here (collinearity mainly appears at merge joints)
    for _ in range(2):
        n = len(hull)
        if n <= 2:
            break
        new = []
        for i in range(n):
            prev = hull[i - 1]
            cur = hull[i]
            nxt = hull[(i + 1) % n]
            if cross(prev, cur, nxt) != 0:
                new.append(cur)
        hull = new

    return hull


def divide_conquer(points):
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 1:
        return pts
    return dc_hull(pts)


def dc_hull(pts):
    n = len(pts)
    if n <= 3:
        return cc_triangle(pts)

    mid = n // 2
    left = dc_hull(pts[:mid])
    right = dc_hull(pts[mid:])

    return merge_hulls(left, right)


def merge_hulls(left, right):
    """
    Merge two convex hulls (each CCW) using correct upper/lower tangents.
    Handles collinear tangent cases by moving to the farther endpoint.
    """
    n1, n2 = len(left), len(right)
    if n1 == 0:
        return right
    if n2 == 0:
        return left
    if n1 == 1 and n2 == 1:
        return left if left[0] == right[0] else [left[0], right[0]]

    # rightmost point of left hull, leftmost point of right hull (tie-break by y)
    i = max(range(n1), key=lambda k: (left[k][0], left[k][1]))
    j = min(range(n2), key=lambda k: (right[k][0], right[k][1]))

    cap = (n1 + n2) * 20 + 20  # safety cap against degenerate cycles

    # ---------- Upper tangent ----------
    i_u, j_u = i, j
    steps = 0
    while True:
        moved = False

        # move i CCW while next is above OR collinear-but-farther from R[j]
        while True:
            ni = (i_u + 1) % n1
            val = cross(left[i_u], right[j_u], left[ni])
            if val > 0 or (val == 0 and dist2(right[j_u], left[ni]) > dist2(right[j_u], left[i_u])):
                i_u = ni
                moved = True
                steps += 1
                if steps > cap:
                    break
            else:
                break
        if steps > cap:
            break

        # move j CW while prev is above OR collinear-but-farther from L[i]
        while True:
            pj = (j_u - 1) % n2
            val = cross(left[i_u], right[j_u], right[pj])
            if val > 0 or (val == 0 and dist2(left[i_u], right[pj]) > dist2(left[i_u], right[j_u])):
                j_u = pj
                moved = True
                steps += 1
                if steps > cap:
                    break
            else:
                break

        if steps > cap or not moved:
            break

    # ---------- Lower tangent ----------
    i_l, j_l = i, j
    steps = 0
    while True:
        moved = False

        # move i CW while prev is below OR collinear-but-farther from R[j]
        while True:
            pi = (i_l - 1) % n1
            val = cross(left[i_l], right[j_l], left[pi])
            if val < 0 or (val == 0 and dist2(right[j_l], left[pi]) > dist2(right[j_l], left[i_l])):
                i_l = pi
                moved = True
                steps += 1
                if steps > cap:
                    break
            else:
                break
        if steps > cap:
            break

        # move j CCW while next is below OR collinear-but-farther from L[i]
        while True:
            nj = (j_l + 1) % n2
            val = cross(left[i_l], right[j_l], right[nj])
            if val < 0 or (val == 0 and dist2(left[i_l], right[nj]) > dist2(left[i_l], right[j_l])):
                j_l = nj
                moved = True
                steps += 1
                if steps > cap:
                    break
            else:
                break

        if steps > cap or not moved:
            break

    # ---------- Build merged hull CCW ----------
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

    hull = remove_collinear_ccw(hull)

    # ensure CCW orientation
    if len(hull) >= 3:
        area2 = 0
        for t in range(len(hull)):
            x1, y1 = hull[t]
            x2, y2 = hull[(t + 1) % len(hull)]
            area2 += x1 * y2 - x2 * y1
        if area2 < 0:
            hull.reverse()

    return hull


# -------------------- Benchmark --------------------

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
        results[name] = {"avg_ms": sum(times) / len(times) * 1000, "hull_size": len(hull)}
    return results


if __name__ == "__main__":
    for n in [100, 1000, 10000]:
        pts = generate_random(n)
        print(f"\nn={n}:")
        res = benchmark(pts)
        for algo, data in res.items():
            print(f"  {algo}: {data['avg_ms']:.3f}ms, hull={data['hull_size']}")
