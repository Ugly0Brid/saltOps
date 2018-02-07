from django.conf import settings
from common.salt_https_api import salt_api_token


def token_id():
    s = salt_api_token(
        {
            "username": settings.SALT_USER,
            "password": settings.SALT_PASSWORD,
            "eauth": "pam"
        },
        settings.SALT_REST_URL + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token
