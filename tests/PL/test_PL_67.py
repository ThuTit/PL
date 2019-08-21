from settings import PL_URL_UAT
import requests
import pytest


from support.Excel2Data import create_data_test

url = PL_URL_UAT + 'api/search/'


class TestPL67():
    ISSUE_KEY = 'PL-88'
    _data = create_data_test()
    @pytest.mark.parametrize('data, expect', _data)
    def test_search_synonym(self, data, expect):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'q': ''+ data
        }
        print(data)
        response = requests.get(url, data)
        result = response.json()
        print(result)
        # print(type(result['result']['products'][0]['name']))
        print(result['result']['products'][0]['name'].lower())
        for i in range(len(result['result']['products'])):
            assert expect.lower() in result['result']['products'][i]['name'].lower()
