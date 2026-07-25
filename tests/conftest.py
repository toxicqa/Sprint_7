"""Общие фикстуры для всех тестов.

Ключевое правило проекта: тестовые данные создаются перед тестом и
удаляются после него, независимо от того, прошёл тест или упал.
"""

import allure
import pytest

from utils.helpers import (
    generate_courier_data,
    register_courier,
    get_courier_id,
    delete_courier,
    generate_order_payload,
    create_order,
    cancel_order,
)


@pytest.fixture
def courier_data():
    """Просто уникальные данные курьера, без создания на сервере."""
    return generate_courier_data()


@pytest.fixture
def registered_courier():
    """Создаёт курьера на сервере и гарантированно удаляет его после теста.

    Возвращает словарь с login/password/firstName и id курьера.
    """
    data = generate_courier_data()

    with allure.step("Подготовка: создать курьера для теста"):
        response = register_courier(data)
        assert response.status_code == 201, "Не удалось создать курьера в фикстуре"

    courier_id = get_courier_id(data["login"], data["password"])
    data["id"] = courier_id

    yield data

    with allure.step("Уборка: удалить курьера после теста"):
        delete_courier(courier_id)


@pytest.fixture
def order_track():
    """Создаёт заказ и возвращает его track. После теста заказ отменяется,
    чтобы не засорять тестовый стенд."""
    payload = generate_order_payload()

    with allure.step("Подготовка: создать заказ для теста"):
        response = create_order(payload)
        assert response.status_code == 201, "Не удалось создать заказ в фикстуре"
        track = response.json()["track"]

    yield track

    with allure.step("Уборка: отменить заказ после теста"):
        cancel_order(track)
