import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4
from pymongo import MongoClient

# MongoDB Client Setup
client = MongoClient(os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['product_db']
collection = db['products']

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path == '/register_product':
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            product_info = json.loads(post_data)

            # Generate UUIDs
            product_id = str(uuid4())
            categories = [
                str(uuid4()) for _ in product_info.get('categories', [])
            ]

            # Create Product Document
            product = {
                "id": product_id,
                "stock": 0,  # Default stock
                "description": product_info.get('description', ''),
                "categories": categories,
                "price": float(product_info.get('price', '0'))
            }

            # Insert into MongoDB
            collection.insert_one(product)

            # Respond
            self._set_headers()
            self.wfile.write(json.dumps({"id": product_id}).encode())

    def do_GET(self):
        if self.path.startswith('/get_product'):
            # Extract product ID from query parameters
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            product_id = query_components.get('id', [None])[0]

            if not product_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Product ID is required"}).encode())
                return

            # Fetch from MongoDB
            product = collection.find_one({"id": product_id})

            if product:
                product['_id'] = str(product['_id'])  # Convert ObjectId to string
                self._set_headers()
                self.wfile.write(json.dumps(product, default=str).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running at http://localhost:{port}/')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
