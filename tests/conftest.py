"""Общие фикстуры для всех тестов.

Правило: фикстуры отвечают только за подготовку предусловий и уборку после
теста. Внутри фикстур нет проверок (assert) — иначе тест, который её
использует, становится неатомарным: непонятно, упал он из-за проверяемой
логики или из-за проблемы в самом предусловии.

Для тестов, где создание курьера/заказа — сам предмет проверки (например,
tests/test_create_courier.py), используются фикстуры-коллекторы
courier_cleanup и order_cleanup: тест сам решает, что именно получилось
создать, и складывает данные для уборки в список, а фикстура удаляет/отменяет
их после теста.
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
def registered_courier():
    """Предусловие: на сервере уже есть курьер. Используется там, где
    курьер — просто предпосылка теста (логин, принятие заказа), а не то,
    что тест проверяет. Курьер гарантированно удаляется после теста."""
    data = generate_courier_data()

    with allure.step("Подготовка: создать курьера для теста"):
        register_courier(data)
        courier_id = get_courier_id(data["login"], data["password"])
        data["id"] = courier_id

    yield data

    with allure.step("Уборка: удалить курьера после теста"):
        delete_courier(courier_id)


@pytest.fixture
def order_track():
    """Предусловие: на сервере уже есть заказ. Используется там, где
    заказ — просто предпосылка теста (принятие, поиск по треку), а не то,
    что тест проверяет. Заказ отменяется после теста."""
    payload = generate_order_payload()

    with allure.step("Подготовка: создать заказ для теста"):
        response = create_order(payload)
        track = response.json()["track"]

    yield track

    with allure.step("Уборка: отменить заказ после теста"):
        cancel_order(track)


@pytest.fixture
def courier_cleanup():
    """Для тестов, где создание курьера — предмет проверки: тест сам
    добавляет в список (login, password) успешно созданных курьеров,
    а фикстура удаляет их после теста."""
    couriers = []

    yield couriers

    with allure.step("Уборка: удалить курьеров, созданных в тесте"):
        for login, password in couriers:
            courier_id = get_courier_id(login, password)
            delete_courier(courier_id)


@pytest.fixture
def order_cleanup():
    """Для тестов, где создание заказа — предмет проверки: тест сам
    добавляет в список трек успешно созданного заказа, а фикстура
    отменяет заказы после теста."""
    tracks = []

    yield tracks

    with allure.step("Уборка: отменить заказы, созданные в тесте"):
        for track in tracks:
            cancel_order(track)
