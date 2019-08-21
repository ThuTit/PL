import pytest
import requests
from es_updater.decorators import srm_updater
from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository
from settings import ES_UPDATER_MODE, PL_URL_TEST

es_repository = EsProductRepository()
es_client = es_repository.es

url_detail = PL_URL_TEST + 'api/products/'

@srm_updater
def update_srm(product):
    return product

def call_api_detail(sku, data):
    response = requests.get(url=url_detail + sku, params=data)
    return response.json()

class TestPL125():
    ISSUE_KEY = 'PL-125'
    def test_get_sale_point_success(self):
        '''
        Kiểm tra response của api detail khi trường sale_point là số nguyên

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về đúng giá trị trường sale_point
        :return:
        '''
        product_srm = fake.srm_product(sale_point=10)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        data = {'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n' }
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] == res['_source']['sale_point'] == 10
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_null(self):
        '''
        Kiểm tra response của api detail khi trường sale_point null

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về giá trị mặc định trường sale_point = 0
        :return:
        '''
        product_srm = fake.srm_product(sale_point=None)
        update_srm(product_srm)
        data = {'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'}
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] == 0
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_am(self):
        '''
        Kiểm tra response của api detail khi trường sale_point < 0

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về đúng giá trị trường sale_point
        :return:
        '''
        product_srm = fake.srm_product(sale_point=-1)
        update_srm(product_srm)
        data = {'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'}
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] == res['_source']['sale_point'] == -1
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_not_disable_sign(self):
        '''
        Kiểm tra response của api detail khi không có trường disable_sign

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về giá trị mặc định trường sale_point = 0
        :return:
        '''
        product_srm = fake.srm_product(sale_point=-1)
        update_srm(product_srm)
        data = {}
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] == 0
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_have_disable_sign_correct(self):
        '''
        Kiểm tra response của api detail khi có trường disable_sign đúng giá trị

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về giá trị mặc định trường sale_point = 0
        :return:
        '''
        product_srm = fake.srm_product(sale_point=10)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        data = {'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'}
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] ==res['_source']['sale_point'] == 10
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_have_disable_sign_wrong(self):
        '''
        Kiểm tra response của api detail khi có trường disable_sign sai giá trị

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về giá trị mặc định trường sale_point = 0
        :return:
        '''
        product_srm = fake.srm_product(sale_point=10)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        data = {'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5ns'}
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] ==0
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_have_disable_sign_space(self):
        '''
        Kiểm tra response của api detail khi trường disable_sign space 2 đầu

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra response
        -> Expect: Trả về giá trị đúng trường sale_point
        :return:
        '''
        product_srm = fake.srm_product(sale_point=11)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        data = {'DISABLE_SIGN': ' bG9pdGllbnByb2R1Y3RsaXN0aW5n '}
        response = call_api_detail(product_srm['sku'], data)
        assert response['result']['product']['salePoint'] == res['_source']['sale_point'] == 11
        es_client.delete(index=es_repository._index, id=product_srm['sku'])


