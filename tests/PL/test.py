import os
from settings import ES_UPDATER_MODE
from es_updater.decorators import catalog_updater, ppm_updater
from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository


es_repository = EsProductRepository()
es_client = es_repository.es
from es_updater.esconfig import EsConfig
from es_updater.repository.es_product import EsProductRepository

# if __name__ == '__main__':
#     EsProductRepository().save({
#         {
#             "sku": "1234",
#             "total_available_by_stock_types": [
#                 {
#                     "type": "Biz",
#                     "total_available": 3
#                 },
#                 {
#                     "type": "Disp",
#                     "total_available": 7
#                 }
#             ],
#             "channels": [
#                 {
#                     "code": "pv_showroom",
#                     "name": "Showroom Phong Vũ",
#                     "id": 1
#                 },
#                 {
#                     "code": "pv_online",
#                     "name": "Phong Vũ online",
#                     "id": 2
#                 },
#                 {
#                     "code": "pv_agent",
#                     "name": "Đại lý Phong Vũ",
#                     "id": 4
#                 }
#             ],
#             "name": "ốp MBA11'' JCPAL Ultra-thin- J4015 (Trong suốt)",
#             "categories": [
#                 {
#                     "code": "01-N002",
#                     "level": 1,
#                     "parent_id": 0,
#                     "name": "Phụ Kiện Laptop",
#                     "id": 3
#                 },
#                 {
#                     "code": "01-N002-08",
#                     "level": 2,
#                     "parent_id": 3,
#                     "name": "Túi đựng laptop",
#                     "id": 153
#                 },
#                 {
#                     "code": "01-N002-08-99",
#                     "level": 3,
#                     "parent_id": 153,
#                     "name": "Túi Laptop Khác",
#                     "id": 168
#                 }
#             ]
#         }
#     })


@ppm_updater
def update_ppm(product):
    return product


if __name__ == '__main__':
    # product_ppm = fake.ppm_product()
    # # # del product_ppm["bundle_products"]
    # update_ppm(product_ppm)
    # print(product_ppm['sku'])
    # print(product_catalog)
    es_client.delete(index=es_repository._index, id='test_sku_1')
    # es_client.delete(index= 'products_test_v2', id=product_catalog['sku'])
    # res = es_client.get(index= ES_UPDATER_MODE, id= product_catalog['sku'])
    # print(res)
