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


def get_credentials(reqUrl: str, namespace: str, vault_token: str):
    headersList = {
     "X-Vault-Namespace": namespace,
     "X-Vault-Token": vault_token,
     "Content-Type": "application/json" 
    }
    
    payload = ""
    token: str
    
    try: 
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        if response.status_code == 200:
            response_json = response.json()
            token = response_json.get('data', {}).get('token', None)
            logging.info("[INFO] Token has been retrieved and it going to be saved to be configured in Vault under the terraform secret engine.")
            return token
        else:
            raise Exception(f"Unknown response status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[ERROR] Failed while fetching credentials from {reqUrl}", exc_info=1)
        raise Exception(f"Failed while fetching credentials from {reqUrl}")
    except Exception as e:
        logging.error(f"[ERROR] Unknown exception occured. {e}", exc_info=1)
        raise Exception(f"Unknown exception occured. {e}")

    
def config_terraform_key(new_token: str, reqUrl: str, namespace: str, vault_token: str):
    headersList = {
     "X-Vault-Namespace": namespace,
     "X-Vault-Token": vault_token,
     "Content-Type": "application/json" 
    }
    
    payload = json.dumps({
      "token": new_token
    })
    
    try:
        response = requests.request("POST", reqUrl, data=payload, headers=headersList)
        
        if response.status_code == 204:
            message = "Status Code: 204"
            logging.info("[INFO] The new Terraform API Token has been configured in the terraform secret engine.")
            return message
        else:
            raise Exception(f"Unknown response status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"[ERROR] Failed while configuring the new API Token posting the request using {reqUrl}", exc_info=1)
        raise Exception(f"Failed while configuring the new API Token posting the request using {reqUrl}")
    except Exception as e:
        logging.error(f"[ERROR] Unknown exception occured. {e}", exc_info=1)
        raise Exception(f"Unknown exception occured. {e}")
        
        
def main_config(client_token: str):
    reqUrl_getcreds = f"{os.environ.get('VAULT_ADDR')}/v1/terraform/creds/{os.environ.get('VAULT_TFC_ROLE')}"
    reqUrl_config = f"{os.environ.get('VAULT_ADDR')}/v1/terraform/config"
    namespace = os.environ.get('VAULT_NAMESPACE')
    vault_token = client_token
    client = boto3.client('sns')

    configure_logging()
    
    try:
        new_token = get_credentials(reqUrl_getcreds, namespace, vault_token)
        config_terraform_key(new_token, reqUrl_config, namespace, vault_token)
        response = client.publish(TopicArn=os.environ.get('DEST_SNS_SUCCESS'),Message="[INFO] A new Terraform API Token has been updated in Vault under the terraform secret engine successfully.")
        logging.info("[INFO] A new Terraform API Token has been updated in Vault under the terraform secret engine successfully.")
        return (response)
    except Exception as e:
        logging.error(f"[ERROR] Error updating the new Terraform API Token in the secret engine. {e}", exc_info=1)
        response = client.publish(TopicArn=os.environ.get('DEST_SNS_FAILURE'),Message=f"[ERROR] Error updating the new Terraform API Token in the secret engine. Error message: {str(e)}")
        return {
          'statusCode': 500,
          'body': f"{respose}."
        }