"""Тесты ручки PUT /api/v1/orders/accept/{id} — принять заказ.

Дополнительное задание.
"""

import allure

from utils.helpers import get_order_id_by_track, accept_order


@allure.epic("QA Scooter API")
@allure.feature("Заказы")
@allure.story("Принять заказ")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа возвращает {{\"ok\": true}}")
    def test_accept_order_returns_ok_true(self, registered_courier, order_track):
        order_id = get_order_id_by_track(order_track)

        response = accept_order(order_id, registered_courier["id"])

        assert response.json() == {"ok": True}

    @allure.title("Успешное принятие заказа возвращает код 200")
    def test_accept_order_returns_200(self, registered_courier, order_track):
        order_id = get_order_id_by_track(order_track)

        response = accept_order(order_id, registered_courier["id"])

        assert response.status_code == 200

    @allure.title("Принять заказ без id курьера — возвращается ошибка")
    def test_accept_order_without_courier_id_returns_error(self, order_track):
        order_id = get_order_id_by_track(order_track)

        response = accept_order(order_id, "")

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Принять заказ с несуществующим id курьера — возвращается ошибка")
    def test_accept_order_wrong_courier_id_returns_error(self, order_track):
        order_id = get_order_id_by_track(order_track)

        response = accept_order(order_id, 999999999)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id не существует"

    @allure.title("Принять заказ без id заказа — возвращается ошибка")
    def test_accept_order_without_order_id_returns_error(self, registered_courier):
        response = accept_order("", registered_courier["id"])

        assert response.status_code == 404

    @allure.title("Принять заказ с несуществующим id заказа — возвращается ошибка")
    def test_accept_order_wrong_order_id_returns_error(self, registered_courier):
        response = accept_order(999999999, registered_courier["id"])

        assert response.status_code == 404
        assert response.json()["message"] == "Заказа с таким id не существует"
