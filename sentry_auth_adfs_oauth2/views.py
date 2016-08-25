from __future__ import absolute_import, print_function

import logging

from sentry.auth.view import AuthView, ConfigureView
from sentry.utils import json

from .constants import (
    ERR_INVALID_RESPONSE,
)
from .utils import urlsafe_b64decode

logger = logging.getLogger('sentry.auth.adfs.oauth2')


class FetchUser(AuthView):
    def __init__(self, adfs, version, *args, **kwargs):
        self.adfs = adfs
        self.version = version
        super(FetchUser, self).__init__(*args, **kwargs)

    def dispatch(self, request, helper):
        data = helper.fetch_state('data')

        try:
            access_token = data['access_token']
        except KeyError:
            logger.error('Missing access_token in OAuth response: %s' % data)
            return helper.error(ERR_INVALID_RESPONSE)

        try:
            _, payload, _ = map(urlsafe_b64decode, access_token.split('.', 2))
        except Exception as exc:
            logger.error(u'Unable to decode access_token: %s' % exc, exc_info=True)
            return helper.error(ERR_INVALID_RESPONSE)

        try:
            payload = json.loads(payload)
        except Exception as exc:
            logger.error(u'Unable to decode access_token payload: %s' % exc, exc_info=True)
            return helper.error(ERR_INVALID_RESPONSE)

        if not payload.get('Email'):
            logger.error('Missing email in access_token payload: %s' % access_token)
            return helper.error(ERR_INVALID_RESPONSE)

        helper.bind_state('ver', payload.get('ver'))
        helper.bind_state('aud', payload.get('aud'))
        helper.bind_state('iss', payload.get('iss'))
        helper.bind_state('appid', payload.get('appid'))
        helper.bind_state('authmethod', payload.get('authmethod'))
        helper.bind_state('user', payload)

        return helper.next_step()


class AdfsOAuth2ConfigureView(ConfigureView):
    def dispatch(self, request, organization, auth_provider):
        return self.render('sentry_auth_adfs_oauth2/configure.html')
