from json.decoder import JSONDecodeError
import string
import urllib
import time

from cached_property import cached_property
import inflection
import requests
from requests_ratelimiter import LimiterSession

API_PATH = 'api/docs.json/'


class BookStack:
    def __init__(
                self,
                base_url,
                token_id=None,
                token_secret=None,
                api_path=API_PATH
            ):
        self.api_base_url = base_url
        self.token_id = token_id
        self.token_secret = token_secret
        self._api_path = api_path
        self.rate_limit=180 # Bookstack default

        self.available_api_methods = set()
        self._session = BaseURLSession(self.api_base_url, per_minute=self.rate_limit)
        self._session.auth = Auth(token_id, token_secret)

    def generate_api_methods(self):
        for base_model_info in self._get_api().values():
            for method_info in base_model_info:
                method_name = self._create_method_name(method_info)

                setattr(
                    self, 
                    method_name,
                    self._create_api_method(method_info)
                )

                self.available_api_methods.add(method_name)

    def _get_api(self):
        r = self._session.request('GET', self._api_path)

        rate_limit = int(r.headers.get('X-RateLimit-Limit', self.rate_limit))
        if rate_limit != self.rate_limit:
            # Create a new rate limited session with the correct rate limit
            self._session = BaseURLSession(self.api_base_url, per_minute=self.rate_limit)
            self._session.auth = Auth(self.token_id, self.token_secret)
            self.rate_limit = rate_limit

        return r.json()

    def _create_api_method(self, method_info):
        def request_method(*args, **kwargs):
            uri = method_info['uri']
            arg = args
            params = kwargs.get('params')
            if method_info['method'] != "POST":
                try:
                    uri = uri.replace('{id}', str(args[0]['id']))
                    del arg[0]["id"]
                except:
                    pass
            if method_info['method'] == "POST" or method_info['method'] == "PUT":
                response = self._session.request(method_info['method'], uri, json=arg[0], params=params)
            else:
                response = self._session.request(method_info['method'], uri.format(arg), params=params)
            return self._get_response_content(response)
        return request_method

    @staticmethod
    def _get_api_args(uri):
        return [api_arg
                for _, api_arg, _, _ in string.Formatter().parse(uri)]

    def _create_method_name(self, method_info):
        return self._format_camelcase(
            '_'.join([method_info['method'], method_info['name']])
        )

    @staticmethod
    def _format_camelcase(string_):
        return inflection.underscore(string_)

    @staticmethod
    def _get_response_content(response):
        try:
            content = response.json()
        except JSONDecodeError:
            content = response.text

        return content


class BaseURLSession(LimiterSession):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url_path, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url_path)
        response = super().request(method, url, *args, **kwargs)

        # Handle 'Too Many Attempts' response
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            response = super().request(method, url, *args, **kwargs)

        return response


class Auth(requests.auth.AuthBase):
    def __init__(self, 
                token_id, 
                token_secret, 
                header_key='Authorization'
            ):
        self.header_key = header_key
        self.token_id = token_id
        self.token_secret = token_secret

    def __call__(self, r):
        r.headers[self.header_key] = \
            f'Token {self.token_id}:{self.token_secret}'

        return r
