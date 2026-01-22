"""Simple HTTP server for convex hull visualization"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import time
from convex_hull import graham_scan, divide_conquer

class ConvexHullHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/compute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            points = json.loads(post_data)
            
            # Convert to tuples for processing
            pts = [tuple(p) for p in points]
            
            # Compute Graham Scan
            t1 = time.perf_counter()
            hull_graham = graham_scan(pts)
            t1 = (time.perf_counter() - t1) * 1000
            
            # Compute Divide & Conquer
            t2 = time.perf_counter()
            hull_dc = divide_conquer(pts)
            t2 = (time.perf_counter() - t2) * 1000
            
            result = {
                'graham': {
                    'hull': [list(p) for p in hull_graham],
                    'time_ms': t1
                },
                'divide_conquer': {
                    'hull': [list(p) for p in hull_dc],
                    'time_ms': t2
                }
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('localhost', port), ConvexHullHandler)
    print(f'Server running at http://localhost:{port}')
    print('Open index.html in browser to use the visualizer')
    server.serve_forever()
