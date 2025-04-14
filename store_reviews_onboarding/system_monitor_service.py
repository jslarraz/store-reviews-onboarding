import psutil
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SystemMonitorService(BaseHTTPRequestHandler):

    def do_GET(self):
        # Get system stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory()
        response = {"cpu_percent": cpu_percent, "memory_usage": memory_usage.percent}

        # Return response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="Port to listen on.")
    args = parser.parse_args()

    port = args.port if args.port else 8080
    httpd = HTTPServer(('', port), SystemMonitorService)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()
