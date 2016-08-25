from __future__ import absolute_import

from sentry.auth import register

from .provider import AdfsOAuth2Provider

register('afds_oauth2', AdfsOAuth2Provider)
