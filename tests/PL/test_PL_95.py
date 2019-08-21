import json
import humps

from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository
from es_updater.decorators import ppm_updater, catalog_updater
import requests
import time

import datetime

from settings import PL_URL_TEST, ES_UPDATER_MODE

es_repository = EsProductRepository()
es_client = es_repository.es

url_pl = PL_URL_TEST + 'api/search/'


@ppm_updater
def update_ppm(product):
    return product


@catalog_updater
def update_catalog(product):
    return product


def iterate_all(iterable, returned="key"):
    """Returns an iterator that returns all keys or values
       of a (nested) iterable.

       Arguments:
           - iterable: <list> or <dictionary>
           - returned: <string> "key" or "value"

       Returns:
           - <iterator>
    """

    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if returned == "key":
                yield key
            elif returned == "value":
                if not (isinstance(value, dict) or isinstance(value, list)):
                    yield value
            else:
                raise ValueError("'returned' keyword only accepts 'key' or 'value'.")
            for ret in iterate_all(value, returned=returned):
                yield ret
    elif isinstance(iterable, list):
        for el in iterable:
            for ret in iterate_all(el, returned=returned):
                yield ret

def rename(old_dict,old_name,new_name):
    new_dict = {}
    for key,value in zip(old_dict.keys(),old_dict.values()):
        new_key = key if key != old_name else new_name
        new_dict[new_key] = old_dict[key]
    return new_dict

def add_promotion(sku, channel, terminal, start_time, end_time):
    product = {
        'sku': sku,
        'channels': [
            {
                'code': 'pv_showroom',
                'name': 'Showroom Phong Vũ',
                'id': 1
            },
            {
                'code': 'pv_online',
                'name': 'Phong Vũ online',
                'id': 2
            },
            {
                'code': 'pv_agent',
                'name': 'Đại lý Phong Vũ',
                'id': 4
            }
        ],
        'name': 'ốp MBA11'' JCPAL Ultra-thin- J4015 (Trong suốt)',
        'categories': [
            {
                'code': '01-N002',
                'level': 1,
                'parent_id': 0,
                'name': 'Phụ Kiện Laptop',
                'id': 3
            },
            {
                'code': '01-N002-08',
                'level': 2,
                'parent_id': 3,
                'name': 'Túi đựng laptop',
                'id': 153
            },
            {
                'code': '01-N002-08-99',
                'level': 3,
                'parent_id': 153,
                'name': 'Túi Laptop Khác',
                'id': 168
            }
        ],
        'promotions': [
            {
                'channel': channel,
                'terminal': terminal,
                'definitions': [
                    {
                        'condition': {
                            'order_value_max': None,
                            'payment_methods': [
                                'all'
                            ],
                            'coupon': None,
                            'order_value_min': None
                        },
                        'partner': 'PHONGVU',
                        'apply_on': 'product',
                        'time_ranges': [],
                        'name': 'Test',
                        'started_at': start_time,
                        'description': 'abc',
                        'id': 76,
                        'type': 'product',
                        'is_default': True,
                        'benefit': {
                            'money': [
                                {
                                    'money': 100000.0,
                                    'budget_id': 0,
                                    'max_discount': None,
                                    'id': 0,
                                    'discount_type': 'money',
                                    'out_of_budget': False,
                                    'percent': None,
                                    'budget_status': 'active'
                                }
                            ],
                            'items': []
                        },
                        'ended_at': end_time
                    }
                ]
            }
        ]

    }
    es_client.create(index=es_repository._index, id=product['sku'], body=product)


def add_promotion_null(sku):
    product = {
        'sku': sku,
        'channels': [
            {
                'code': 'pv_showroom',
                'name': 'Showroom Phong Vũ',
                'id': 1
            },
            {
                'code': 'pv_online',
                'name': 'Phong Vũ online',
                'id': 2
            },
            {
                'code': 'pv_agent',
                'name': 'Đại lý Phong Vũ',
                'id': 4
            }
        ],
        'name': 'ốp MBA11'' JCPAL Ultra-thin- J4015 (Trong suốt)',
        'categories': [
            {
                'code': '01-N002',
                'level': 1,
                'parent_id': 0,
                'name': 'Phụ Kiện Laptop',
                'id': 3
            },
            {
                'code': '01-N002-08',
                'level': 2,
                'parent_id': 3,
                'name': 'Túi đựng laptop',
                'id': 153
            },
            {
                'code': '01-N002-08-99',
                'level': 3,
                'parent_id': 153,
                'name': 'Túi Laptop Khác',
                'id': 168
            }
        ],
        'promotions': []

    }
    es_client.create(index=es_repository._index, id=product['sku'], body=product)


