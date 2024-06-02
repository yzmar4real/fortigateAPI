import requests
import json

# FortiGate credentials and URL
fortigate_ip = "your-foritgate-ip"
username = "your-username"
password = "your-password%"
base_url = f"https://{fortigate_ip}"

# Disable warnings for insecure connections
requests.packages.urllib3.disable_warnings()

# Log in and get the session cookie
login_url = f"{base_url}/logincheck"
login_payload = {
    'username': username,
    'secretkey': password
}
session = requests.session()
response = session.post(login_url, data=login_payload, verify=False)

if response.status_code != 200:
    print("Login failed!")
    print(response.text)
    exit()

# Get CSRF token
csrf_token = session.cookies.get('ccsrftoken')
if csrf_token:
    csrf_token = csrf_token.strip('"')

headers = {
    'X-CSRFTOKEN': csrf_token,
    'Content-Type': 'application/json'
}

# Create an authorization profile called restAPI_special
profile_url = f"{base_url}/api/v2/cmdb/system/accprofile"
profile_payload = {
    "name": "restAPI_special",
    "sysgrp": "read-write"
}
response = session.post(profile_url, headers=headers, json=profile_payload, verify=False)

if response.status_code == 200:
    print("Authorization profile restAPI created successfully!")
else:
    print(response.status_code)    
    print("Failed to create authorization profile!")
    print(response.text)
    # exit()


# Create a user called restapi_admin 
## You should replace this section of the code with your own variables

user_url = f"{base_url}/api/v2/cmdb/system/api-user"
user_payload = {
    "name": "restapi_admin",
    "password": "your-password",
    "accprofile": "restAPI_special" 
}
response = session.post(user_url, headers=headers, json=user_payload, verify=False)

if response.status_code == 200:
    print("User restapi_admin created successfully!")
else:
    print(response.status_code)
    print("Failed to create user!")
    print(response.text)
    # exit()

# Generate a token id for the user restapi_admin
# Correct endpoint for generating API token
token_url = f"{base_url}/api/v2/monitor/system/api-user/generate-key"
token_payload = {
    "api-user": "restapi_admin",
    "vdom": "root"       
}
response = session.post(token_url, headers=headers, json=token_payload, verify=False)

if response.status_code == 200:
    token_data = response.json()
    if 'access_token' in token_data['results'].keys():
        token_id = token_data['results']['access_token']
        print("Token generated successfully!")
        print(f"Token ID: {token_id}")
    else:
        print("Token generation failed!")
        print(token_data)
else:
    print("Failed to generate token!")
    print(response.text)
