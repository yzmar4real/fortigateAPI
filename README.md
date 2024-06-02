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

## Step 1 - Logging into the Firewall 

This step assumes the presence of at least one superadmin user created on the firewall post-setup.
   
```
import requests

fortigate_ip = "192.168.1.1"
username = "admin"
password = "your_password"
login_url = f"https://{fortigate_ip}/logincheck"

session = requests.session()
login_payload = {'username': username, 'secretkey': password}
response = session.post(login_url, data=login_payload, verify=False)

if response.status_code == 200:
    print("Login successful")
else:
    print("Login failed")

```

## Step 2 - Creating an authorization profile and granting specific context access 

In this use case, i intend to capture configuration backups which is under the systemgrp context that i granted read/write permissions. 

It is advisable to only grant the specific permissions required per use-case.
   
```
profile_url = f"https://{fortigate_ip}/api/v2/cmdb/system/admin"
profile_payload = {"name": "restAPI", "accprofile": "super_admin"}

response = session.post(profile_url, json=profile_payload, verify=False)
if response.status_code == 200:
    print("Profile created successfully")
else:
    print("Failed to create profile")
```

## Step 3 - Creating a specific user for the restAPI admin calls. 
   
```
user_url = f"https://{fortigate_ip}/api/v2/cmdb/user/local"
user_payload = {"name": "restapi_admin", "password": "StrongPassword123"}

response = session.post(user_url, json=user_payload, verify=False)
if response.status_code == 200:
    print("User created successfully")
else:
    print("Failed to create user")
```

## Step 4 - Generating the API Token
   
```
token_url = f"https://{fortigate_ip}/api/v2/system/api-user/generate"
token_payload = {"name": "restapi_admin", "profile": "restAPI", "vdom": "root"}

response = session.post(token_url, json=token_payload, verify=False)
if response.status_code == 200:
    token = response.json().get('token')
    print(f"Token generated successfully: {token}")
else:
    print("Failed to generate token")

```

## Putting it all together 

1. Clone this git repository
2. Update the variables in the code with your actual requirements (its better to use an .env file for the sensitive data)
3. Run python Main.py to generate the token.
