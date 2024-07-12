import json
import requests
import os
import boto3
import logging


def configure_logging():
  log_level = os.environ.get('LOG_LEVEL', 'INFO')
  numeric_level = getattr(logging, log_level.upper(), logging.INFO)
  if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)
  logging.basicConfig(level=numeric_level)


def rotate_keys(vault_token: str):
    reqUrl = f"{os.environ.get('VAULT_ADDR')}/v1/terraform/rotate-role/{os.environ.get('VAULT_TFC_ROLE')}"

    headersList = {
     "X-Vault-Namespace": os.environ.get('VAULT_NAMESPACE'),
     "X-Vault-Token": vault_token
    }
    
    payload = ""

    try:
        response = requests.request("POST", reqUrl, data=payload, headers=headersList)
        if response.status_code == 204:
            message = "Status Code: 204"
            logging.info("[INFO] The Terraform API Token has been rotated in the terraform secret engine.")
            return message
        else:
            raise Exception(f"Unknown response status: {response.status_code}")
    except Exception as e:
        logging.error(f"[ERROR] Unknown exception occured. {e}", exc_info=1)
        raise Exception(f"Unknown exception occured. {e}")
        

def main_rotate(client_token: str):
    client = boto3.client('sns', region_name='ap-southeast-2')
    vault_token = client_token
    
    try:
        rotate_keys(vault_token)
        response = client.publish(TopicArn=os.environ.get('DEST_SNS_SUCCESS'),Message="Terraform API Token has been rotated succefully.")
        logging.info("[INFO] Terraform API Token has been rotated succefully.")
        return (response)
    except Exception as e:
        logging.error(f"[ERROR] Error rotating the Terraform API Token in the secret engine. {e}", exc_info=1)
        response = client.publish(TopicArn=os.environ.get('DEST_SNS_FAILURE'),Message=f"Error rotating the Terraform API Token in the secret engine. Error message: {str(e)}")
        return {
          'statusCode': 500,
          'body': f"{respose}."
        }