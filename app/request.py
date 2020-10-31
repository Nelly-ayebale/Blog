import urllib.request
import json
from .models import Quote

base_url = None

def configure_request(app):
    global base_url
    base_url = app.config['QUOTE_BASE_URL']


def get_quotes():
    '''
    Function that gets the json response to our url request
    '''
    with urllib.request.urlopen(base_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quote_results = None

        if get_quotes_response:
            quote = get_quotes_response.get('quote')
            author = get_quotes_response.get('author')

            quote_results = Quote(quote,author)
    return quote_results

