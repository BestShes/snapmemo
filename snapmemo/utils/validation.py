import requests

from snapmemo import settings
from utils import customexception


class CheckSocialAccessToken():
    @staticmethod
    def check_facebook(access_token):

        url = 'https://graph.facebook.com/debug_token'
        param = {
            'input_token': access_token,
            'access_token': settings.COMMON_CONF_FILE['facebook']['app-access-token']
        }
        response = requests.get(url, params=param)
        response_dict = response.json()
        is_valid = response_dict['data']['is_valid']
        username = response_dict['data']['user_id']
        if is_valid:
            return username
        else:
            raise customexception.AuthenticateException('Invalid Access Token')

