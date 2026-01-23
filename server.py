from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json, time
from convex_hull import graham_scan, divide_conquer

class ConvexHullHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/compute':
            self.send_error(404)
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length).decode())
            pts = [tuple(p) for p in data]

            t = time.perf_counter()
            hull_g = graham_scan(pts)
            t1 = (time.perf_counter() - t) * 1000

            t = time.perf_counter()
            hull_d = divide_conquer(pts)
            t2 = (time.perf_counter() - t) * 1000

            result = {
                'graham': {'hull': hull_g, 'time_ms': t1},
                'divide_conquer': {'hull': hull_d, 'time_ms': t2}
            }

            self.send_response(200)
        except Exception as e:
            result = {'error': str(e)}
            self.send_response(400)

        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server = ThreadingHTTPServer(('localhost', 8000), ConvexHullHandler)
    print('http://localhost:8000')
    server.serve_forever()
