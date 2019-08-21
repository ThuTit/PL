from settings import PL_URL_TEST
import requests
url = PL_URL_TEST + 'api/search/'

class TestFiltersBlock():
    ISSUE_KEY = 'PL-107'
    def test_filters_null(self):
        '''
        Trường filters = null 123

        Tạo data có trường filters = null 123

        Step by step:
        - Tạo data có trường filters = null
        - Gửi request
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': None
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['result']['filters'] == []

    def test_filters_empty(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': ''
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'BAD_REQUEST'

    def test_filters_have_space(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': ' attributeSets '
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'attributeSets'

    def test_not_have_param_filters(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'] == []
    def test_filters_are_attributeSets(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'attributeSets'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'attributeSets'
    def test_filters_are_attributes(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'attributes'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        for i in range(len(result['result']['filters'])):
            assert 'attributes' in str(result['result']['filters'][i]['code'])

    def test_filters_are_brands(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'brands'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'brands'
    def test_filters_are_attributeSets_and_attributes(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'attributeSets,attributes'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'attributeSets'
        for i in range(1, len(result['result']['filters'])):
            assert 'attributes' in str(result['result']['filters'][i]['code'])
    def test_filters_are_attributeSets_and_brands(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'attributeSets,brands'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'brands'
        assert result['result']['filters'][1]['code'] == 'attributeSets'
    def test_filters_are_brands_and_attributes(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'brands,attributes'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'brands'
        for i in range(1, len(result['result']['filters'])):
            assert 'attributes' in str(result['result']['filters'][i]['code'])

    def test_filters_are_attributeSets_brands_and_attributes(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'attributeSets,brands,attributes'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'brands'
        assert result['result']['filters'][1]['code'] == 'attributeSets'
        for i in range(2, len(result['result']['filters'])):
            assert 'attributes' in str(result['result']['filters'][i]['code'])

    def test_filters_are_attributeSets_brands_attributes_and_space(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'attributeSets, brands, attributes'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'
        assert result['result']['filters'][0]['code'] == 'brands'
        assert result['result']['filters'][1]['code'] == 'attributeSets'
        for i in range(2, len(result['result']['filters'])):
            assert 'attributes' in str(result['result']['filters'][i]['code'])

    def test_filters_are_not_attributeSets_brands_and_attributes(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'filters': 'abc'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'BAD_REQUEST'

    def test_responses_are_filters(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            'responses': 'filters'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['code'] == 'SUCCESS'