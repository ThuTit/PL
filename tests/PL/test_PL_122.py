import requests
import time

from es_updater.repository.es_product import EsProductRepository
from requests.auth import HTTPBasicAuth

from settings import PL_URL_TEST, PL_URL_ELASTIC_SEARCH, USER_ELATIC_SEARCH, PASSWORD_ELASTIC_SEARCH, ES_UPDATER_MODE

url_test = PL_URL_TEST + 'api/products/'
url_elastic_search = PL_URL_ELASTIC_SEARCH
es_repository = EsProductRepository()
es_client = es_repository.es
index = 'products_test'

def call_api_update_stock(productBizType, available, sku):
    update_stock = [{

        'sku': sku,
        'items': [
            {
                'branch': 'string',
                'branchName': 'string',
                'warehouse': 'string',
                'warehouseName': 'string',
                'location': 'string',
                'locationName': 'string',
                'storeCode': 'string',
                'productBizType': productBizType,
                'available': available,
                'onHand': 5,
                'reserved': 1,
                'timestamp': time.time()
            }
        ]

    }
    ]

    response = requests.put(url_test, json=update_stock)
    return response.json()


def call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2, time1, time2):
    update_stock = [
        {

            'sku': sku,
            'items': [
                {
                    'branch': 'string',
                    'branchName': 'string',
                    'warehouse': 'string',
                    'warehouseName': 'string',
                    'location': location1,
                    'locationName': 'string',
                    'storeCode': 'string',
                    'productBizType': productBizType1,
                    'available': available1,
                    'onHand': 5,
                    'reserved': 1,
                    'timestamp': time1
                }
            ]

        },
        {

            'sku': sku,
            'items': [
                {
                    'branch': 'string',
                    'branchName': 'string',
                    'warehouse': 'string',
                    'warehouseName': 'string',
                    'location': location2,
                    'locationName': 'string',
                    'storeCode': 'string',
                    'productBizType': productBizType2,
                    'available': available2,
                    'onHand': 5,
                    'reserved': 1,
                    'timestamp': time2
                }
            ]

        }
    ]

    response = requests.put(url_test, json=update_stock)
    return response.json()


def call_api_check_stock_elastic_search(sku):
    payload = {
        'query': {
            'match': {
                'sku': sku
            }
        }

    }
    param = {
        'path': es_repository._index+'/_search',
        'method': 'POST'
    }
    headers = {
        'kbn-version': '7.1.1',
        'Content-Type': 'application/json'
    }
    response = requests.post(url_elastic_search,
                             params=param,
                             json=payload,
                             headers=headers,
                             auth=HTTPBasicAuth(USER_ELATIC_SEARCH, PASSWORD_ELASTIC_SEARCH))

    return response.json()


