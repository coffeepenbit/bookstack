# bookstack
A Python wrapper for [BookStack's](https://www.bookstackapp.com) API

# Installation
To install `bookstack`, run:

`pip install bookstack`

# Setup
To use BookStack's API, you'll need to get a token ID and secret.

You can find how to get these values from your BookStack instance's doc page at `http[s]://<example.com>/api/docs`

**Note**: Your account's user group must have API usage priveleges enabled.

# Usage
Once you've acquired your token ID and secret, you're ready to rock.

```python
>>> import bookstack

# Input the appropriate values for these three variables
>>> base_url = 'http[s]://<example.com>'
>>> token_id = '<token_id>'
>>> token_secret = '<token_secret>'

>>> api = bookstack.BookStack(base_url, token_id=token_id, token_secret=token_secret)
```

This wrapper *dynamically* generates its API calls at runtime. To have the wrapper generate the methods, use:

```python
>>> api.generate_api_methods()

>>> api.available_api_methods
{'get_books_export_pdf', 'get_shelves_list', 'post_books_create', 'get_docs_display', 'delete_shelves_delete', 'get_books_list', 'get_docs_json', 'delete_books_delete', 'get_books_read', 'get_shelves_read', 'put_books_update', 'get_books_export_plain_text', 'get_books_export_html', 'post_shelves_create', ...}
```

The above are then the methods available to you, for example:

```python
>>> books_list = api.get_books_list()
>>> books_list['data'][0]['name']
'Mathematics'
```
