import requests
from settings import PL_URL_DEV

url = PL_URL_DEV + 'api/search/'
class TestPL106():
    ISSUE_KEY = 'DP-20'
    def test_responses_are_products(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'q': 'laptop',
            'responses': 'products'
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['products'])):
            assert result['result']['products'][i] != []
            assert result['result']['filters'] == []
            assert result['result']['keywords'] == []


    def test_responses_are_products_space_start_end(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'q': 'laptop',
            'responses': ' products '
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['products'])):
            assert result['result']['products'][i] != []
            assert result['result']['filters'] == []
            assert result['result']['keywords'] == []

    def test_responses_are_filters(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'price_gte': 0,
            'price_lte': 100000000,
            'filters': 'brands',
            'responses': 'filters'
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['filters'])):
            assert result['result']['products']== []
            assert result['result']['filters'][i] != []
            assert result['result']['keywords'] == []

    def test_responses_are_filters_space_start_end(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'q': 'laptop',
            'filters': 'brands',
            'responses': ' filters '
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['filters'])):
            assert result['result']['products'] == []
            assert result['result']['filters'][i] != []
            assert result['result']['keywords'] == []
    def test_responses_are_keywords(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'q': 'laptop',
            'responses': 'keywords'
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['keywords'])):
            assert result['result']['products']== []
            assert result['result']['filters'] == []
            assert result['result']['keywords'][i] != []

    def test_responses_are_keywords_space_start_end(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'q': 'laptop',
            'responses': ' keywords '
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['keywords'])):
            assert result['result']['products'] == []
            assert result['result']['filters'] == []
            assert result['result']['keywords'][i] != []

    def test_responses_null(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'responses': None
        }
        request = requests.get(url, params=data)
        result = request.json()
        for i in range(len(result['result']['products'])):
            assert result['result']['products'][i]!= []
