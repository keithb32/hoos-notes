########################################################################################
#  REFERENCES
#
#  Title: my_adapter.py
#  Author: Moeedlodhi
#  Date: 6/21/2021
#  URL: https://medium.com/geekculture/getting-started-with-django-social-authentication-80ee7dc26fe0
#
#  Title: django-allauth
#  Author: Raymond Penners
#  Code version: 0.46.0
#  URL: https://github.com/pennersr/django-allauth
#  Software license: MIT
#
#  Title: django-rest-framework
#  Author: Encode OSS Ltd
#  Code version: 3.11.0
#  URL: https://github.com/encode/django-rest-framework/tree/master
#  Software license: BSD-3
#
#  Title: django-rest-auth
#  Author: Tivix Inc.
#  Code version: 0.9.5
#  URL: https://github.com/Tivix/django-rest-auth
#  Software license: MIT
########################################################################################

from django.contrib.auth import get_user_model
User = get_user_model()
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.response import Response


# MyAdapter, a class for handling email collisions
# Reference: my_adapter.py by Moeedlodhi (tutorial)
class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        if sociallogin.is_existing:
            return

            # some social logins don't have an email address, e.g. facebook accounts
            # with mobile numbers only, but allauth takes care of this case so just
            # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return
        try:
            user = User.objects.get(email=sociallogin.user.email)
            sociallogin.connect(request, user)
            # Create a response object
            raise ImmediateHttpResponse('hello')
        except User.DoesNotExist:
            pass