#!/usr/bin/env python3
import urllib.request
import json
import time

# Wait for server to start
time.sleep(3)

# Test the cats API endpoint
try:
    response = urllib.request.urlopen('http://localhost:8000/api/cats/')
    content = response.read().decode('utf-8')
    print(f'Status Code: {response.getcode()}')
    if response.getcode() == 200:
        data = json.loads(content)
        print(f'✓ API returned {len(data)} cats successfully!')
        for cat in data:
            print(f'  ID: {cat["id"]}, Name: {cat["name"]}, Litter: {cat["litter_code"]}, Created: {cat.get("created_at", "N/A")}')
    else:
        print(f'✗ API returned status {response.getcode()}')
        print(f'Content: {content}')
except Exception as e:
    print(f'✗ Error: {e}')
