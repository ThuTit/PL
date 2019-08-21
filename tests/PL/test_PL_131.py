import pytest
from es_updater.faker import fake
from es_updater.decorators import catalog_updater
from es_updater.repository.es_product import EsProductRepository
from settings import ES_UPDATER_MODE

es_repository = EsProductRepository()
es_client = es_repository.es


@catalog_updater
def update_catalog(product):
    return product


class TestPL131():
    ISSUE_KEY = 'PL-131'

    def test_update_cat_is_bundle_products(self):
        '''
        Kiem tra update san pham catalog khi san pham la bundle

        Step by step:
        - Tao du lieu san pham la bundle
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product()
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_miss_bundle_products(self):
        '''
        Kiem tra update san pham catalog khi thieu truong bundle_products

        Step by step:
        - Tao du lieu san pham thieu truong bundle_products
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product()
        del product_catalog['bundle_products']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_miss_parent_bundles(self):
        '''
        Kiem tra update san pham catalog khi thieu truong parent_bundles

        Step by step:
        - Tao du lieu san pham thieu truong parent_bundles
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product()
        del product_catalog['parent_bundles']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_miss_is_bundle(self):
        '''
        Kiem tra update san pham catalog khi thieu truong is_bundle

        Step by step:
        - Tao du lieu san pham thieu truong is_bundle
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product()
        del product_catalog['is_bundle']
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_bundle_products_null(self):
        '''
        Kiem tra update san pham catalog khi truong bundle_products null

        Step by step:
        - Tao du lieu san pham truong bundle_products null
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product(bundle_products=[])
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_parent_bundles_null(self):
        '''
        Kiem tra update san pham catalog khi truong parent_bundles null

        Step by step:
        - Tao du lieu san pham truong parent_bundles null
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product(parent_bundles=[])
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_is_bundle_null(self):
        '''
        Kiem tra update san pham catalog khi truong is_bundle null

        Step by step:
        - Tao du lieu san pham truong is_bundle null
        - Update du lieu vao ES
        - So sanh du lieu vua tao va du lieu duoc update vao ES
        - Expect: Du lieu 2 ben trung khop
        :return:
        '''
        product_catalog = fake.catalog_product(is_bundle=None)
        update_catalog(product_catalog)
        res = es_client.get(index=es_repository._index, id=product_catalog['sku'])
        assert res['_source'] == product_catalog
        es_client.delete(index=es_repository._index, id=product_catalog['sku'])

    def test_update_cat_is_bundle_is_string(self):
        '''
        Kiem tra update san pham catalog khi truong is_bundle la string

        Step by step:
        - Tao du lieu san pham truong is_bundle la string
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(is_bundle='sbd')
            update_catalog(product_catalog)

    def test_update_cat_is_bundle_different_1_0(self):
        '''
        Kiem tra update san pham catalog khi truong is_bundle co gia tri khac 1, 0

        Step by step:
        - Tao du lieu san pham truong is_bundle co gia tri khac 1, 0
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(is_bundle=2)
            update_catalog(product_catalog)

    def test_update_cat_bundle_products_sku_int(self):
        '''
        Kiem tra update san pham catalog khi truong bundle_products.sku la int

        Step by step:
        - Tao du lieu san pham truong bundle_products.sku la int
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(bundle_products=[fake.bundle_product(sku=12345)])
            update_catalog(product_catalog)

    def test_update_cat_bundle_products_name_int(self):
        '''
        Kiem tra update san pham catalog khi truong bundle_products.name la int

        Step by step:
        - Tao du lieu san pham truong bundle_products.name la int
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(bundle_products=[fake.bundle_product(name=12345)])
            update_catalog(product_catalog)

    def test_update_cat_bundle_products_quantity_string(self):
        '''
        Kiem tra update san pham catalog khi truong bundle_products.quantity la string

        Step by step:
        - Tao du lieu san pham truong bundle_products.quantity la string
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(bundle_products=[fake.bundle_product(quantity='dfdf')])
            update_catalog(product_catalog)

    def test_update_cat_bundle_products_priority_string(self):
        '''
        Kiem tra update san pham catalog khi truong bundle_products.priority la string

        Step by step:
        - Tao du lieu san pham truong bundle_products.priority la string
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(bundle_products=[fake.bundle_product(priority='dfdf')])
            update_catalog(product_catalog)

    def test_update_cat_parent_bundles_sku_int(self):
        '''
        Kiem tra update san pham catalog khi truong parent_bundles.sku la int

        Step by step:
        - Tao du lieu san pham truong parent_bundles.sku la int
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(parent_bundles=[fake.bundle_product(sku=123659)])
            update_catalog(product_catalog)

    def test_update_cat_parent_bundles_name_int(self):
        '''
        Kiem tra update san pham catalog khi truong parent_bundles.name la int

        Step by step:
        - Tao du lieu san pham truong parent_bundles.name la int
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(parent_bundles=[fake.bundle_product(name=123659)])
            update_catalog(product_catalog)

    def test_update_cat_parent_bundles_seo_name_int(self):
        '''
        Kiem tra update san pham catalog khi truong parent_bundles.seo_name la int

        Step by step:
        - Tao du lieu san pham truong parent_bundles.seo_name la int
        - Update du lieu vao ES
        - Expect: Bao loi
        :return:
        '''
        with pytest.raises(Exception):
            product_catalog = fake.catalog_product(parent_bundles=[fake.bundle_product(seo_name=123659)])
            update_catalog(product_catalog)
