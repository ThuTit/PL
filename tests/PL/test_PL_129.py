import requests
from es_updater.repository.es_product import EsProductRepository

from settings import PL_URL_TEST, ES_UPDATER_MODE

es_repository = EsProductRepository()
es_client = es_repository.es
url_pl = PL_URL_TEST + 'api/search/'
url_detail = PL_URL_TEST + 'api/products/'


def add_product(sku, type, available):
    product = {
        'sku': sku,
        'total_available_by_stock_types': [
            {
                'type': type,
                'total_available': available
            }
        ],
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
        ]
    }
    es_client.create(index=es_repository._index, id=product['sku'], body=product)


def add_product_have_2_type(sku, type1, type2, available1, available2):
    product = {
        'sku': sku,
        'total_available_by_stock_types': [
            {
                'type': type1,
                'total_available': available1
            },
            {
                'type': type2,
                'total_available': available2
            }
        ],
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
        ]
    }
    es_client.create(index=es_repository._index, id=product['sku'], body=product)


def add_product_have_3_type(sku, type1, type2, type3, available1, available2):
    product = {
        'sku': sku,
        'total_available_by_stock_types': [
            {
                'type': type1,
                'total_available': available1
            },
            {
                'type': type2,
                'total_available': available2
            },
            {
                'type': type3,
                'total_available': available2
            }
        ],
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
        ]
    }
    es_client.create(index=es_repository._index, id=product['sku'], body=product)


def refresh_indices():
    es_client.indices.refresh(index=es_repository._index)


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
        'DISABLE_SIGN': 'bG9pdGllbnByb2R1Y3RsaXN0aW5n'
    }
    response = requests.get(url=url_detail + sku, params=data)
    return response.json()


