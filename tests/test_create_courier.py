"""Тесты ручки POST /api/v1/courier — создание курьера."""

import allure
import pytest

from utils.helpers import generate_courier_data, register_courier, get_courier_id, delete_courier
from utils.urls import COURIER_URL


@allure.epic("QA Scooter API")
@allure.feature("Курьеры")
@allure.story("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера возвращает код 201")
    def test_create_courier_all_fields_returns_201(self, courier_data):
        response = register_courier(courier_data)

        try:
            assert response.status_code == 201
        finally:
            courier_id = get_courier_id(courier_data["login"], courier_data["password"])
            delete_courier(courier_id)

    @allure.title("Успешное создание курьера возвращает {{\"ok\": true}}")
    def test_create_courier_all_fields_returns_ok_true(self, courier_data):
        response = register_courier(courier_data)

        try:
            assert response.json() == {"ok": True}
        finally:
            courier_id = get_courier_id(courier_data["login"], courier_data["password"])
            delete_courier(courier_id)

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_create_courier_duplicate_login_returns_error(self, courier_data):
        first_response = register_courier(courier_data)
        assert first_response.status_code == 201, "Первого курьера создать не удалось"

        try:
            with allure.step("Повторно отправить запрос с тем же логином"):
                second_response = register_courier(courier_data)

            with allure.step("Проверить код ответа и текст ошибки"):
                assert second_response.status_code == 409
                assert second_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        finally:
            courier_id = get_courier_id(courier_data["login"], courier_data["password"])
            delete_courier(courier_id)

    @allure.title("Создание курьера с уже существующим логином возвращает ошибку")
    def test_create_courier_existing_login_returns_error_code(self, courier_data):
        register_courier(courier_data)

        try:
            duplicate = {
                "login": courier_data["login"],
                "password": generate_courier_data()["password"],
                "firstName": generate_courier_data()["firstName"],
            }
            response = register_courier(duplicate)

            assert response.status_code == 409
        finally:
            courier_id = get_courier_id(courier_data["login"], courier_data["password"])
            delete_courier(courier_id)

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_returns_error(self, courier_data):
        del courier_data["login"]

        response = register_courier(courier_data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_returns_error(self, courier_data):
        del courier_data["password"]

        response = register_courier(courier_data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Курьера можно создать без необязательного поля firstName")
    def test_create_courier_without_firstname_returns_201(self, courier_data):
        del courier_data["firstName"]

        response = register_courier(courier_data)

        try:
            assert response.status_code == 201
        finally:
            courier_id = get_courier_id(courier_data["login"], courier_data["password"])
            delete_courier(courier_id)
