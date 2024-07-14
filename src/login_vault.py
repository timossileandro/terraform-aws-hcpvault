import boto3
import botocore.session
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
import json
import base64
import os
import logging


def configure_logging():
  log_level = os.environ.get('LOG_LEVEL', 'INFO')
  numeric_level = getattr(logging, log_level.upper(), logging.INFO)
  if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)
  logging.basicConfig(level=numeric_level)


def create_signed_request(url, region, service, body=''):
    session = botocore.session.get_session()
    credentials = session.get_credentials().get_frozen_credentials()

    request = AWSRequest(
        method='POST',
        url=url,
        data=body,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    SigV4Auth(credentials, service, region).add_auth(request)
    
    return request.url, request.headers, body


def main_login():
    try:
        vault_url = f'{os.environ.get('VAULT_ADDR')}/v1/auth/aws/login'
        vault_region = os.environ.get('AWS_REGION')
        vault_service = 'sts'
        body = 'Action=GetCallerIdentity&Version=2011-06-15'

        signed_url, signed_headers, signed_body = create_signed_request(vault_url, vault_region, vault_service, body)

        signed_url_base64 = base64.b64encode(signed_url.encode()).decode()
        signed_body_base64 = base64.b64encode(signed_body.encode()).decode()

        auth_payload = {
            'role': os.environ.get('VAULT_AWS_ROLE'),
            'iam_http_request_method': 'POST',
            'iam_request_url': signed_url_base64,
            'iam_request_body': signed_body_base64,
            'iam_request_headers': {k: v for k, v in signed_headers.items()}
        }
        
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*',
            'X-Vault-Namespace': os.environ.get('VAULT_NAMESPACE')
        }

        response = requests.post(vault_url, json=auth_payload, headers=headers)
        response_json = response.json()
        client_token = response_json['auth']['client_token']
        print(f"Client Token: {client_token}")
        
        if response.status_code == 200:
            logging.info("[INFO] Login in Vault using AWS Auth method has been successfully.")
            logging.info("[INFO] Client Token has been retrieved successfully.")
            return client_token
        else:
            raise Exception(f"Unknown response status: {response.status_code}")
              
    except requests.exceptions.RequestException as e:
        logging.error(f"[ERROR] Failed login in Vault!", exc_info=1)
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {e}")
        }