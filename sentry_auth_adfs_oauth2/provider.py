from __future__ import absolute_import, print_function

from sentry.auth.providers.oauth2 import (
    OAuth2Callback, OAuth2Provider, OAuth2Login
)

from .constants import (
    AUTHORIZE_URL, ACCESS_TOKEN_URL, CLIENT_ID, DATA_VERSION,
    RESOURCE, COMPANY_NAME, EMAIL_KEY, FIRSTNAME_KEY, LASTNAME_KEY
)
from .views import FetchUser, AdfsOAuth2ConfigureView


class AdfsOAuth2Login(OAuth2Login):
    authorize_url = AUTHORIZE_URL
    client_id = CLIENT_ID
    relying_party_trust = RESOURCE

    def __init__(self, adfs=None):
        self.adfs = adfs
        super(AdfsOAuth2Login, self).__init__()

    def get_authorize_params(self, state, redirect_uri):
        params = super(AdfsOAuth2Login, self).get_authorize_params(
            state, redirect_uri
        )

        params['resource'] = self.relying_party_trust

        # ADFS doesn't like these
        del params['scope']
        return params


class AdfsOAuth2Provider(OAuth2Provider):
    company_name = COMPANY_NAME or "Unknown"
    name = company_name + ' ADFS OAuth2'
    client_id = CLIENT_ID
    client_secret = "Thanks Microsoft!"

    def __init__(self, adfs=None, version=None, **config):
        self.adfs = adfs
        # if adfs is not configured this is part of the setup pipeline
        # this is a bit complex in Sentry's SSO implementation as we don't
        # provide a great way to get initial state for new setup pipelines
        # vs missing state in case of migrations.
        if adfs is None:
            version = DATA_VERSION
        else:
            version = None
        self.version = version
        super(AdfsOAuth2Provider, self).__init__(**config)

    def get_configure_view(self):
        return AdfsOAuth2ConfigureView.as_view()

    def get_auth_pipeline(self):
        return [
            AdfsOAuth2Login(adfs=self.adfs),
            OAuth2Callback(
                access_token_url=ACCESS_TOKEN_URL,
                client_id=self.client_id,
                client_secret=self.client_secret,
            ),
            FetchUser(
                adfs=self.adfs,
                version=self.version,
            ),
        ]

    def get_refresh_token_url(self):
        return ACCESS_TOKEN_URL

    def build_config(self, state):
        self.ver = state['ver']
        return {
            'adfs': {
                'ver': state['ver'],
                'aud': state['aud'],
                'iss': state['iss'],
                'appid': state['appid'],
                'authmethod': state['authmethod'],
            },
            'version': DATA_VERSION,
        }

    def build_identity(self, state):
        # These keys heavily depend on your ADFS OAuth2 claim settings
        # data.user = {
        #     'First_Name': 'My First Name',
        #     'Last_Name': 'My Last Name',
        #     'ver': '1.0',
        #     'aud': 'Relying Party Trust',
        #     'iss': 'http://server.com/adfs/services/trust',
        #     'authmethod': 'http://schemas.microsoft.com/ws/2008/06/identity/authenticationmethod/windows',
        #     'appid': 'Some ID',
        #     'exp': 01234,
        #     'auth_time': '2016-08-23T16:27:42.977Z',
        #     'iat': 01234,
        #     'Email': 'derp@herp.com'
        # }
        data = state['data']
        user_data = state['user']
        return {
            'id': user_data[EMAIL_KEY],
            'email': user_data[EMAIL_KEY],
            'name': user_data[FIRSTNAME_KEY] + " " + user_data[LASTNAME_KEY],
            'data': self.get_oauth_data(data),
        }
