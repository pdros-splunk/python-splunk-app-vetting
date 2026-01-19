import os
import json
import requests
import tempfile
import argparse
import threading
import webbrowser
from time import sleep
from base64 import b64encode

from const import *
from dotenv import load_dotenv

load_dotenv()

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def get_submit_response():
    idx = 0
    while response_submit is None:
        print(f'\r{VALIDATION_MESSAGES[idx % len(VALIDATION_MESSAGES)]}', end='', flush=True)
        sleep(10)
        idx += 1


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="FDSE App vettting processing tool"
    )
    parser.add_argument(
        "--app-dir",
        required=True,
        help="Path to the app for App vetting procoess"
    )
    parser.add_argument(
        "--cloud-only",
        required=False,
        help="If you want to run only cloud tests",
    )
    parser.add_argument(
        "--ssai-only",
        required=False,
        help="If you want to run only self-service",
    )
    
    args = parser.parse_args()

    print("Starting authentication process...")


    token = basic_auth(os.getenv("USER"), os.getenv("PASSWORD"))
    headers = {
    'Authorization': token
    }

    response_auth = requests.request("GET", LOGIN_URL, headers=headers)

    if not response_auth.status_code == 200:
        raise Exception(f"Login failed with status code {response_auth.status_code}: {response_auth.text}")
    print("Authentication successful.")

    jwt_token = response_auth.json().get('data', {}).get('token')
    # Submit file for validation
    file_path = args.app_dir
    file_name = file_path.split('/')[-1]

    files=[
    ('app_package',(file_name,open(file_path,'rb'),'application/x-tar'))
    ]
    headers_submit = {
    'Authorization': f'Bearer {jwt_token}'
    }

    if args.cloud_only:
        payload = {'included_tags': 'cloud'}
    elif args.ssai_only:
        payload = {'included_tags': 'self_service'}
    else:
        payload = {}    

    response_submit = None
    done = False
    t = threading.Thread(target=get_submit_response)
    t.start()
    
    response_submit = requests.request("POST", VALIDATE_URL, headers=headers_submit, files=files, data=payload)
    done = True
    if not response_submit.status_code == 200:
        raise Exception(f"App submission failed with status code {response_submit.status_code}: {response_submit.text}")

    print("\nApp submitted successfully. Monitoring validation status...")
    request_id = response_submit.json().get('request_id')
    status = False
    status_url = f"{STATUS_URL}/{request_id}"
    idx = 0
    while status is False:
        print(f'\r{WAITING_MESSAGES[idx % len(WAITING_MESSAGES)]}', end='', flush=True)
        sleep(60)

        response_status = requests.request("GET", status_url, headers=headers_submit)
        if response_status.status_code != 200:
            raise Exception(f"Status check failed with status code {response_status.status_code}: {response_status.text}")

        if response_status.json().get('status').lower() == 'success':
            print(f"\nStatus success, json results: {json.dumps(response_status.json(), indent=4)}")
            print('\nGenerating HTML preview of results...')
            status = True
        idx += 1

    headers_submit.update({'Content-Type':'text/html'})
    report_url = f"{REPORT_URL}/{request_id}"
    response_report = requests.request("GET", report_url, headers=headers_submit)
    if response_report.status_code != 200:
        raise Exception(f"Report retrieval failed with status code {response_report.status_code}: {response_report.text}")
    

    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(response_report.text)
        webbrowser.open(f'file://{f.name}')
    
    print('Done. HTML report opened in web browser.')
    