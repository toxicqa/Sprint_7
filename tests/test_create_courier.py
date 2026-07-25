"""Тесты ручки POST /api/v1/courier — создание курьера."""

import allure

from utils.helpers import generate_courier_data, register_courier


@allure.epic("QA Scooter API")
@allure.feature("Курьеры")
@allure.story("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера возвращает код 201")
    def test_create_courier_all_fields_returns_201(self, courier_cleanup):
        data = generate_courier_data()

        response = register_courier(data)
        courier_cleanup.append((data["login"], data["password"]))

        assert response.status_code == 201

    @allure.title("Успешное создание курьера возвращает {{\"ok\": true}}")
    def test_create_courier_all_fields_returns_ok_true(self, courier_cleanup):
        data = generate_courier_data()

        response = register_courier(data)
        courier_cleanup.append((data["login"], data["password"]))

        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_create_courier_duplicate_login_returns_error(self, courier_cleanup):
        data = generate_courier_data()
        register_courier(data)
        courier_cleanup.append((data["login"], data["password"]))

        with allure.step("Повторно отправить запрос с тем же логином"):
            second_response = register_courier(data)

        assert second_response.status_code == 409
        assert second_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Создание курьера с уже существующим логином возвращает ошибку")
    def test_create_courier_existing_login_returns_error_code(self, courier_cleanup):
        data = generate_courier_data()
        register_courier(data)
        courier_cleanup.append((data["login"], data["password"]))

        duplicate = generate_courier_data()
        duplicate["login"] = data["login"]

        response = register_courier(duplicate)

        assert response.status_code == 409

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_returns_error(self):
        data = generate_courier_data()
        del data["login"]

        response = register_courier(data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_returns_error(self):
        data = generate_courier_data()
        del data["password"]

        response = register_courier(data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Курьера можно создать без необязательного поля firstName")
    def test_create_courier_without_firstname_returns_201(self, courier_cleanup):
        data = generate_courier_data()
        del data["firstName"]

        response = register_courier(data)
        courier_cleanup.append((data["login"], data["password"]))

        assert response.status_code == 201
