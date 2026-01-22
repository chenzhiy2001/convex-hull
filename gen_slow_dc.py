import math
from convex_hull import graham_scan, divide_conquer, benchmark

def circle_points(n, r=400, cx=300, cy=250):
    return [(cx + r*math.cos(2*math.pi*i/n), cy + r*math.sin(2*math.pi*i/n)) for i in range(n)]

if __name__ == "__main__":
    for n in [100, 500, 1000]:
        pts = circle_points(n)
        res = benchmark(pts, runs=5)
        print(f"n={n}: Graham={res['graham']['avg_ms']:.3f}ms, D&C={res['divide_conquer']['avg_ms']:.3f}ms")
