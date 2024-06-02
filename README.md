# fortigateAPI

API's are the backbone of automation, assurnace and programability as they provide infrastructure as code mechanisms to connect to devices, and acheive multiple functions. 

## Overview

 Python Code that allows CyberSecurity Engineers setup new or existing Fortigate firewalls for API access without having to use the GUI or CLI.

## Use Case Description

This use case is particularly helpful in situations where you have a large number of existing devices in a network and FortiManager is not deployed, this will reduce the manual overhead of each device from 5mins to literally 5 seconds (average time to run the script on EveNG) 

## Contacts
*Oluyemi Oshunkoya (yemi_o@outlook.com)

## Solution Components
*Python

## Prerequisites 

Python3.6 and above

EveNG or live lab environment running FortiOS 7.x and above (should work with lower versions as well)

You also need the requests library which you can get using the command below 

```
pip install requests 

```


## Step 1 - Logging into the Firewall and extracting Session Cookie

This step assumes the presence of at least one superadmin user created on the firewall post-setup.
   
```
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

```

## Step 2 - Creating an authorization profile and granting specific context access 

In this use case, i intend to capture configuration backups which is under the systemgrp context that i granted read/write permissions. 

It is advisable to only grant the specific permissions required per use-case.
   
```

# Create an authorization profile.

profile_url = f"{base_url}/api/v2/cmdb/system/accprofile"
profile_payload = {
    "name": "your-auth-profile",
    "sysgrp": "read-write"
}
response = session.post(profile_url, headers=headers, json=profile_payload, verify=False)

if response.status_code == 200:
    print(f"Authorization profile {your-auth-profile} created successfully!")
else:
    print(response.status_code)    
    print("Failed to create authorization profile!")
    print(response.text)
```

## Step 3 - Creating a specific user for the restAPI admin calls.
   
```
# Create a RestAPI User (You can modify this to match your requirements)

user_url = f"{base_url}/api/v2/cmdb/system/api-user"
user_payload = {
    "name": "your-restapi-user",
    "password": "your-password",
    "accprofile": "your-auth-profile"
}
response = session.post(user_url, headers=headers, json=user_payload, verify=False)

if response.status_code == 200:
    print("User created successfully!")
else:
    print(response.status_code)
    print("Failed to create user!")
    print(response.text)
```

## Step 4 - Generating the API Token
   
```
# Generate a token id for the user restapi_admin

token_url = f"{base_url}/api/v2/monitor/system/api-user/generate-key"
token_payload = {
    "api-user": "your-restapi-user",
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
```

## Putting it all together 

1. Clone this git repository
2. Update the variables in the code with your actual requirements (its better to use an .env file for the sensitive data)
3. Run python Main.py to generate the token.
