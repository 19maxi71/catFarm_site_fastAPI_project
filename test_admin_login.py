#!/usr/bin/env python3
import urllib.request
import urllib.parse
import http.cookiejar
import json
import time

# Wait for server to start
time.sleep(3)

# Create a cookie jar to handle sessions
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

try:
    # First, try to access admin (should redirect to login)
    response = opener.open('http://localhost:8000/admin')
    print(f'Initial admin access: {response.getcode()}')

    # Login with admin credentials
    login_data = urllib.parse.urlencode({
        'username': 'admin',
        'password': 'admin123'
    }).encode('utf-8')

    login_request = urllib.request.Request(
        'http://localhost:8000/admin/login',
        data=login_data,
        method='POST'
    )
    login_request.add_header('Content-Type', 'application/x-www-form-urlencoded')

    login_response = opener.open(login_request)
    print(f'Login response: {login_response.getcode()}')

    # Now try to access the admin page again
    admin_response = opener.open('http://localhost:8000/admin')
    admin_content = admin_response.read().decode('utf-8')
    print(f'Admin page after login: {admin_response.getcode()}')

    if 'Cat Management' in admin_content:
        print('✓ Admin interface loaded successfully!')
        # Count cats by looking for litter_code occurrences
        cat_count = admin_content.count('litter_code')
        print(f'Found {cat_count} cats in the admin interface')

        # Check for specific cats
        if 'L001' in admin_content and 'L004' in admin_content:
            print('✓ All cats including ANTONIO (L004) are visible!')
        else:
            print('✗ Some cats missing from admin interface')
            if 'L004' not in admin_content:
                print('  - ANTONIO (L004) not found')
    else:
        print('✗ Admin interface not found in response')
        print(f'Content preview: {admin_content[:500]}...')

except Exception as e:
    print(f'Error: {e}')
