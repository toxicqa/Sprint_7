"""Тесты ручки POST /api/v1/courier/login — авторизация курьера."""

import allure
import pytest

from utils.helpers import generate_courier_data, login_courier


@allure.epic("QA Scooter API")
@allure.feature("Курьеры")
@allure.story("Логин курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться и получает код 200")
    def test_login_courier_valid_credentials_returns_200(self, registered_courier):
        response = login_courier(registered_courier["login"], registered_courier["password"])

        assert response.status_code == 200

    @allure.title("Успешная авторизация возвращает id курьера")
    def test_login_courier_valid_credentials_returns_id(self, registered_courier):
        response = login_courier(registered_courier["login"], registered_courier["password"])

        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Нельзя авторизоваться без логина")
    def test_login_courier_without_login_returns_error(self, registered_courier):
        response = login_courier(None, registered_courier["password"])

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Нельзя авторизоваться без пароля")
    @pytest.mark.xfail(
        reason=(
            "Известный баг сервиса: если поле password отсутствует в запросе "
            "вовсе (а не пустое), сервер отвечает 504 Gateway Timeout вместо "
            "ожидаемых 400 и текста ошибки. Тест оставлен как документация бага — "
            "если сервис починят, он станет падать в XPASS."
        ),
        strict=False,
    )
    def test_login_courier_without_password_returns_error(self, registered_courier):
        response = login_courier(registered_courier["login"], None)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация с неверным паролем возвращает ошибку")
    def test_login_courier_wrong_password_returns_error(self, registered_courier):
        response = login_courier(registered_courier["login"], "wrong_password_123")

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация с несуществующим логином возвращает ошибку")
    def test_login_courier_nonexistent_login_returns_error(self):
        nonexistent = generate_courier_data()

        response = login_courier(nonexistent["login"], nonexistent["password"])

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
