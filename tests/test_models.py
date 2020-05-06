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

    # @staticmethod
    # @pytest.mark.vcr()
    # def test_get_docs(fixture_bookstack):
    #     test_result = fixture_bookstack._get_docs()

    #     assert test_result
    #     assert isinstance(test_result, dict)
    #     assert all(key in test_result.keys() for key in ['docs'])        

    @staticmethod
    # @pytest.mark.vcr()
    def test_api(fixture_bookstack):
        test_result = fixture_bookstack._api

        assert isinstance(test_result, bookstack.models.API)

    @staticmethod
    def test_methods(fixture_bookstack):
        test_result = fixture_bookstack.methods()

        assert 'books_export_plain_text' in test_result
        assert '_create_methods' not in test_result

    @staticmethod
    def test_reset_api(fixture_bookstack):
        raise NotImplementedError

    @staticmethod
    @pytest.mark.vcr()
    def test_get_books(fixture_bookstack):
        test_result = fixture_bookstack.get_books()

        assert test_result
        assert isinstance(test_result, dict)
        assert all(key in test_result.keys() for key in ['data', 'total'])

    @staticmethod
    @pytest.mark.vcr()
    def test_read_book(fixture_bookstack):
        test_result = fixture_bookstack.read_book(1)

        assert test_result
        assert isinstance(test_result, dict)
        assert all(key in test_result.keys() 
                   for key in ['id', 'name','slug'])   

    @staticmethod
    @pytest.mark.vcr()
    def test_export_text(fixture_bookstack):
        test_result = fixture_bookstack.export_text(1)

        assert test_result
        assert isinstance(test_result, str)

    @staticmethod
    @pytest.mark.vcr()
    def test_export_html(fixture_bookstack):
        test_result = fixture_bookstack.export_html(1)

        assert test_result
        assert isinstance(test_result, str)


class TestAPI:
    @staticmethod
    def test_intiialize_empty():
        with pytest.raises(TypeError):
            bookstack.models.API() # pylint: disable=no-value-for-parameter
    
    @staticmethod
    def test_initialize(api_info):
        test_result = bookstack.models.API(api_info)

        assert test_result

