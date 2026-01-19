#!/usr/bin/env python3
"""
Wine Dashboard Server
Serves static files and handles pull list state persistence.
Run from project root: python scripts/server.py
Access: http://localhost:8080
"""

import http.server
import json
import os
from urllib.parse import urlparse

PORT = 8080

# Paths relative to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(PROJECT_ROOT, 'public')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
PULL_LIST_FILE = os.path.join(DATA_DIR, 'pull_list.json')

class WineHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        # Serve wine_collection.json from data directory
        if self.path == '/wine_collection.json':
            try:
                with open(os.path.join(DATA_DIR, 'wine_collection.json'), 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
            return

        # Serve pull_list.json from data directory
        if self.path == '/pull_list.json':
            try:
                with open(PULL_LIST_FILE, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{}')
            return

        # Default: serve from public directory
        super().do_GET()

    def do_POST(self):
        if self.path == '/pull_list.json':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(PULL_LIST_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    print(f'Project root: {PROJECT_ROOT}')
    print(f'Serving files from: {PUBLIC_DIR}')
    print(f'Data directory: {DATA_DIR}')

    with http.server.HTTPServer(('', PORT), WineHandler) as httpd:
        print(f'\nWine Dashboard Server running at http://localhost:{PORT}')
        print('Press Ctrl+C to stop')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped')
