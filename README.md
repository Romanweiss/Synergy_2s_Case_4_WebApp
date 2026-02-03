# Кейс-задача №4 — WEB-приложение (FastAPI + PostgreSQL)

## Описание
Минимальное WEB-приложение с клиент–серверной архитектурой на тему «Туризм».  
Реализован REST API для получения списка туров и создания заявки (заказа) на тур.

Проект выполнен в рамках учебной практики (кейс-задача №4).

## Используемые технологии
- Python 3.12
- FastAPI (ASGI)
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Docker / Docker Compose

## Функциональность API
- `GET /health` — проверка доступности сервиса
- `GET /tours` — получение списка активных туров
- `POST /orders` — создание заявки на тур

### Документация API (OpenAPI)
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Структура проекта
```

Case_4_WebApp/
├── app/
│   ├── main.py        # точка входа FastAPI
│   ├── db.py          # подключение к базе данных
│   ├── models.py      # ORM-модели SQLAlchemy
│   ├── schemas.py     # схемы Pydantic
│   └── routers/       # маршруты API
│
├── sql/
│   └── init.sql       # DDL и тестовые данные (инициализация БД)
│
├── docs/
│   ├── swagger.png    # Swagger UI
│   ├── health.png     # ответ /health
│   ├── tours.png      # ответ /tours
│   ├── db_schema.png  # структура БД (DBeaver)
│   └── post_order.png # создание заказа (опционально)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md

````

## Запуск через Docker Compose

1. Перейдите в каталог проекта:
```bash
cd Case_4_WebApp
````

2. Выполните сборку и запуск сервисов:

```bash
docker compose up --build
```

3. После запуска откройте в браузере:

* `http://localhost:8000/docs`
* `http://localhost:8000/health`
* `http://localhost:8000/tours`

## База данных

Структура базы данных создаётся автоматически при первом запуске контейнера PostgreSQL
на основе SQL-скрипта:

```
sql/init.sql
```

## Скриншоты

В папке `docs/` представлены:

* `swagger.png` — интерфейс Swagger UI
* `health.png` — результат запроса `/health`
* `tours.png` — результат запроса `/tours`
* `db_schema.png` — схема базы данных (DBeaver)
* `post_order.png` — пример создания заказа через Swagger (опционально)

