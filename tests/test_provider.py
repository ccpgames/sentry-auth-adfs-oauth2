from __future__ import absolute_import

import pytest

from sentry.auth.exceptions import IdentityNotValid
from sentry.models import AuthIdentity, AuthProvider
from sentry.testutils import TestCase

from sentry_auth_adfs_oauth2.provider import AdfsOAuth2Provider

COMPANY_NAME = 'Test'

class AdfsOAuth2ProviderTest(TestCase):
    def setUp(self):
        self.org = self.create_organization(owner=self.user)
        self.user = self.create_user('foo@example.com')
        self.auth_provider = AuthProvider.objects.create(
            provider='oauth2',
            organization=self.org,
        )
        self.provider = self.get_provider()
        super(AdfsOAuth2ProviderTest, self).setUp()

    def get_provider(self):
        self.provider = AdfsOAuth2Provider(
            key=self.auth_provider.provider
        )

    def test_refresh_identity_without_refresh_token(self):
        auth_identity = AuthIdentity.objects.create(
            auth_provider=self.auth_provider,
            user=self.user,
            data={
                'access_token': 'access_token',
            }
        )

        provider = AdfsOAuth2Provider(key=self.auth_provider.provider)
        with pytest.raises(IdentityNotValid):
            provider.refresh_identity(auth_identity)
