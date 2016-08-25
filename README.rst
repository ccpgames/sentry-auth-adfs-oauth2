ADFS OAuth2 Auth for Sentry
======================

``ADFS_OAUTH2_COMPANY_NAME`` - Prefix to use for naming the provider

``ADFS_OAUTH2_AUTH_URL`` - Should look something like: https://adfs.yourcompany.com/adfs/oauth2/authorize

``ADFS_OAUTH2_TOKEN_URL`` - Should looke somethinhg like: https://adfs.yourcompany.com/adfs/oauth2/token

``ADFS_OAUTH2_CLIENT_ID`` - This is usually an UUID looking thing

``ADFS_OAUTH2_RESOURCE`` - Also known as the Relying Party Trust.

These are configured by your ADFS server claim response.

``ADFS_OAUTH2_EMAIL_KEY`` - The key which the claim uses in the token to denote the authorized user's email.

``ADFS_OAUTH2_FIRSTNAME_KEY`` - The key which the claim uses in the token to denote the authorized user's first name.

``ADFS_OAUTH2_LASTNAME_KEY`` - The key which the claim uses in the token to denote the authorized user's last name.
