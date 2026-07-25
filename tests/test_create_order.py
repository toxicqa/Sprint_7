"""Тесты ручки POST /api/v1/orders — создание заказа.

Параметризация проверяет все допустимые варианты поля color:
один цвет, оба цвета и полное отсутствие поля.
"""

import allure
import pytest

from utils.helpers import generate_order_payload, create_order


@allure.epic("QA Scooter API")
@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None,
        ],
        ids=[
            "color_black",
            "color_grey",
            "color_black_and_grey",
            "color_not_specified",
        ],
    )
    @allure.title("Заказ создаётся с любым набором цветов и код ответа 201")
    def test_create_order_with_color_returns_201(self, color, order_cleanup):
        payload = generate_order_payload(color=color)

        response = create_order(payload)
        order_cleanup.append(response.json()["track"])

        assert response.status_code == 201

    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None,
        ],
        ids=[
            "color_black",
            "color_grey",
            "color_black_and_grey",
            "color_not_specified",
        ],
    )
    @allure.title("Тело ответа при создании заказа содержит track")
    def test_create_order_with_color_returns_track(self, color, order_cleanup):
        payload = generate_order_payload(color=color)

        response = create_order(payload)
        order_cleanup.append(response.json().get("track"))

        assert "track" in response.json()