class TestPL122():
    ISSUE_KEY = 'PL-122'
    def test_product_type_is_biz(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = biz
        :return:
        '''
        sku = 'qwer'
        productBizType = 'biz'
        available = 1
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        # print(data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type'])
        assert productBizType == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_product_type_is_disp(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = disp
        :return:
        '''
        sku = 'qwer'
        productBizType = 'disp'
        available = 2
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_product_type_is_outlet(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = outlet
        :return:
        '''
        sku = 'qwer'
        productBizType = 'outlet'
        available = 3
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_product_type_is_None(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = None
        :return:
        '''
        sku = 'qwer'
        productBizType = None
        available = 4
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert 'UNKNOWN' == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_product_type_is_empty(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = Rong
        :return:
        '''
        sku = 'qwer'
        productBizType = ''
        available = 5
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert 'UNKNOWN' == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_product_type_is_blank(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = khoang trang
        :return:
        '''
        sku = 'qwer'
        productBizType = ' '
        available = 6
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_product_type_is_blank_start_end(self):
        '''
        Kiem tra update ton kho cho san pham co product_biz_type = khoang trang dau cuoi
        :return:
        '''
        sku = 'qwer'
        productBizType = ' biz '
        available = 7
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['total_available']
        es_client.delete(index=es_repository._index, id=sku)

    def test_location_different_timestamp_different_productBizType_different(self):
        '''
        Kiem tra update ton kho cho san pham co location khac nhau, timestamp khac nhau, productBizType khac nhau
        :return:
        '''
        sku = 'sku1'
        productBizType1 = 'biz'
        productBizType2 = 'outlet'
        available1 = 7
        available2 = 8
        location1 = 'location1'
        location2 = 'location2'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2,location1, location2, time.time()-1, time.time() )
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][1]['type']
        assert available1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][1][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_location_different_timestamp_equal_productBizType_equal(self):
        '''
        Kiem tra update ton kho cho san pham co location khac nhau, timestamp giong nhau, productBizType giong nhau
        :return:
        '''
        sku = 'sku2'
        productBizType1 = 'biz'
        productBizType2 = 'biz'
        available1 = 7
        available2 = 8
        location1 = 'location1'
        location2 = 'location2'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2,location1, location2, time.time(), time.time() )
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available1 + available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)


    def test_location_same_timestamp_different_productBizType_different(self):
        '''
        Kiem tra update ton kho cho san pham co location giong nhau, timestamp khac nhau, productBizType khac nhau
        :return:
        '''
        sku = 'sku3'
        productBizType1 = 'biz'
        productBizType2 = 'outlet'
        available1 = 7
        available2 = 8
        location1 = 'location1'
        location2 = 'location1'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2,
                               time.time()-1, time.time())
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_location_same_timestamp_same_productBizType_same(self):
        '''
        Kiem tra update ton kho cho san pham co location giong nhau, timestamp giong nhau, productBizType giong nhau
        :return:
        '''
        sku = 'sku6'
        productBizType1 = 'biz'
        productBizType2 = 'biz'
        available1 = 9
        available2 = 10
        location1 = 'location1'
        location2 = 'location1'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2,
                               time.time(), time.time())
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_location_different_timestamp_different_productBizType_same(self):
        '''
        Kiem tra update ton kho cho san pham co location khac nhau, timestamp khac nhau, productBizType giong nhau
        :return:
        '''
        sku = 'sku7'
        productBizType1 = 'biz'
        productBizType2 = 'biz'
        available1 = 9
        available2 = 10
        location1 = 'location1'
        location2 = 'location2'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2,
                               time.time()-1, time.time())
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available1 + available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_location_different_timestamp_same_productBizType_different(self):
        '''
        Kiem tra update ton kho cho san pham co location khac nhau, timestamp giong nhau, productBizType khac nhau
        :return:
        '''
        sku = 'sku9'
        productBizType1 = 'biz'
        productBizType2 = 'outlet'
        available1 = 9
        available2 = 10
        location1 = 'location1'
        location2 = 'location2'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2,
                               time.time(), time.time())
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][1]['type']
        assert available1 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][1][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_location_same_timestamp_different_productBizType_same(self):
        '''
        Kiem tra update ton kho cho san pham co location khac nhau, timestamp giong nhau, productBizType khac nhau
        :return:
        '''
        sku = 'sku10'
        productBizType1 = 'biz'
        productBizType2 = 'biz'
        available1 = 9
        available2 = 10
        location1 = 'location1'
        location2 = 'location1'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2,
                               time.time()-1, time.time())
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_location_same_timestamp_same_productBizType_different(self):
        '''
        Kiem tra update ton kho cho san pham co location khac nhau, timestamp giong nhau, productBizType khac nhau
        :return:
        '''
        sku = 'sku10'
        productBizType1 = 'biz'
        productBizType2 = 'outlet'
        available1 = 9
        available2 = 10
        location1 = 'location1'
        location2 = 'location1'
        call_api_update_stocks(sku, productBizType1, productBizType2, available1, available2, location1, location2,
                               time.time(), time.time())
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_update_stock_when_exit_product_same_type(self):
        '''
        Kiem tra update ton kho khi da ton tai san pham co cung productBizType
        :return:
        '''
        sku = 'qwerty1'
        productBizType = 'biz'
        available = 1
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        call_api_update_stock(productBizType, available, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)

    def test_update_stock_when_exit_product_different_type(self):
        '''
        Kiem tra update ton kho khi da ton tai san pham khac productBizType
        :return:
        '''
        sku = 'qwerty2'
        productBizType1 = 'biz'
        available1 = 1
        call_api_update_stock(productBizType1, available1, sku)
        time.sleep(1)
        productBizType2 = 'outlet'
        available2 = 5
        call_api_update_stock(productBizType2, available2, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)
    def test_update_stock_when_exit_product_have_type_none(self):
        '''
        Kiem tra update ton kho khi da ton tai san pham co productBizType None
        :return:
        '''
        sku = 'qwerty3'
        productBizType1 = None
        available1 = 1
        call_api_update_stock(productBizType1, available1, sku)
        time.sleep(1)
        productBizType2 = 'outlet'
        available2 = 5
        call_api_update_stock(productBizType2, available2, sku)
        time.sleep(1)
        data_check = call_api_check_stock_elastic_search(sku)
        assert productBizType2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0]['type']
        assert available2 == data_check['hits']['hits'][0]['_source']['total_available_by_stock_types'][0][
            'total_available']
        es_client.delete(index=es_repository._index, id=sku)