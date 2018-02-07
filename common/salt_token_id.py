from rsc.common.salt_https_api import salt_api_token

SALT_REST_URL = 'http://10.100.11.208:8001/'
SALT_USER = 'sa'
SALT_PASSWORD = 'sapassword'


def token_id():
    s = salt_api_token(
        {
            "username": SALT_USER,
            "password": SALT_PASSWORD,
            "eauth": "pam"
        },
        SALT_REST_URL + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token
