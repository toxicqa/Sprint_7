"""Тесты ручки GET /api/v1/orders — получение списка заказов."""

import allure

from utils.helpers import get_orders_list


@allure.epic("QA Scooter API")
@allure.feature("Заказы")
@allure.story("Список заказов")
class TestGetOrdersList:

    @allure.title("Запрос списка заказов возвращает код 200")
    def test_get_orders_list_returns_200(self):
        response = get_orders_list()

        assert response.status_code == 200

    @allure.title("Тело ответа содержит список заказов orders")
    def test_get_orders_list_returns_orders_key(self):
        response = get_orders_list()

        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
