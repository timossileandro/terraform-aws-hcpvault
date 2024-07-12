from login_vault import main_login
from config_token import main_config
from rotate_token import main_rotate


def lambda_handler(event, context):
    token: str
    config: str
    rotate: str

    try:
        token = main_login()
        config = main_config(token)
        rotate = main_rotate(token)
        return ()

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500
        }