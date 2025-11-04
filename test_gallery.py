import requests
import base64

# Create a simple test image (1x1 pixel PNG in base64)
test_image_base64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='

# Test the API endpoint
url = 'http://localhost:8000/api/articles/1/images/'
data = {
    'image_base64': test_image_base64,
    'caption': 'Test gallery image',
    'display_order': 1
}

try:
    response = requests.post(url, json=data)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Error: {e}')
