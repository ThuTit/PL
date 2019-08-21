import time

import requests
from es_updater.decorators import catalog_updater
from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository
from settings import ES_UPDATER_MODE, PL_URL_TEST

es_repository = EsProductRepository()
es_client = es_repository.es
url_pl = PL_URL_TEST + 'api/search/'
url_detail = PL_URL_TEST + 'api/products/'

@catalog_updater
def update_catalog(product):
    return product


def call_api_search(result, sku):
    data = {
        'channel': 'pv_showroom',
        'terminal': 'CP00',
        'isBundle': result,
        'q': sku,
        '_page': 1,
        '_limit': 1000
    }
    response = requests.get(url=url_pl, params=data)
    return response.json()
def call_api_detail(sku):
    data = {
        'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'
    }
    response = requests.get(url=url_detail + sku, params=data)
    return response.json()


class TestPL88():
    ISSUE_KEY = 'PL-88'

    def test_isBundle_is_True(self):
        '''
        Kiểm tra api search với trường isBundle = True

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search với isBundle = True
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1, channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(1)
        response = call_api_search(True, None)
        sku = list()
        for i in range(len(response['result']['products'])):
            sku.append(response['result']['products'][i]['sku'])
        assert res['_source']['sku'] in sku
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_isBundle_is_False(self):
        '''
        Kiểm tra api search với trường isBundle = False

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search với isBundle = False
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=0, channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(1)
        response = call_api_search(False, None)
        sku = list()
        for i in range(len(response['result']['products'])):
            sku.append(response['result']['products'][i]['sku'])
        assert res['_source']['sku'] in sku
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_isBundle_is_something(self):
        '''
        Kiểm tra api search với trường isBundle khác True, False

        Step by step:
        - Gọi api search với isBundle khác True, False
        - Kiểm tra kết quả trả về -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        response = call_api_search('something', None)
        assert response['code'] == 'BAD_REQUEST'

    def test_isBundle_is_True_and_search_sku(self):
        '''
        Kiểm tra api search với trường isBundle = True và search keyword = sku

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search với isBundle = True và search keyword = sku
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1, channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(1)
        response = call_api_search(True, product_catalog['sku'])
        sku = list()
        for i in range(len(response['result']['products'])):
            sku.append(response['result']['products'][i]['sku'])
        assert res['_source']['sku'] in sku
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_isBundle_True_is_parent_detail(self):
        '''
        Kiểm tra api detail khi sản phẩm là bundle và là bundle cha

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1)
        del product_catalog['bundle_products']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(0.5)
        response = call_api_detail(product_catalog['sku'])
        assert response['result']['product']['isBundle'] == True
        assert response['result']['product']['parentBundles'] != None
        assert response['result']['product']['bundleProducts'] == None
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])
    def test_isBundle_True_is_product_detail(self):
        '''
        Kiểm tra api detail khi sản phẩm là bundle và là sản phẩm con

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1)
        del product_catalog['parent_bundles']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(0.5)
        response = call_api_detail(product_catalog['sku'])
        assert response['result']['product']['isBundle'] == True
        assert response['result']['product']['parentBundles'] == None
        assert response['result']['product']['bundleProducts'] != None
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])
    def test_isBundle_True_is_sample_detail(self):
        '''
        Kiểm tra api detail khi sản phẩm là bundle

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1)
        del product_catalog['parent_bundles']
        del product_catalog['bundle_products']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(0.5)
        response = call_api_detail(product_catalog['sku'])
        assert response['result']['product']['isBundle'] == True
        assert response['result']['product']['parentBundles'] == None
        assert response['result']['product']['bundleProducts'] == None
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])
    def test_isBundle_True_is_not_bundle_detail(self):
        '''
        Kiểm tra api detail khi sản phẩm không là bundle

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api detail
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product()
        del product_catalog['parent_bundles']
        del product_catalog['bundle_products']
        del product_catalog['is_bundle']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(0.5)
        print(product_catalog['sku'])
        response = call_api_detail(product_catalog['sku'])
        assert response['result']['product']['isBundle'] == None
        assert response['result']['product']['parentBundles'] == None
        assert response['result']['product']['bundleProducts'] == None
        # es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    # /rrgfdg
    def test_isBundle_True_is_parent_search(self):
        '''
        Kiểm tra api search khi sản phẩm là bundle và là bundle cha

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1, channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        del product_catalog['bundle_products']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(1)
        response = call_api_search(True, product_catalog['sku'])
        assert response['result']['products'][0]['isBundle'] == True
        assert response['result']['products'][0]['parentBundles'] != None
        assert response['result']['products'][0]['bundleProducts'] == None
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])
    def test_isBundle_True_is_product_search(self):
        '''
        Kiểm tra api search khi sản phẩm là bundle và là sản phẩm con

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1, channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        del product_catalog['parent_bundles']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(1)
        response = call_api_search(True, product_catalog['sku'])
        assert response['result']['products'][0]['isBundle'] == True
        assert response['result']['products'][0]['parentBundles'] == None
        assert response['result']['products'][0]['bundleProducts'] != None
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])
    def test_isBundle_True_is_sample_search(self):
        '''
        Kiểm tra api search khi sản phẩm là bundle

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=1, channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        del product_catalog['parent_bundles']
        del product_catalog['bundle_products']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(1)
        response = call_api_search(True, product_catalog['sku'])
        assert response['result']['products'][0]['isBundle'] == True
        assert response['result']['products'][0]['parentBundles'] == None
        assert response['result']['products'][0]['bundleProducts'] == None
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])
    def test_isBundle_True_is_not_bundle_search(self):
        '''
        Kiểm tra api search khi sản phẩm không là bundle

        Step by step:
        - Insert dữ liệu vào ES
        - Gọi api search
        - Kiểm tra kết quả trả về -> Expect: Hiển thị dữ liệu đã insert ES
        :return:
        '''
        product_catalog = fake.catalog_product(channels=[{'code': 'pv_showroom',
                                                                       'name': 'Showroom Phong Vũ',
                                                                       'id': 1}])
        del product_catalog['parent_bundles']
        del product_catalog['bundle_products']
        del product_catalog['is_bundle']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        time.sleep(0.5)
        print(product_catalog['sku'])
        response = call_api_search(False, product_catalog['sku'])
        assert response['result']['products'] == []
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])


