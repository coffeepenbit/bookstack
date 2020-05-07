import pytest

import bookstack


@pytest.mark.vcr()
def test_readme_example(fixture_bookstack):
    assert 'get_books_export_pdf' in fixture_bookstack.available_api_methods
    assert 'Computers' == fixture_bookstack.get_books_list()['data'][0]['name']