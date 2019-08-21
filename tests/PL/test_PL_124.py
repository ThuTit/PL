import pytest
from es_updater.decorators import srm_updater
from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository
from settings import ES_UPDATER_MODE

es_repository = EsProductRepository()
es_client = es_repository.es



@srm_updater
def update_srm(product):
    return product


class TestPL124():
    ISSUE_KEY = 'PL-124'
    def test_get_sale_point_is_duong(self):
        '''
        Kiểm tra lấy sale point từ SRM với sale_point là số dương

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu insert và dữ liệu ES trả về
        -> Expect: 2 bộ dữ liệu trùng khớp
        :return:
        '''
        product_srm = fake.srm_product(sale_point=10)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        assert res['_source'] == product_srm
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_is_0(self):
        '''
        Kiểm tra lấy sale point từ SRM với sale_point là 0

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu insert và dữ liệu ES trả về
        -> Expect: 2 bộ dữ liệu trùng khớp
        :return:
        '''
        product_srm = fake.srm_product(sale_point=0)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        assert res['_source'] == product_srm
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_is_am(self):
        '''
        Kiểm tra lấy sale point từ SRM với sale_point là 0

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu insert và dữ liệu ES trả về
        -> Expect: 2 bộ dữ liệu trùng khớp
        :return:
        '''
        product_srm = fake.srm_product(sale_point=-10)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        assert res['_source'] == product_srm
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_is_string_so(self):
        '''
        Kiểm tra lấy sale point từ SRM với sale_point là string dạng số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu insert và dữ liệu ES trả về
        -> Expect: 2 bộ dữ liệu trùng khớp
        :return:
        '''
        product_srm = fake.srm_product(sale_point='123')
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        assert res['_source'] == product_srm
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_get_sale_point_is_string_chu(self):
        '''
        Kiểm tra lấy sale point từ SRM với sale_point là string dạng chữ

        Step by step:
        - Insert dữ liệu vào ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_srm = fake.srm_product(sale_point='12ert')
            update_srm(product_srm)

    def test_get_sale_point_is_null(self):
        '''
        Kiểm tra lấy sale point từ SRM với sale_point = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu insert và dữ liệu ES trả về
        -> Expect: 2 bộ dữ liệu trùng khớp
        :return:
        '''
        product_srm = fake.srm_product(sale_point=None)
        update_srm(product_srm)
        res = es_client.get(index=es_repository._index, id=product_srm['sku'])
        assert res['_source'] == product_srm
        es_client.delete(index=es_repository._index, id=product_srm['sku'])

    def test_do_not_have_sale_point(self):
        '''
        Kiểm tra ingest dữ liệu không có trường sale_point

        Step by step:
        - Insert dữ liệu vào ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_srm = fake.srm_product()
            del product_srm['sale_point']
            update_srm(product_srm)