def refresh_indices():
    es_client.indices.refresh(index=es_repository._index)


def call_api_search(sku, channel, terminal):
    data = {
        'channel': channel,
        'terminal': terminal,
        'hasPromotions': True,
        'q': sku

    }
    response = requests.get(url=url_pl, params=data)
    return response.json()


class TestPL95():
    ISSUE_KEY = 'PL-95'

    def test_product_have_promotion(self):
        '''
        Kiem tra response tra ve khi san pham co khuyen mai

        Step by step:
        - Tao du lieu theo yeu cau
        - Insert du lieu vao Elastic Search
        - Goi API search
        - Expect: Response tra ve co san pham
        :return:
        '''
        start = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        end = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        product = fake.product(
            channels=[(fake.channel(code='pv_showroom'))],
            promotions=[(fake.promotion(channel='pv_showroom', terminal='CP00',
                                        definitions=[fake.promotion_definition(started_at=start,
                                                                               ended_at=end)]
                                        ))])
        update_ppm(product)
        update_catalog(product)
        refresh_indices()
        res = es_client.get(index=es_repository._index, id=product['sku'])
        channel = 'pv_showroom'
        terminal = 'CP00'
        result = call_api_search(product['sku'], channel, terminal)
        res_camel = res['_source']['promotions'][0]
        # res_camel = {key.replace(): for key in iterate_all(res_camel, 'key') }
        print(json.dumps(res_camel))
        for i in iterate_all(res_camel, 'key'):
            j = humps.camelize(i)
            print(j)



        # print(res_camel)
        assert result['result']['products'][0]['promotions'] != []
        es_client.delete(index=es_repository._index, id=product['sku'])


    def test_product_have_not_promotion(self):
        '''
        Kiem tra response tra ve khi san pham khong co khuyen mai

        Step by step:
        - Tao du lieu theo yeu cau
        - Insert du lieu vao Elastic Search
        - Goi API search
        - Expect: Response tra ve khong co san pham
        :return:
        '''

        sku = 'test_sku'
        channel = 'pv_showroom'
        terminal = 'CP00'
        add_promotion_null(sku)
        refresh_indices()
        result = call_api_search(sku, channel, terminal)
        print(result['result']['products'][0]['promotions'])
        # assert result['result']['products'][0]['promotions'] == []
        es_client.delete(index=es_repository._index, id=sku)


    def test_product_have_promotion_apply_all_channel(self):
        '''
        Kiem tra response tra ve khi san pham co khuyen mai ap dung tat ca channel

        Step by step:
        - Tao du lieu theo yeu cau
        - Insert du lieu vao Elastic Search
        - Goi API search
        - Expect: Response tra ve co san pham ap dung tat ca channel
        :return:
        '''

        sku = 'test_sku'
        channel = 'all'
        terminal = None
        channel1 = 'pv_showroom'
        terminal1 = 'CP00'
        start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        add_promotion(sku, channel, terminal, start_time, end_time)
        refresh_indices()
        result = call_api_search(sku, channel1, terminal1)
        assert result['result']['products'][0]['promotions'] != []
        es_client.delete(index=es_repository._index, id=sku)


    def test_product_have_promotion_apply_one_channel_and_search_true(self):
        '''
        Kiem tra response tra ve khi san pham co khuyen mai ap dung 1 channel, goi api cua channel do

        Step by step:
        - Tao du lieu theo yeu cau
        - Insert du lieu vao Elastic Search
        - Goi API search
        - Expect: Response tra ve co san pham
        :return:
        '''

        sku = 'test_sku'
        channel = 'pv_showroom'
        terminal = 'CP00'
        start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        add_promotion(sku, channel, terminal, start_time, end_time)
        refresh_indices()
        result = call_api_search(sku, channel, terminal)
        assert result['result']['products'][0]['promotions'] != []
        es_client.delete(index=es_repository._index, id=sku)


    def test_product_have_promotion_apply_one_channel_and_search_fail(self):
        '''
        Kiem tra response tra ve khi san pham co khuyen mai ap dung 1 channel, goi api cua channel khac

        Step by step:
        - Tao du lieu theo yeu cau
        - Insert du lieu vao Elastic Search
        - Goi API search
        - Expect: Response tra ve khong co san pham
        :return:
        '''

        sku = 'test_sku'
        channel1 = 'pv_showroom'
        terminal1 = 'CP00'
        channel2 = 'pv_online'
        terminal2 = 'online'
        start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        add_promotion(sku, channel1, terminal1, start_time, end_time)
        refresh_indices()
        result = call_api_search(sku, channel2, terminal2)
        print(result['result']['products'])
        # assert result['result']['products']== []
        es_client.delete(index=es_repository._index, id=sku)
