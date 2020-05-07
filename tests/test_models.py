import pytest

import bookstack


# TODO
# Tests will not work when you run them. This is why.
#
# Fixtures are defined in conftest.py; however, conftest.py is currently
# listed in .gitignore. Therefore, it will be unavailable until
# I redact sensitive information from the VCR.py casettes.


class TestBookStack:
    @staticmethod
    def test_intiialize_empty():
        with pytest.raises(TypeError):
            bookstack.BookStack() # pylint: disable=no-value-for-parameter

    @staticmethod
    @pytest.mark.parametrize(
        "base_url, token_id, token_secret", [
            (
                'https://example.com',
                'abc123',
                'def456'
            )
        ]
    )
    def test_intiialize(base_url, token_id, token_secret):
        kwargs = {
            'base_url': base_url, 
            'token_id': token_id, 
            'token_secret': token_secret
        }

        test_result = bookstack.BookStack(**kwargs)

        assert base_url in test_result.api_base_url
        assert token_id == token_id
        assert token_secret == token_secret

    @staticmethod
    def test_generate_api_methods(fixture_bookstack, fixture_api_info):
        fixture_bookstack.generate_api_methods()

        assert 'get_books_list' in fixture_bookstack.available_api_methods
        assert 'get_books_list' in dir(fixture_bookstack)

    @staticmethod
    @pytest.mark.vcr()
    def test_get_docs_json(fixture_bookstack):
        test_result = fixture_bookstack.get_docs_json()

        assert test_result
        assert isinstance(test_result, dict)
        assert all(key in test_result.keys() for key in ['docs'])        

    @staticmethod
    def test_available_api_methods(fixture_bookstack):
        test_result = fixture_bookstack.available_api_methods

        assert 'get_books_export_plain_text' in test_result
        assert '_create_methods' not in test_result

    @staticmethod
    @pytest.mark.vcr()
    def test_get_books_list(fixture_bookstack):
        test_result = fixture_bookstack.get_books_list()

        assert test_result
        assert isinstance(test_result, dict)
        assert all(key in test_result.keys() for key in ['data', 'total'])

    @staticmethod
    @pytest.mark.vcr()
    def test_get_books_read(fixture_bookstack):
        test_result = fixture_bookstack.get_books_read(id=2)

        assert test_result
        assert isinstance(test_result, dict)
        assert all(key in test_result.keys() 
                   for key in ['id', 'name','slug'])   

    @staticmethod
    @pytest.mark.vcr()
    def test_get_books_export_plain_text(fixture_bookstack):
        test_result = fixture_bookstack.get_books_export_plain_text(id=2)

        assert test_result
        assert isinstance(test_result, str)

    @staticmethod
    @pytest.mark.vcr()
    def test_get_books_export_html(fixture_bookstack):
        test_result = fixture_bookstack.get_books_export_html(id=2)

        assert test_result
        assert isinstance(test_result, str)
