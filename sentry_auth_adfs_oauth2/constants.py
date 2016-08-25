from __future__ import absolute_import, print_function

from django.conf import settings

COMPANY_NAME = getattr(settings, 'ADFS_OAUTH2_COMPANY_NAME', None)

AUTHORIZE_URL = getattr(settings, 'ADFS_OAUTH2_AUTH_URL', None)

ACCESS_TOKEN_URL = getattr(settings, 'ADFS_OAUTH2_TOKEN_URL', None)

CLIENT_ID = getattr(settings, 'ADFS_OAUTH2_CLIENT_ID', None)

RESOURCE = getattr(settings, 'ADFS_OAUTH2_RESOURCE', None)

EMAIL_KEY = getattr(settings, 'ADFS_OAUTH2_EMAIL_KEY', None)
FIRSTNAME_KEY = getattr(settings, 'ADFS_OAUTH2_FIRSTNAME_KEY', None)
LASTNAME_KEY = getattr(settings, 'ADFS_OAUTH2_LASTNAME_KEY', None)

ERR_INVALID_RESPONSE = 'Unable to fetch user information from ADFS.  Please check the log.'

DATA_VERSION = '1'
