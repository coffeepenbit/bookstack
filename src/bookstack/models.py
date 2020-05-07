from json.decoder import JSONDecodeError
import string
import urllib

from cached_property import cached_property
import inflection
import requests


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
        self.token_id = None
        self.token_secret = None
        self._api_path = api_path

        self.available_api_methods = set()
        self._session = BaseURLSession(self.api_base_url)
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
        return self._session.request('GET', self._api_path).json()

    def _create_api_method(self, method_info):
        def request_method(**kwargs):
            response = self._session.request(
                method_info['method'],
                method_info['uri'].format(**kwargs)
            )
            
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


class BaseURLSession(requests.Session):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url_path, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url_path)
        
        return super().request(method, url, *args, **kwargs)


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