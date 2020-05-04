import urllib

import requests


class BookStack:
    def __init__(self, base_url, token_id=None, token_secret=None):
        self.api_base_url = self._create_api_base_url(base_url)
        self.token_id = None
        self.token_secret = None

        self._session = BaseURLSession(self.api_base_url)
        self._session.auth = Auth(token_id, token_secret)

        self.endpoint_paths = {
            'docs': 'docs.json/',
            'books': 'books/',
            'shelves': 'shelves/',
            'export_text': 'export/plaintext',
            'export_html': 'export/html'
        }
    
    @staticmethod
    def _create_api_base_url(base_url):
        parsed_url = urllib.parse.urlparse(base_url)
        if 'api' in str(parsed_url.path):
            parsed_url = parsed_url
        else:
            parsed_url = parsed_url._replace(**{'path': 'api/'})

        return parsed_url.geturl()

    def get_docs(self):
        return self._session.get(self.endpoint_paths['docs']).json()

    def get_books(self):
        return self._session.get(self.endpoint_paths['books']).json()

    def read_book(self, book_id):
        return self._session.get(
            urllib.parse.urljoin(
                self.endpoint_paths['books'],
                str(book_id)
            )
        ).json()

    def export_text(self, book_id):
        return self._session.get(
            urllib.parse.urljoin(
                self.endpoint_paths['books'],
                f"{book_id}/{self.endpoint_paths['export_text']}"
            )
        ).text

    def export_html(self, book_id):
        return self._session.get(
            urllib.parse.urljoin(
                self.endpoint_paths['books'],
                f"{book_id}/{self.endpoint_paths['export_html']}"
            )
        ).text              
        

class BaseURLSession(requests.Session):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def get(self, url_path, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url_path)
        return super().get(url, *args, **kwargs)


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
        r.headers[self.header_key] = f'Token {self.token_id}:{self.token_secret}'

        return r