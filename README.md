# Synergy Case 4 WebApp

Минимальное веб-приложение в предметной области "Туризм" на базе FastAPI и PostgreSQL.
Проект реализует REST API для каталога туров и приема заявок.

## Содержание
- [Функциональность](#функциональность)
- [Технологический стек](#технологический-стек)
- [Архитектура](#архитектура)
- [Структура проекта](#структура-проекта)
- [Требования](#требования)
- [Запуск через Docker Compose](#запуск-через-docker-compose)
- [Полная очистка перед новой сборкой](#полная-очистка-перед-новой-сборкой)
- [Постоянное хранение данных локально](#постоянное-хранение-данных-локально)
- [Локальный запуск (без контейнера API)](#локальный-запуск-без-контейнера-api)
- [Переменные окружения](#переменные-окружения)
- [Проверка API](#проверка-api)
- [Остановка и сброс](#остановка-и-сброс)
- [Типовые проблемы](#типовые-проблемы)
- [Скриншоты и аналитика](#скриншоты-и-аналитика)

## Функциональность
- `GET /health` - проверка доступности сервиса.
- `GET /tours` - список активных туров.
- `POST /orders` - создание заявки на тур.
- `GET /orders` - список созданных заявок.
- OpenAPI документация из коробки: Swagger UI и ReDoc.

## Технологический стек
- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL 16 (alpine)
- Docker / Docker Compose

## Архитектура
Клиент (браузер / API-клиент) -> FastAPI -> PostgreSQL

База данных инициализируется SQL-скриптом `sql/init.sql` при первом запуске PostgreSQL (когда каталог данных пустой).

## Структура проекта
```text
Synergy_2s_Case_4_WebApp/
|-- app/
|   |-- main.py
|   |-- db.py
|   |-- models.py
|   |-- schemas.py
|   `-- routers/
|       |-- health.py
|       |-- tours.py
|       |-- orders.py
|       `-- ANALYSIS.md
|-- docs/
|   |-- db_schema.png
|   |-- health.png
|   |-- post_order.png
|   |-- swagger.png
|   `-- tours.png
|-- sql/
|   `-- init.sql
|-- .env.example
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

## Требования
- Docker Desktop (или Docker Engine + Docker Compose plugin)
- Для локального запуска: Python 3.12+

## Запуск через Docker Compose
Рекомендуемый способ запуска.

1. Перейдите в директорию проекта:
```powershell
cd F:\Synergy\2nd_Semester\Case_4_WebApp\Synergy_2s_Case_4_WebApp
```

2. Соберите и запустите сервисы:
```powershell
docker compose up --build
```

3. Откройте в браузере:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

## Полная очистка перед новой сборкой
Этот сценарий удаляет контейнеры, локально собранные образы и локальные данные PostgreSQL.

1. Остановить и удалить контейнеры + локальные образы compose-проекта:
```powershell
docker compose down --remove-orphans --rmi local
```

2. Удалить локальные данные БД из проекта:
```powershell
if (Test-Path .\.data\postgres) { Remove-Item -Recurse -Force .\.data\postgres }
```

3. Собрать и запустить заново:
```powershell
docker compose up --build
```

Важно: после удаления `./.data/postgres` база создается заново, и `sql/init.sql` выполняется как при первом старте.

## Постоянное хранение данных локально
Чтобы данные, внесенные через Swagger (`POST /orders`), сохранялись между пересозданиями контейнеров, PostgreSQL хранит файлы в локальной папке проекта:

- хост: `./.data/postgres`
- контейнер: `/var/lib/postgresql/data`

Это уже настроено в `docker-compose.yml`:
```yaml
services:
  db:
    volumes:
      - ./.data/postgres:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
```

Поведение:
- `docker compose down` -> данные сохраняются.
- `docker compose up` -> поднимается тот же набор данных.
- Полный сброс данных происходит только если удалить `./.data/postgres`.

## Локальный запуск (без контейнера API)
Этот вариант запускает PostgreSQL в Docker, а API - локально из Python.

1. Перейдите в директорию проекта:
```powershell
cd F:\Synergy\2nd_Semester\Case_4_WebApp\Synergy_2s_Case_4_WebApp
```

2. Создайте и активируйте виртуальное окружение:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Установите зависимости:
```powershell
pip install -r requirements.txt
```

4. Поднимите только PostgreSQL:
```powershell
docker compose up -d db
```

5. Задайте строку подключения к БД для локального API:
```powershell
$env:DATABASE_URL="postgresql+psycopg://tourism:tourism@localhost:5432/tourism"
```

6. Запустите API:
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Переменные окружения
Шаблон находится в `.env.example`.

Ключевые переменные:
- `DATABASE_URL` - строка подключения, которую использует приложение.
- `DOCKER_DATABASE_URL` - справочное значение для запуска внутри Docker-сети.
- `APP_HOST`, `APP_PORT`, `APP_ENV`, `LOG_LEVEL` - служебные настройки.

## Проверка API
### 1) Список туров
```powershell
curl.exe -s http://localhost:8000/tours
```

### 2) Создание заявки
```powershell
curl.exe -X POST "http://localhost:8000/orders" `
  -H "Content-Type: application/json" `
  -d '{"full_name":"Ivan Petrov","phone":"+79990001122","tour_id":1,"persons":2,"start_date":"2026-03-10"}'
```

### 3) Просмотр заявок
```powershell
curl.exe -s http://localhost:8000/orders
```

## Остановка и сброс
Остановить и удалить контейнеры:
```powershell
docker compose down
```

Остановить и удалить контейнеры + volumes Docker Compose:
```powershell
docker compose down -v
```

Примечание: bind mount `./.data/postgres` не удаляется командой `down -v`, потому что это папка хоста, а не именованный том Docker.

## Типовые проблемы
- Порт `8000` занят:
  измените проброс порта в `docker-compose.yml` или освободите порт.
- Порт `5432` занят:
  остановите локальный PostgreSQL или измените проброс порта БД.
- Данные "не сбрасываются" после `down -v`:
  удалите `./.data/postgres` вручную (см. раздел "Полная очистка перед новой сборкой").
- `ModuleNotFoundError` при локальном запуске:
  проверьте активацию `.venv` и выполните `pip install -r requirements.txt`.

## Скриншоты и аналитика
- Скриншоты API и схемы БД: папка `docs/`
- Аналитическая часть кейса: `app/routers/ANALYSIS.md`
