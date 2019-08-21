import pytest
import requests
from es_updater.decorators import ppm_updater
from es_updater.faker import fake
from es_updater.repository.es_product import EsProductRepository
from settings import ES_UPDATER_MODE, PL_URL_TEST

es_repository = EsProductRepository()
es_client = es_repository.es


@ppm_updater
def update_ppm(product):
    return product


class TestPL135():
    ISSUE_KEY ='PL-135'
    def test_get_coupon_success(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM thành công

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu trùng khớp
        :return:
        '''
        product_ppm = fake.ppm_product()
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source'] == product_ppm
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])

    def test_get_coupon_budget_status_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi budget_status null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=fake.coupon(
                            budget_status=None)
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
        # res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        # # print(res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'])
        # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
        #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == None
        # es_client.delete(index=es_repository._index, id=product_ppm['sku'])

    def test_get_coupon_budget_status_int(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi budget_status là số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=fake.coupon(
                            budget_status=123)
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)

    def test_get_coupon_budget_status_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường budget_status

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=fake.coupon(
                            budget_status='active')
                        )
                    )))
                ]))
            ])
            del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status']
            update_ppm(product_ppm)

    # def test_get_coupon_budget_status_have_space(self):
    #     '''
    #     Kiểm tra lấy dữ liệu coupon từ PPM khi trường budget_status có space đầu cuối
    #
    #     Step by step:
    #     - Insert dữ liệu vào ES
    #     - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
    #     -> Expect: Trim space, dữ liệu trùng khớp
    #     :return:
    #     '''
    #
    #     product_ppm = fake.ppm_product(promotions=[
    #         (fake.promotion(definitions=[
    #             (fake.promotion_definition(benefit=(
    #                 fake.benefit(coupon=fake.coupon(
    #                     budget_status=' active ')
    #                 )
    #             )))
    #         ]))
    #     ])
    #     update_ppm(product_ppm)
    #     res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
    #     assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
    #            product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == 'active'

    def test_get_coupon_id_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.id = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(id=None)
                        ))
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
            res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
            # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
            #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == 'active'

    def test_get_coupon_id_string_chu(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.id = string dạng chữ

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(id='qưerqw')
                        ))
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)

    def test_get_coupon_id_string_so(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.id = string dạng số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''

        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                    fake.coupon(applied_promotion=(
                        fake.applied_promotion(id='123')
                    ))
                    )
                )))
            ]))
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['id'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['id'] == 123
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])

    def test_get_coupon_id_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường applied_promotion.id

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(id=154)
                        ))
                        )
                    )))
                ]))
            ])
            del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['id']
            update_ppm(product_ppm)

    def test_get_coupon_name_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.name = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(name=None)
                        ))
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
            res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
            # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
            #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == 'active'
    def test_get_coupon_name_string_so(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.name = string dạng số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''


        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                    fake.coupon(applied_promotion=(
                        fake.applied_promotion(name='12345')
                    ))
                    )
                )))
            ]))
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['name'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['name'] == '12345'
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    def test_get_coupon_name_int(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.name = int

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(name=122)
                        ))
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
        # product_ppm = fake.ppm_product(promotions=[
        #     (fake.promotion(definitions=[
        #         (fake.promotion_definition(benefit=(
        #             fake.benefit(coupon=
        #             fake.coupon(applied_promotion=(
        #                 fake.applied_promotion(name='<h4>thunt</h4>')
        #             ))
        #             )
        #         )))
        #     ]))
        # ])
        # update_ppm(product_ppm)
        # res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['name'] == \
        #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['name'] == '<h4>thunt</h4>'

    def test_get_coupon_name_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường applied_promotion.name

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(name='ègthte')
                        ))
                        )
                    )))
                ]))
            ])
            del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['name']
            update_ppm(product_ppm)
    def test_get_coupon_description_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.description = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(description=None)
                        ))
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
            res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
            # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
            #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == 'active'

    def test_get_coupon_description_int(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.description = int

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(description=122)
                        ))
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)

    def test_get_coupon_description_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường applied_promotion.description

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(applied_promotion=(
                            fake.applied_promotion(description='description')
                        ))
                        )
                    )))
                ]))
            ])
            del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['description']
            update_ppm(product_ppm)

    def test_get_coupon_description_string_dang_so(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường applied_promotion.description là string dạng số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''


        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                    fake.coupon(applied_promotion=(
                        fake.applied_promotion(description='123456')
                    ))
                    )
                )))
            ]))
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['description'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']['description'] == '123456'
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    # ////
    def test_get_coupon_max_quantity_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường max_quantity = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(max_quantity=(None)
                        )
                        )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
            res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
            # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
            #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == 'active'

    def test_get_coupon_max_quantity_string_chu(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường max_quantity = string dạng chữ

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                        fake.coupon(max_quantity='qưerqw')
                        )
                        )
                    ))])
                )
            ])
            update_ppm(product_ppm)

    def test_get_coupon_max_quantity_string_so(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường max_quantity = string dạng số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''

        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(max_quantity='123')
                                 )
                )
                ))])
            )
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['max_quantity'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['max_quantity'] == 123
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    def test_get_coupon_max_quantity_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường max_quantity

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                                     fake.coupon(max_quantity='123')
                                     )
                    )
                    ))])
                )
            ])
            update_ppm(product_ppm)
            del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['max_quantity']
            update_ppm(product_ppm)

        # ////

    def test_get_coupon_quantity_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường quantity = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                                     fake.coupon(quantity=(None)
                                                 )
                                     )
                    )))
                ]))
            ])
            update_ppm(product_ppm)
            res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
            # assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == \
            #        product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['budget_status'] == 'active'

    def test_get_coupon_quantity_string_chu(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường quantity = string dạng chữ

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                                     fake.coupon(quantity='qưerqw')
                                     )
                    )
                    ))])
                )
            ])
            update_ppm(product_ppm)

    def test_get_coupon_quantity_string_so(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường quantity = string dạng số

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''

        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(quantity='123')
                                 )
                )
                ))])
            )
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity'] == 123
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    def test_get_coupon_quantity_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường quantity

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''
        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                                     fake.coupon(quantity='123')
                                     )
                    )
                    ))])
                )
            ])
            update_ppm(product_ppm)
            del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['quantity']
            update_ppm(product_ppm)

    def test_get_coupon_out_of_budget_different_True_False(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi trường out_of_budget khác True, False

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Hiển thị thông báo lỗi
        :return:
        '''

        with pytest.raises(Exception):
            product_ppm = fake.ppm_product(promotions=[
                (fake.promotion(definitions=[
                    (fake.promotion_definition(benefit=(
                        fake.benefit(coupon=
                                     fake.coupon(out_of_budget='qưerqw')
                                     )
                    )
                    ))])
                )
            ])
            update_ppm(product_ppm)



    def test_get_coupon_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi coupon = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''

        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=None
                ))
                ))])
            )
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon'] == None
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    def test_get_coupon_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường coupon

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''
        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(out_of_budget=True)
                                 )
                )
                ))])
            )
        ])

        del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']
        update_ppm(product_ppm)
        print(product_ppm['promotions'][0]['definitions'][0]['benefit'])
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        print(res['_source']['promotions'][0]['definitions'][0]['benefit'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    def test_get_coupon_applied_promotion_null(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi applied_promotion = null

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''

        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(applied_promotion=None)
                ))
                ))])
            )
        ])
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion'] == None
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])
    def test_get_coupon_applied_promotion_not_found(self):
        '''
        Kiểm tra lấy dữ liệu coupon từ PPM khi không có trường applied_promotion

        Step by step:
        - Insert dữ liệu vào ES
        - Kiểm tra dữ liệu đầu vào và dữ liệu từ ES
        -> Expect: Dữ liệu giống nhau
        :return:
        '''
        product_ppm = fake.ppm_product(promotions=[
            (fake.promotion(definitions=[
                (fake.promotion_definition(benefit=(
                    fake.benefit(coupon=
                                 fake.coupon(applied_promotion=(
                        fake.applied_promotion(description='123456')
                    ))
                                 )
                )
                ))])
            )
        ])

        del product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']['applied_promotion']
        update_ppm(product_ppm)
        res = es_client.get(index=es_repository._index, id=product_ppm['sku'])
        assert res['_source']['promotions'][0]['definitions'][0]['benefit']['coupon'] == \
               product_ppm['promotions'][0]['definitions'][0]['benefit']['coupon']
        es_client.delete(index=es_repository._index, id=product_ppm['sku'])