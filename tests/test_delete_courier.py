"""Тесты ручки DELETE /api/v1/courier/{id} — удаление курьера.

Дополнительное задание.
"""

import allure

from utils.helpers import generate_courier_data, register_courier, get_courier_id, delete_courier


@allure.epic("QA Scooter API")
@allure.feature("Курьеры")
@allure.story("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Успешное удаление курьера возвращает {{\"ok\": true}}")
    def test_delete_courier_returns_ok_true(self):
        data = generate_courier_data()
        register_courier(data)
        courier_id = get_courier_id(data["login"], data["password"])

        response = delete_courier(courier_id)

        assert response.json() == {"ok": True}

    @allure.title("Успешное удаление курьера возвращает код 200")
    def test_delete_courier_returns_200(self):
        data = generate_courier_data()
        register_courier(data)
        courier_id = get_courier_id(data["login"], data["password"])

        response = delete_courier(courier_id)

        assert response.status_code == 200

    @allure.title("Удаление без id возвращает ошибку")
    def test_delete_courier_without_id_returns_error(self):
        response = delete_courier("")

        assert response.status_code == 404

    @allure.title("Удаление курьера с несуществующим id возвращает ошибку")
    def test_delete_courier_nonexistent_id_returns_error(self):
        response = delete_courier(999999999)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет."
