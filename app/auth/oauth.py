import json
from flask import current_app, url_for, request, redirect, session

from requests_oauthlib import OAuth2Session
from urllib.request import urlopen

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    openid_url = "https://accounts.google.com/.well-known/openid-configuration"

    def __init__(self):
        super(GoogleSignIn, self).__init__("google")
        self.openid_config = json.load(urlopen(self.openid_url))
        self.session = OAuth2Session(
            client_id=self.consumer_id,
            redirect_uri=self.get_callback_url(),
            scope=self.openid_config["scopes_supported"]
        )

    def authorize(self):
        auth_url, _ = self.session.authorization_url(
            self.openid_config["authorization_endpoint"])
        return redirect(auth_url)

    def callback(self):
        if "code" not in request.args:
            return None, None

        self.session.fetch_token(
            token_url=self.openid_config["token_endpoint"],
            code=request.args["code"],
            client_secret=self.consumer_secret,
        )

        me = self.session.get(self.openid_config["userinfo_endpoint"]).json()
        print(me)
        return me["given_name"], me["email"]
