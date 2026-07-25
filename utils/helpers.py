"""Вспомогательные функции: генерация тестовых данных и обёртки над запросами,
которые часто повторяются в разных тестах (создание/удаление курьера,
поиск id заказа по треку и т. п.)."""

import random
import string
import time

import allure
import requests

from utils.urls import (
    COURIER_URL,
    COURIER_LOGIN_URL,
    ORDERS_URL,
    ORDERS_CANCEL_URL,
    ORDERS_TRACK_URL,
    ORDERS_ACCEPT_URL,
)


def generate_random_string(length: int = 10) -> str:
    """Генерирует строку из случайных строчных латинских букв заданной длины."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_courier_data() -> dict:
    """Генерирует уникальные данные нового курьера: login, password, firstName."""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }


def generate_order_payload(color=None) -> dict:
    """Собирает тело запроса на создание заказа. Параметр color позволяет
    задать список цветов самоката (или не задавать его вовсе)."""
    payload = {
        "firstName": generate_random_string(8),
        "lastName": generate_random_string(8),
        "address": f"{random.randint(1, 200)} улица Пушкина, дом {random.randint(1, 50)}",
        "metroStation": str(random.randint(1, 200)),
        "phone": f"+7{random.randint(1000000000, 9999999999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2026-08-01",
        "comment": "Комментарий к заказу для теста",
    }
    if color is not None:
        payload["color"] = color
    return payload


@allure.step("Зарегистрировать нового курьера")
def register_courier(courier_data: dict) -> requests.Response:
    return requests.post(COURIER_URL, data=courier_data, timeout=20)


@allure.step("Авторизовать курьера и получить его id")
def login_courier(login: str = None, password: str = None) -> requests.Response:
    """None означает «поле не передавать вовсе», а не «передать пустое значение» —
    requests иначе сериализует None как строку 'None', и сервер обрабатывает
    это не так, как реальное отсутствие поля."""
    payload = {}
    if login is not None:
        payload["login"] = login
    if password is not None:
        payload["password"] = password
    return requests.post(COURIER_LOGIN_URL, data=payload, timeout=20)


@allure.step("Получить id курьера по логину/паролю")
def get_courier_id(login: str, password: str) -> int:
    response = login_courier(login, password)
    return response.json()["id"]


@allure.step("Удалить курьера по id")
def delete_courier(courier_id) -> requests.Response:
    return requests.delete(f"{COURIER_URL}/{courier_id}", timeout=20)


@allure.step("Создать заказ")
def create_order(payload: dict) -> requests.Response:
    return requests.post(ORDERS_URL, json=payload, timeout=20)


@allure.step("Получить список заказов")
def get_orders_list(params: dict = None) -> requests.Response:
    return requests.get(ORDERS_URL, params=params, timeout=20)


@allure.step("Дождаться, пока заказ станет доступен по треку")
def wait_for_order_by_track(track, attempts: int = 5, delay: float = 1.0) -> requests.Response:
    """Сразу после создания заказа сервис не всегда готов найти его по треку —
    видимо, есть небольшая задержка индексации на сервере. Поэтому опрашиваем
    ручку несколько раз с паузой, прежде чем считать, что заказа нет."""
    response = requests.get(ORDERS_TRACK_URL, params={"t": track}, timeout=20)
    for _ in range(attempts - 1):
        if response.status_code == 200:
            return response
        time.sleep(delay)
        response = requests.get(ORDERS_TRACK_URL, params={"t": track}, timeout=20)
    return response


@allure.step("Найти id заказа по номеру трека")
def get_order_id_by_track(track) -> int:
    """В ответе на создание заказа возвращается только track, а не id.
    Общий список заказов (GET /orders) — это все заказы стенда с пагинацией,
    искать в нём ненадёжно: свежий заказ может просто не попасть на страницу.
    Поэтому ищем id через ручку поиска заказа по треку, дожидаясь индексации."""
    response = wait_for_order_by_track(track)
    return response.json()["order"]["id"]


@allure.step("Отменить заказ по треку")
def cancel_order(track) -> requests.Response:
    return requests.post(ORDERS_CANCEL_URL, params={"track": track}, timeout=20)


@allure.step("Принять заказ")
def accept_order(order_id, courier_id) -> requests.Response:
    """В документации есть неточность: id заказа и id курьера нужно
    передавать в параметрах запроса (query params), а не в теле."""
    return requests.put(f"{ORDERS_ACCEPT_URL}/{order_id}", params={"courierId": courier_id}, timeout=20)


@allure.step("Получить заказ по номеру трека (без ожидания индексации)")
def get_order_by_track(track) -> requests.Response:
    return requests.get(ORDERS_TRACK_URL, params={"t": track}, timeout=20)