class TestPL129():
    ISSUE_KEY = 'PL-129'

    def test_search_product_type_is_biz(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = biz

        Step by step:
        - Tao du lieu san pham co product_biz_type = biz
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = biz
        :return:
        '''
        sku = 'test_sku_1'
        type = 'biz'
        available = 5
        add_product(sku, type, available)
        refresh_indices()
        result = call_api_search(sku)

        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available


    def test_detail_product_type_is_biz(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = biz

        Step by step:
        - Tao du lieu san pham co product_biz_type = biz
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = biz
        :return:
        '''
        sku = 'test_sku_1'
        type = 'biz'
        available = 5
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available
        es_client.delete(index=es_repository._index, id=sku)

    def test_search_product_type_is_disp(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = disp

        Step by step:
        - Tao du lieu san pham co product_biz_type = disp
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = disp
        :return:
        '''
        sku = 'test_sku_1'
        type = 'disp'
        available = 5
        add_product(sku, type, available)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available

    def test_detail_product_type_is_disp(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = disp

        Step by step:
        - Tao du lieu san pham co product_biz_type = disp
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = disp
        :return:
        '''
        sku = 'test_sku_1'
        type = 'disp'
        available = 5
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available
        es_client.delete(index=es_repository._index, id=sku)

    def test_search_product_type_is_outlet(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = outlet

        Step by step:
        - Tao du lieu san pham co product_biz_type = outlet
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = outlet
        :return:
        '''
        sku = 'test_sku_1'
        type = 'outlet'
        available = 5
        add_product(sku, type, available)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available


    def test_detail_product_type_is_outlet(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = outlet

        Step by step:
        - Tao du lieu san pham co product_biz_type = outlet
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = outlet
        :return:
        '''
        sku = 'test_sku_1'
        type = 'outlet'
        available = 5
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available
        es_client.delete(index=es_repository._index, id=sku)

    def test_search_product_type_is_None(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = None

        Step by step:
        - Tao du lieu san pham co product_biz_type = None
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = None
        :return:
        '''
        sku = 'test_sku_1'
        type = None
        available = 5
        add_product(sku, type, available)
        refresh_indices()
        result = call_api_search(sku)
        # print(call_api_search(sku))
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available

    def test_detail_product_type_is_None(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = None

        Step by step:
        - Tao du lieu san pham co product_biz_type = None
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = None
        :return:
        '''
        sku = 'test_sku_1'
        type = None
        available = 5
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available
        es_client.delete(index=es_repository._index, id=sku)


    def test_search_product_type_is_Empty(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type rong

        Step by step:
        - Tao du lieu san pham co product_biz_type = ''
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = ''
        :return:
        '''
        sku = 'test_sku_1'
        type = ''
        available = 5
        add_product(sku, type, available)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available

    def test_detail_product_type_is_Empty(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type rong

        Step by step:
        - Tao du lieu san pham co product_biz_type = ''
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = ''
        :return:
        '''
        sku = 'test_sku_1'
        type = ''
        available = 5
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available
        es_client.delete(index=es_repository._index, id=sku)

    def test_search_product_type_is_Blank(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = khoang trang

        Step by step:
        - Tao du lieu san pham co product_biz_type = ' '
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = ' '
        :return:
        '''
        sku = 'test_sku_1'
        type = ' '
        available = 5
        add_product(sku, type, available)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available

    def test_detail_product_type_is_Blank(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = khoang trang

        Step by step:
        - Tao du lieu san pham co product_biz_type = ' '
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = ' '
        :return:
        '''
        sku = 'test_sku_1'
        type = ' '
        available = 5
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available
        es_client.delete(index=es_repository._index, id=sku)

    def test_search_product_type_are_biz_disp(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = biz, disp

        Step by step:
        - Tao du lieu san pham co product_biz_type = biz, disp
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = biz, disp
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'biz'
        type2 = 'disp'
        available1 = 5
        available2 = 6
        add_product_have_2_type(sku, type1, type2, available1, available2)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['total'] == available2

    def test_detail_product_type_are_biz_disp(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = biz, disp

        Step by step:
        - Tao du lieu san pham co product_biz_type = biz, disp
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = biz, disp
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'biz'
        type2 = 'disp'
        available1 = 5
        available2 = 6
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['product']['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['product']['totalAvailableByStocks'][1]['total'] == available2
        es_client.delete(index=es_repository._index, id=sku)
    def test_search_product_type_are_biz_outlet(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = biz, outlet

        Step by step:
        - Tao du lieu san pham co product_biz_type = biz, outlet
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = biz, outlet
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'biz'
        type2 = 'outlet'
        available1 = 5
        available2 = 6
        add_product_have_2_type(sku, type1, type2, available1, available2)
        refresh_indices()
        result = call_api_search(sku)

        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['total'] == available2

    def test_detail_product_type_are_biz_outlet(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = biz, outlet

         Step by step:
        - Tao du lieu san pham co product_biz_type = biz, outlet
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = biz, outlet
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'biz'
        type2 = 'outlet'
        available1 = 5
        available2 = 6
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['product']['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['product']['totalAvailableByStocks'][1]['total'] == available2
        es_client.delete(index=es_repository._index, id=sku)
    def test_search_product_type_are_disp_outlet(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = disp, outlet

         Step by step:
        - Tao du lieu san pham co product_biz_type = disp, outlet
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = disp, outlet
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'disp'
        type2 = 'outlet'
        available1 = 5
        available2 = 6
        add_product_have_2_type(sku, type1, type2, available1, available2)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['total'] == available2


    def test_detail_product_type_are_disp_outlet(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = disp, outlet

         Step by step:
        - Tao du lieu san pham co product_biz_type = disp, outlet
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = disp, outlet
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'disp'
        type2 = 'outlet'
        available1 = 5
        available2 = 6
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['product']['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['product']['totalAvailableByStocks'][1]['total'] == available2
        es_client.delete(index=es_repository._index, id=sku)
    def test_search_product_type_are_disp_outlet_biz(self):
        '''
        Kiem tra ket qua tra ve cua API search voi product_biz_type = disp, outlet, biz

         Step by step:
        - Tao du lieu san pham co product_biz_type = disp, outlet, biz
        - Insert vao Elastic Search
        - Goi API search
        - Expect: Tra ve san pham co totalAvailableByStocks.type = disp, outlet, biz
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'disp'
        type2 = 'outlet'
        type3 = 'biz'
        available1 = 5
        available2 = 6
        add_product_have_3_type(sku, type1, type2, type3, available1, available2)
        refresh_indices()
        result = call_api_search(sku)
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['products'][0]['totalAvailableByStocks'][2]['type'] == type3
        assert result['result']['products'][0]['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['products'][0]['totalAvailableByStocks'][1]['total'] == available2
        assert result['result']['products'][0]['totalAvailableByStocks'][2]['total'] == available2

    def test_detail_product_type_are_disp_outlet_biz(self):
        '''
        Kiem tra ket qua tra ve cua API detail voi product_biz_type = disp, outlet, biz

          Step by step:
        - Tao du lieu san pham co product_biz_type = disp, outlet, biz
        - Insert vao Elastic Search
        - Goi API detail
        - Expect: Tra ve san pham co totalAvailableByStocks.type = disp, outlet, biz
        :return:
        '''
        sku = 'test_sku_1'
        type1 = 'disp'
        type2 = 'outlet'
        type3 = 'biz'
        available1 = 5
        available2 = 6
        result = call_api_detail(sku)
        assert result['result']['product']['totalAvailableByStocks'][0]['type'] == type1
        assert result['result']['product']['totalAvailableByStocks'][1]['type'] == type2
        assert result['result']['product']['totalAvailableByStocks'][2]['type'] == type3
        assert result['result']['product']['totalAvailableByStocks'][0]['total'] == available1
        assert result['result']['product']['totalAvailableByStocks'][1]['total'] == available2
        assert result['result']['product']['totalAvailableByStocks'][2]['total'] == available2
        es_client.delete(index=es_repository._index, id=sku)
