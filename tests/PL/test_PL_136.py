import json

import pytest
import time
import requests
from es_updater.decorators import ppm_updater, catalog_updater
from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository
from settings import ES_UPDATER_MODE, PL_URL_TEST

url_pl = PL_URL_TEST + 'api/search/'
url_detail = PL_URL_TEST + 'api/products/'
es_repository = EsProductRepository()
es_client = es_repository.es


@ppm_updater
def update_ppm(product):
    return product


@catalog_updater
def update_catalog(product):
    return product


def call_api_search(sku):
    data = {
        'channel': 'pv_online',
        'terminal': 'online',
        'q': sku

    }
    response = requests.get(url=url_pl, params=data)
    return response.json()


def call_api_detail(sku):
    data = {
        'DISABLE_SIGN':'bG9pdGllbnByb2R1Y3RsaXN0aW5n'
    }
    response = requests.get(url=url_detail + sku)
    return response.json()


class TestPL136():
    ISSUE_KEY = 'PL-136'
    def test_response_api_search_when_all_fields_valid(self):
        '''
        Kiểm tra response của api search khi giá trị các trường hợp lệ

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API search
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_online')],
            promotions=[(fake.promotion(channel='pv_online', terminal='online'))]
        )
        update_ppm(product)
        update_catalog(product)
        res = es_client.get(index=es_repository._index, id=product['sku'])
        time.sleep(1)
        result = call_api_search(product['sku'])
        # print(product['sku'])
        # print(result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'])
        # print(res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'])
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['outOfBudget'] == \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['out_of_budget']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['maxQuantity'] == \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['max_quantity']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'budgetStatus'] == res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'budget_status']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'appliedPromotion'] == res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'applied_promotion']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity'] == \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity']
        es_client.delete(index=es_repository._index, id=product['sku'])

    def test_response_api_search_when_apply_all(self):
        '''
        Kiểm tra response của api search khi coupon áp dụng cho toàn quốc

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API search
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_online')],
            promotions=[(fake.promotion(channel='all', terminal=None))]
        )
        update_ppm(product)
        update_catalog(product)
        res = es_client.get(index=es_repository._index, id=product['sku'])
        time.sleep(1)
        result = call_api_search(product['sku'])
        # print(result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'])
        # print(res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'])
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['outOfBudget'] == \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['out_of_budget']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['maxQuantity'] == \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['max_quantity']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'budgetStatus'] == res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'budget_status']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'appliedPromotion'] == res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'][
                   'applied_promotion']
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity'] == \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity']
        # print(product['sku'])
        es_client.delete(index=es_repository._index, id=product['sku'])

    def test_response_api_search_when_different_channel(self):
        '''
        Kiểm tra response của api search khi coupon áp dụng cho toàn quốc nhưng khác kênh bán

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API search
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_showroom')],
            promotions=[(fake.promotion(channel='all', terminal=None))]
        )
        print(json.dumps(product))
        update_ppm(product)
        update_catalog(product)
        time.sleep(1)
        result = call_api_search(product['sku'])
        assert result['result']['products'] == []
        es_client.delete(index=es_repository._index, id=product['sku'])

    def test_response_api_search_when_coupon_null(self):
        '''
        Kiểm tra response của api search khi coupon null

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API search
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_online')],
            promotions=[(fake.promotion(channel='all', terminal=None, definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=None
                ))
                ))])
            )]
        )
        update_ppm(product)
        update_catalog(product)
        res = es_client.get(index=es_repository._index, id=product['sku'])
        time.sleep(1)
        result = call_api_search(product['sku'])
        # print(result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'])
        # print(res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'])
        # print(product['sku'])
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']== \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'] == None
        es_client.delete(index=es_repository._index, id=product['sku'])

    def test_response_api_search_when_applied_promotion_null(self):
        '''
        Kiểm tra response của api search khi applied_promotion null

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API search
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_online')],
            promotions=[(fake.promotion(channel='pv_online', terminal='online', definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(applied_promotion=None)
                ))
                ))])
            )]
        )
        update_ppm(product)
        update_catalog(product)
        res = es_client.get(index=es_repository._index, id=product['sku'])
        time.sleep(1)
        result = call_api_search(product['sku'])
        # print(result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'])
        # print(res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'])
        # print(product['sku'])
        assert result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['appliedPromotion']== \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'] == None
        es_client.delete(index=es_repository._index, id=product['sku'])

    def test_response_api_detail_when_coupon_null(self):
        '''
        Kiểm tra response của api detail khi coupon null

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API detail
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_online')],
            promotions=[(fake.promotion(channel='all', terminal=None, definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=None
                ))
                ))])
            )]
        )
        update_ppm(product)
        update_catalog(product)
        res = es_client.get(index=es_repository._index, id=product['sku'])
        time.sleep(1)
        result = call_api_detail(product['sku'])
        # print(result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon'])
        # print(res['_source']['promotion']['definitions'][0]['benefit']['coupon'])
        # print(product['sku'])
        assert result['result']['product']['promotions'][0]['definitions'][0]['benefit']['coupon']== \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'] == None
        es_client.delete(index=es_repository._index, id=product['sku'])

    def test_response_api_detail_when_applied_promotion_null(self):
        '''
        Kiểm tra response của api detail khi applied_promotion null

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi API detail
        - Kiểm tra response trả về
        -> Expect: Hiển thị giá trị của khối definitions.benefit.coupon giống trong ES
        :return:
        '''
        product = fake.product(
            channels=[fake.channel(code='pv_online')],
            promotions=[(fake.promotion(channel='pv_online', terminal='online', definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(applied_promotion=None)
                ))
                ))])
            )]
        )
        update_ppm(product)
        update_catalog(product)
        res = es_client.get(index=es_repository._index, id=product['sku'])
        time.sleep(1)
        result = call_api_detail(product['sku'])
        # print(result['result']['products'][0]['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'])
        # print(res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'])
        # print(product['sku'])
        assert result['result']['product']['promotions'][0]['definitions'][0]['benefit']['coupon']['appliedPromotion']== \
               res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'] == None
        es_client.delete(index=es_repository._index, id=product['sku'])
