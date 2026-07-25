"""Тесты ручки GET /api/v1/orders/track — получить заказ по номеру.

Дополнительное задание.
"""

import allure

from utils.helpers import wait_for_order_by_track, get_order_by_track


@allure.epic("QA Scooter API")
@allure.feature("Заказы")
@allure.story("Получить заказ по номеру")
class TestGetOrderByTrack:

    @allure.title("Запрос с существующим треком возвращает код 200")
    def test_get_order_by_track_returns_200(self, order_track):
        # ретраи нужны: сразу после создания заказ иногда ещё не проиндексирован
        response = wait_for_order_by_track(order_track)

        assert response.status_code == 200

    @allure.title("Запрос с существующим треком возвращает объект заказа")
    def test_get_order_by_track_returns_order(self, order_track):
        response = wait_for_order_by_track(order_track)

        assert "order" in response.json()

    @allure.title("Запрос без номера трека возвращает ошибку")
    def test_get_order_by_track_without_track_returns_error(self):
        response = get_order_by_track("")

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Запрос с несуществующим треком возвращает ошибку")
    def test_get_order_by_track_nonexistent_track_returns_error(self):
        response = get_order_by_track(999999999)

        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"
