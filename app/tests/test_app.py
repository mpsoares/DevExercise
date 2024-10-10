import unittest
import requests
import threading
import app.app as app

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a new thread
        server_thread = threading.Thread(target=app.run)
        server_thread.daemon = True
        server_thread.start()

    def test_register_product(self):
        url = 'http://localhost:8000/register_product'
        data = {
            "description": "Test Product",
            "categories": [{"name": "Category1"}, {"name": "Category2"}],
            "price": "19.99"
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_product(self):
        # First, register a product
        url = 'http://localhost:8000/register_product'
        data = {
            "description": "Test Product",
            "categories": [{"name": "Category1"}],
            "price": "9.99"
        }
        response = requests.post(url, json=data)
        product_id = response.json().get('id')

        # Now, retrieve the product
        url = f'http://localhost:8000/get_product?id={product_id}'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        product = response.json()
        self.assertEqual(product.get('id'), product_id)

if __name__ == '__main__':
    unittest.main()
