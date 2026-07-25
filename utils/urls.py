"""Константы с адресами ручек API учебного сервиса «Яндекс.Самокат»."""

BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Курьеры
COURIER_URL = f"{BASE_URL}/api/v1/courier"
COURIER_LOGIN_URL = f"{COURIER_URL}/login"

# Заказы
ORDERS_URL = f"{BASE_URL}/api/v1/orders"
ORDERS_CANCEL_URL = f"{ORDERS_URL}/cancel"
ORDERS_ACCEPT_URL = f"{ORDERS_URL}/accept"
ORDERS_TRACK_URL = f"{ORDERS_URL}/track"
