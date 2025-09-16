#!/usr/bin/env python3
import urllib.request
import urllib.error

# Test the admin endpoint
try:
    response = urllib.request.urlopen("http://localhost:8001/admin")
    content = response.read().decode('utf-8')
    print(f"Status Code: {response.getcode()}")
    print(f"Content Type: {response.headers.get('content-type', 'N/A')}")
    if response.getcode() == 200:
        print("✓ Admin endpoint is working!")
        # Check if it contains expected content
        if "Cat Management" in content:
            print("✓ Custom admin interface is being served!")
        else:
            print("✗ Custom admin interface not found in response")
            print(f"First 500 chars: {content[:500]}")
    else:
        print(f"✗ Admin endpoint returned status {response.getcode()}")
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error: {e.code} - {e.reason}")
except Exception as e:
    print(f"✗ Error testing admin endpoint: {e}")
