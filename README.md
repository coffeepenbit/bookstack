# bookstack
*version: 0.1.0-alpha.2*

**Please note that this project is currently in an unstable state. Please be patient.**

A Python wrapper for [BookStack's](https://www.bookstackapp.com) API

# Installation
To install `bookstack`, run:

`pip install bookstack`

# Setup
To use BookStack's API, you'll need to get a token ID and secret.

You can find how to get these values from your BookStack instance's doc page at `http[s]://<example.com>/api/docs`

# Usage
Once you've acquired your token ID and secret, you're ready to rock.

```python
import bookstack

# Input the appropriate values for these three variables
base_url = 'http[s]://<example.com>'
token_id = '<token_id>'
token_secret = '<token_secret>'

api = bookstack.BookStack(base_url, token_id=token_id, token_secret=token_secret)
```