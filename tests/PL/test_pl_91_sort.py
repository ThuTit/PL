from settings import PL_URL_DEV

import requests

url = PL_URL_DEV + 'api/search/'
url_ppm = PL_URL_DEV + 'api/ppm/search'


class TestSort():
    ISSUE_KEY = 'PL-53'

    def test_sort_name_asc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'name',
            '_order': 'asc'
        }
        response = requests.get(url, data)
        _json = response.json()
        name = list()
        name_sorted = list()
        for i in range(len(_json['result']['products'])):
            name.append(_json['result']['products'][i]['name'])
            name_sorted.append(_json['result']['products'][i]['name'])
        name.sort()
        # print(name)
        # print(name_sorted)
        for j in range(len(name)):
            if name[j] == name_sorted[j]:
                assert True
            else:
                assert False

    def test_sort_name_desc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'name',
            '_order': 'desc'
        }
        response = requests.get(url, data)

        _json = response.json()
        name = list()
        name_sorted = list()
        for i in range(len(_json['result']['products'])):
            name.append(_json['result']['products'][i]['name'].lower())
            name_sorted.append(_json['result']['products'][i]['name'].lower())
        name.sort(reverse=True)
        print(name)
        print(name_sorted)
        for j in range(len(name)):
            # print(name[j])
            # print(name_sorted[j])
            if name[j] == name_sorted[j]:
                assert True
            else:
                assert False

    def test_sort_sku_asc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'sku',
            '_order': 'asc',
            '_page': '1',
            '_limit': '50'
        }
        response = requests.get(url, data)
        _json = response.json()
        sku = list()
        sku_sorted = list()
        for i in range(len(_json['result']['products'])):
            sku.append(_json['result']['products'][i]['sku'])
            sku_sorted.append(_json['result']['products'][i]['sku'])
        sku.sort()
        print(sku)
        print(sku_sorted)
        for j in range(len(sku)):
            if sku[j] == sku_sorted[j]:
                assert True
            else:
                assert False

    def test_sort_sku_desc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'sku',
            '_order': 'desc',
            '_page': '1',
            '_limit': '50'
        }
        response = requests.get(url, data)
        _json = response.json()
        sku = list()
        sku_sorted = list()
        for i in range(len(_json['result']['products'])):
            sku.append(_json['result']['products'][i]['sku'])
            sku_sorted.append(_json['result']['products'][i]['sku'])
        sku.sort(reverse=True)
        print(sku)
        print(sku_sorted)
        for j in range(len(sku)):
            # print(sku[j])
            # print(sku_sorted[j])
            if sku[j] == sku_sorted[j]:
                assert True
            else:
                assert False

    def test_sort_importPrice_asc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'importPrice',
            '_order': 'asc',
            '_page': 10,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        print(_json)
        importPrice = list()
        importPrice_sorted = list()
        for i in range(len(_json['result']['products'])):
            importPrice.append(_json['result']['products'][i]['importPrice'])
            importPrice_sorted.append(_json['result']['products'][i]['importPrice'])
        importPrice.sort()
        print(importPrice)
        print(importPrice_sorted)
        for j in range(len(importPrice)):
            if importPrice[j] == importPrice_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(importPrice[j])
                print(_json['result']['products'][len(importPrice) - j]['sku'])
                print(importPrice_sorted[j])
                assert False

    def test_sort_importPrice_desc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'importPrice',
            '_order': 'desc',
            '_page': 10,
            '_limit': 1000
        }
        response = requests.post(url_ppm, json=data)

        _json = response.json()
        importPrice = list()
        importPrice_sorted = list()
        for i in range(len(_json['result']['products'])):
            importPrice.append(_json['result']['products'][i]['importPrice'])
            importPrice_sorted.append(_json['result']['products'][i]['importPrice'])
        importPrice.sort(reverse=True)
        print(importPrice)
        print(importPrice_sorted)
        for j in range(len(importPrice)):
            if importPrice[j] == importPrice_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(importPrice[j])
                print(_json['result']['products'][len(importPrice) - j]['sku'])
                print(importPrice_sorted[j])

                assert False

    def test_sort_supplierSalePrice_asc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'supplierSalePrice',
            '_order': 'asc',
            '_page': 10,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        supplierSalePrice = list()
        supplierSalePrice_sorted = list()
        for i in range(len(_json['result']['products'])):
            supplierSalePrice.append(_json['result']['products'][i]['price']['supplierSalePrice'])
            supplierSalePrice_sorted.append(_json['result']['products'][i]['price']['supplierSalePrice'])
        supplierSalePrice.sort()
        print(supplierSalePrice)
        print(supplierSalePrice_sorted)
        for j in range(len(supplierSalePrice)):
            if supplierSalePrice[j] == supplierSalePrice_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(supplierSalePrice[j])
                print(_json['result']['products'][len(supplierSalePrice) - j]['sku'])
                print(supplierSalePrice_sorted[j])
                assert False

    def test_sort_supplierSalePrice_desc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'supplierSalePrice',
            '_order': 'desc',
            '_page': 10,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        supplierSalePrice = list()
        supplierSalePrice_sorted = list()
        for i in range(len(_json['result']['products'])):
            supplierSalePrice.append(_json['result']['products'][i]['price']['supplierSalePrice'])
            supplierSalePrice_sorted.append(_json['result']['products'][i]['price']['supplierSalePrice'])
        supplierSalePrice.sort(reverse=True)
        print(supplierSalePrice)
        print(supplierSalePrice_sorted)
        for j in range(len(supplierSalePrice)):
            if supplierSalePrice[j] == supplierSalePrice_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(supplierSalePrice[j])
                print(_json['result']['products'][len(supplierSalePrice) - j]['sku'])
                print(supplierSalePrice_sorted[j])
                assert False

    def test_sort_sellPrice_asc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'sellPrice',
            '_order': 'asc',
            '_page': 10,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        sellPrice = list()
        sellPrice_sorted = list()
        for i in range(len(_json['result']['products'])):
            sellPrice.append(_json['result']['products'][i]['price']['sellPrice'])
            sellPrice_sorted.append(_json['result']['products'][i]['price']['sellPrice'])
        sellPrice.sort()
        print(sellPrice)
        print(sellPrice_sorted)
        for j in range(len(sellPrice)):
            if sellPrice[j] == sellPrice_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(sellPrice[j])
                print(_json['result']['products'][len(sellPrice) - j]['sku'])
                print(sellPrice_sorted[j])
                assert False

    def test_sort_sellPrice_desc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'sellPrice',
            '_order': 'desc',
            '_page': 10,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        sellPrice = list()
        sellPrice_sorted = list()
        for i in range(len(_json['result']['products'])):
            sellPrice.append(_json['result']['products'][i]['price']['sellPrice'])
            sellPrice_sorted.append(_json['result']['products'][i]['price']['sellPrice'])
        sellPrice.sort(reverse=True)
        print(sellPrice)
        print(sellPrice_sorted)
        for j in range(len(sellPrice)):
            if sellPrice[j] == sellPrice_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(sellPrice[j])
                print(_json['result']['products'][len(sellPrice) - j]['sku'])
                print(sellPrice_sorted[j])
                assert False

    def test_sort_stocks_asc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'stocks',
            '_order': 'asc',
            '_page': 1,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        stocks = list()
        stocks_sorted = list()

        test = list()

        for i in range(len(_json['result']['products'])):
            sum_stocks = list()
            sum_element = 0
            for k in range(len(_json['result']['products'][i]['stocks'])):
                sum = _json['result']['products'][i]['stocks'][k]['available']
                sum_element += sum
            sum_stocks.append(sum_element)
            stocks.append(sum_element)
            stocks_sorted.append(sum_element)
        stocks.sort()
        print(stocks)
        print(stocks_sorted)
        for j in range(len(stocks)):
            if stocks[j] == stocks_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(stocks[j])
                print(_json['result']['products'][len(stocks) - j]['sku'])
                print(stocks_sorted[j])
                assert False


    def test_sort_stocks_desc(self):
        data = {
            'channel': 'pv_online',
            'terminal': 'online',
            'visitorId': '111',
            '_sort': 'stocks',
            '_order': 'desc',
            '_page': 1,
            '_limit': 1000

        }
        response = requests.post(url_ppm, json=data)
        _json = response.json()
        stocks = list()
        stocks_sorted = list()

        test = list()

        for i in range(len(_json['result']['products'])):
            sum_stocks = list()
            sum_element = 0
            for k in range(len(_json['result']['products'][i]['stocks'])):
                sum = _json['result']['products'][i]['stocks'][k]['available']
                sum_element += sum
            sum_stocks.append(sum_element)
            stocks.append(sum_element)
            stocks_sorted.append(sum_element)
        stocks.sort(reverse=True)
        print(stocks)
        print(stocks_sorted)
        for j in range(len(stocks)):
            if stocks[j] == stocks_sorted[j]:
                assert True
            else:
                print(_json['result']['products'][j]['sku'])
                print(stocks[j])
                print(_json['result']['products'][len(stocks) - j]['sku'])
                print(stocks_sorted[j])
                assert False
