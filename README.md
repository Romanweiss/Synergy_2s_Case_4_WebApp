```md
# Кейс-задача №4 — WEB-приложение (FastAPI + PostgreSQL)

## Описание

Минимальное WEB-приложение с клиент–серверной архитектурой на тему «Туризм».

Система реализует базовый функционал туристической компании:
- каталог туров;
- приём заявок на тур;
- хранение данных в реляционной базе данных;
- документированное REST API.

Проект выполнен в рамках учебной практики (кейс-задача №4).

---

## Используемые технологии

- Python 3.12  
- FastAPI (ASGI)  
- Uvicorn  
- PostgreSQL  
- SQLAlchemy  
- Pydantic  
- Docker / Docker Compose  

---

## Архитектура

Проект построен по клиент–серверной WEB-архитектуре:

```

Браузер / Swagger → FastAPI (API) → PostgreSQL

````

- FastAPI реализует бизнес-логику и REST API.
- PostgreSQL хранит данные (туры и заявки).
- Docker Compose обеспечивает развертывание сервисов.

---

## Функциональность API

### Основные эндпойнты:

- `GET /health` — проверка доступности сервиса  
- `GET /tours` — получение списка активных туров  
- `POST /orders` — создание заявки на тур  
- `GET /orders` — получение списка созданных заявок  

---

## Пример создания заявки

### Запрос:

```http
POST /orders
Content-Type: application/json
````

```json
{
  "full_name": "Иван Петров",
  "phone": "+79990001122",
  "tour_id": 1,
  "persons": 2,
  "start_date": "2026-03-10"
}
```

### Ответ:

```json
{
  "order_id": 3,
  "full_name": "Иван Петров",
  "phone": "+79990001122",
  "tour_id": 1,
  "persons": 2,
  "start_date": "2026-03-10",
  "created_at": "2026-02-17T12:40:12.123456"
}
```

---

## Документация API (OpenAPI)

FastAPI автоматически генерирует документацию:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Swagger используется для тестирования запросов без отдельного фронтенда.

---

## Структура базы данных

В системе реализованы две основные таблицы:

### Таблица `tours` (справочник)

Содержит:

* название тура
* страну
* город
* длительность (`nights`)
* базовую стоимость
* признак активности (`is_active`)

### Таблица `orders` (переменная информация)

Содержит:

* данные клиента
* ссылку на тур (внешний ключ)
* количество человек
* дату начала тура
* дату создания заявки

Связь реализована через внешний ключ:

```
orders.tour_id → tours.tour_id
```

---

## Структура проекта

```
Case_4_WebApp/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│
├── sql/
│   └── init.sql
│
├── docs/
│   ├── swagger.png
│   ├── health.png
│   ├── tours.png
│   ├── db_schema.png
│   ├── post_order.png
│   └── orders.png
│
├── ANALYSIS.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

---

## Запуск через Docker Compose

1. Перейдите в каталог проекта:

```bash
cd Case_4_WebApp
```

2. Выполните сборку и запуск:

```bash
docker compose up --build
```

3. После запуска откройте в браузере:

* [http://localhost:8000/docs](http://localhost:8000/docs)
* [http://localhost:8000/health](http://localhost:8000/health)
* [http://localhost:8000/tours](http://localhost:8000/tours)
* [http://localhost:8000/orders](http://localhost:8000/orders)

---

## Перезапуск базы данных (при необходимости)

Если требуется заново выполнить `init.sql`:

```bash
docker compose down -v
docker compose up --build
```

Флаг `-v` удаляет volume PostgreSQL.

---

## База данных

Структура БД создаётся автоматически при первом запуске контейнера
на основе файла:

```
sql/init.sql
```

---

## Скриншоты

В папке `docs/` представлены:

* `swagger.png` — Swagger UI
* `health.png` — ответ `/health`
* `tours.png` — список туров
* `post_order.png` — создание заявки
* `orders.png` — список заявок
* `db_schema.png` — структура базы данных (DBeaver)

---

## Аналитическая часть

Анализ рынка WEB-информационных систем в сфере туризма
представлен в отдельном файле:

```
ANALYSIS.md
```

---

## Соответствие требованиям задания

В рамках кейс-задачи выполнено:

* разработано WEB-приложение;
* реализована клиент–серверная архитектура;
* использована реляционная СУБД;
* реализованы первичные и внешние ключи;
* подготовлен SQL-скрипт создания структуры БД;
* создан репозиторий GitHub с кодом проекта.
