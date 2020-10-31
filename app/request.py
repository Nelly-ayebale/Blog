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
            quote_results_list = get_quotes_response
            quote_results = process_results(quote_results_list)
    return quote_results

def process_results(quote_list):
    '''
    Function that processes the quotes' results and transforms them to a list of objects
    '''
    quote_results = []
    for quote_item in quote_list:
        quote = quote_item.get('quote')
        author = quote_item.get('author')

        quote_object = Quote(quote,author)
        quote_results.append(quote_object)
    return quote_results