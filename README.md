# Sprint_7 — тестирование API «Яндекс.Самокат»

Автотесты для API учебного сервиса **Яндекс.Самокат**.

- Документация API: https://qa-scooter.praktikum-services.ru/docs/
- Базовый URL: https://qa-scooter.praktikum-services.ru

## Что покрыто тестами

Основное задание:
- `tests/test_create_courier.py` — создание курьера (`POST /api/v1/courier`)
- `tests/test_login_courier.py` — логин курьера (`POST /api/v1/courier/login`)
- `tests/test_create_order.py` — создание заказа (`POST /api/v1/orders`), с параметризацией по цвету
- `tests/test_list_orders.py` — список заказов (`GET /api/v1/orders`)

Дополнительное задание:
- `tests/test_delete_courier.py` — удаление курьера (`DELETE /api/v1/courier/{id}`)
- `tests/test_accept_order.py` — принять заказ (`PUT /api/v1/orders/accept/{id}`)
- `tests/test_get_order_by_track.py` — получить заказ по номеру (`GET /api/v1/orders/track`)

Каждая ручка вынесена в отдельный тестовый класс. Все тесты независимы:
тестовые данные (курьер, заказ) создаются в фикстурах перед тестом и
удаляются после него — см. `tests/conftest.py`.

## Установка

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Для генерации HTML-отчёта дополнительно нужен Allure Commandline
(https://allurereport.org/docs/install/) — например, через Homebrew:

```bash
brew install allure
```

или через Scoop на Windows:

```bash
scoop install allure
```

## Запуск тестов

```bash
pytest
```

Результаты в формате Allure сохранятся в `reports/allure-results`
(путь задан в `pytest.ini`).

Запустить только основное задание:

```bash
pytest tests/test_create_courier.py tests/test_login_courier.py tests/test_create_order.py tests/test_list_orders.py
```

## Генерация Allure-отчёта

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

В репозиторий по условиям задания пушится только папка `reports/allure-report`
(сырые результаты `reports/allure-results` в git не попадают — см. `.gitignore`).

## Структура проекта

```
Sprint_7/
├── pytest.ini
├── requirements.txt
├── README.md
├── utils/
│   ├── urls.py         # адреса ручек API
│   └── helpers.py       # генерация данных и обёртки над запросами
├── tests/
│   ├── conftest.py                  # фикстуры: courier_data, registered_courier, order_track
│   ├── test_create_courier.py
│   ├── test_login_courier.py
│   ├── test_create_order.py
│   ├── test_list_orders.py
│   ├── test_delete_courier.py
│   ├── test_accept_order.py
│   └── test_get_order_by_track.py
└── reports/
    └── allure-report/    # генерируется командой allure generate, пушится в git
```

## Примечание к дополнительному заданию

В документации есть неточность: при отмене и принятии заказа id/track нужно
передавать не в теле запроса, а в параметрах запроса (query params), например:

```
PUT /api/v1/orders/accept/{id}?courierId=...
POST /api/v1/orders/cancel?track=...
```

Это учтено в `utils/helpers.py` и в `tests/test_accept_order.py`.

---
Проект сдан на ревью.
