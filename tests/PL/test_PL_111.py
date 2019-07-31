from settings import PL_URL_TEST, PL_URL_DEV
import requests


url = PL_URL_DEV + 'api/search/'
url_ppm = PL_URL_DEV + 'api/ppm/search'
url_detail = PL_URL_DEV + 'api/products/1703075'


class TestPL111():
    ISSUE_KEY = 'PL-88'

    def test_api_search_truyen_dung_param(self):
        '''
        Test API Search truyền đúng param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n',
            'q': '1806180'
        }
        response = requests.get(url, params=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['products'][0]['stocks'] != []
        for i in range(len(result['result']['products'][0]['stocks'])):
            total_stocks +=result['result']['products'][0]['stocks'][i]['available']
        assert result['result']['products'][0]['totalAvailable'] == total_stocks

    def test_api_search_truyen_dung_param_chua_space_dau_cuoi(self):
        '''
        Test API Search truyền đúng param DISABLE_SIGN chứa space đầu cuối
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'DISABLE_SIGN': ' bG9pdGllbnByb2R1Y3RsaXN0aW5n ',
            'q': '1806180'
        }
        response = requests.get(url, params=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['products'][0]['stocks'] != []
        for i in range(len(result['result']['products'][0]['stocks'])):
            total_stocks += result['result']['products'][0]['stocks'][i]['available']
        assert result['result']['products'][0]['totalAvailable'] == total_stocks

    def test_api_search_truyen_sai_param(self):
        '''
        Test API Search truyền sai param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'DISABLE_SIGN': 'ebG9pdGllbnByb2R1Y3RsaXN0aW5n',
            'q': '1806180'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['result']['products'][0]['stocks'] == []
        assert result['result']['products'][0]['totalAvailable'] != None

    def test_api_search_khong_truyen_param(self):
        '''
        Test API Search không truyền param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'q': '1806180'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['result']['products'][0]['stocks'] == []
        assert result['result']['products'][0]['totalAvailable'] != None

    def test_api_products_truyen_dung_param(self):
        '''
        Test API Products truyền đúng param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'skus': '1703075',
            'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'
        }
        response = requests.get(url, params=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['products'][0]['stocks'] != []
        for i in range(len(result['result']['products'][0]['stocks'])):
            total_stocks +=result['result']['products'][0]['stocks'][i]['available']
        assert result['result']['products'][0]['totalAvailable'] == total_stocks

    def test_api_products_truyen_dung_param_chua_space_dau_cuoi(self):
        '''
        Test API Products truyền đúng param DISABLE_SIGN chứa space đầu cuối
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'skus': '1703075',
            'DISABLE_SIGN': ' bG9pdGllbnByb2R1Y3RsaXN0aW5n '
        }
        response = requests.get(url, params=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['products'][0]['stocks'] != []
        for i in range(len(result['result']['products'][0]['stocks'])):
            total_stocks += result['result']['products'][0]['stocks'][i]['available']
        assert result['result']['products'][0]['totalAvailable'] == total_stocks

    def test_api_products_truyen_sai_param(self):
        '''
        Test API Products truyền sai param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'skus': '1703075',
            'DISABLE_SIGN': 'ebG9pdGllbnByb2R1Y3RsaXN0aW5n'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['result']['products'][0]['stocks'] == []
        assert result['result']['products'][0]['totalAvailable'] != None

    def test_api_products_khong_truyen_param(self):
        '''
        Test API Products không truyền param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'skus': '1703075'
        }
        response = requests.get(url, params=data)
        result = response.json()
        assert result['result']['products'][0]['stocks'] == []
        assert result['result']['products'][0]['totalAvailable'] != None

    def test_api_Detail_truyen_dung_param(self):
        '''
        Test API Detail truyền đúng param DISABLE_SIGN
        '''
        data = {

            'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'
        }
        response = requests.get(url_detail, params=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['product']['stocks'] != []
        for i in range(len(result['result']['product']['stocks'])):
            total_stocks += result['result']['product']['stocks'][i]['available']
        assert result['result']['product']['totalAvailable'] == total_stocks

    def test_api_Detail_truyen_dung_param_chua_space_dau_cuoi(self):
        '''
        Test API Detail truyền đúng param DISABLE_SIGN chứa space đầu cuối
        '''
        data = {

            'DISABLE_SIGN': ' bG9pdGllbnByb2R1Y3RsaXN0aW5n '
        }
        response = requests.get(url_detail, params=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['product']['stocks'] != []
        for i in range(len(result['result']['product']['stocks'])):
            total_stocks += result['result']['product']['stocks'][i]['available']
        assert result['result']['product']['totalAvailable'] == total_stocks

    def test_api_Detail_truyen_sai_param(self):
        '''
        Test API Detail truyền sai param DISABLE_SIGN
        '''
        data = {

            'DISABLE_SIGN': 'ebG9pdGllbnByb2R1Y3RsaXN0aW5n'
        }
        response = requests.get(url_detail, params=data)
        result = response.json()
        assert result['result']['product']['stocks'] == []
        assert result['result']['product']['totalAvailable'] != None

    def test_api_Detail_khong_truyen_param(self):
        '''
        Test API Detail không truyền param DISABLE_SIGN
        '''
        data = {}
        response = requests.get(url_detail, params=data)
        result = response.json()
        assert result['result']['product']['stocks'] == []
        assert result['result']['product']['totalAvailable'] != None

    def test_api_Check_ton_truyen_dung_param(self):
        '''
        Test API Check tồn truyền đúng param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n',
            'q': '1703075'
        }
        response = requests.post(url_ppm, json=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['products'][0]['stocks'] != []
        for i in range(len(result['result']['products'][0]['stocks'])):
            total_stocks += result['result']['products'][0]['stocks'][i]['available']
        assert result['result']['products'][0]['totalAvailable'] == total_stocks

    def test_api_Check_ton_truyen_dung_param_chua_space_dau_cuoi(self):
        '''
        Test API Check tồn truyền đúng param DISABLE_SIGN chứa space đầu cuối
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'DISABLE_SIGN': ' bG9pdGllbnByb2R1Y3RsaXN0aW5n ',
            'q': '1703075'
        }
        response = requests.post(url_ppm, json=data)
        result = response.json()
        total_stocks = 0
        assert result['result']['products'][0]['stocks'] != []
        for i in range(len(result['result']['products'][0]['stocks'])):
            total_stocks += result['result']['products'][0]['stocks'][i]['available']
        assert result['result']['products'][0]['totalAvailable'] == total_stocks

    def test_api_Check_ton_truyen_sai_param(self):
        '''
        Test API Check tồn truyền sai param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'DISABLE_SIGN': 'ebG9pdGllbnByb2R1Y3RsaXN0aW5n',
            'q': '1703075'
        }
        response = requests.post(url_ppm, json=data)
        result = response.json()
        assert result['result']['products'][0]['stocks'] == []
        assert result['result']['products'][0]['totalAvailable'] != None

    def test_api_Check_ton_khong_truyen_param(self):
        '''
        Test API Check tồn không truyền param DISABLE_SIGN
        '''
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '123',
            'q': '1703075'
        }
        response = requests.post(url_ppm, json=data)
        result = response.json()
        assert result['result']['products'][0]['stocks'] == []
        assert result['result']['products'][0]['totalAvailable'] != None