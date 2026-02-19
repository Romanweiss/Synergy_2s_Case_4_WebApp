# Кейс-задача №4 — WEB-приложение «Туризм» (Python + FastAPI + PostgreSQL)

## Описание
В проекте реализовано учебное WEB-приложение в предметной области «Туризм».

Система построена по WEB-архитектуре:
- клиент (браузер / API-клиент);
- сервер приложений (FastAPI);
- база данных (PostgreSQL).

Проект включает:
- аналитический обзор рыночных WEB-систем (`CASE_5_ANALYTICAL_REVIEW.md`);
- рабочее WEB-приложение с REST API;
- SQL-скрипт структуры БД (`sql/init.sql`).

## Соответствие условию
Условие требует:
1. Анализ WEB-информационных систем на рынке и вариантов использования в компании.
2. Создание WEB-приложения.
3. Наличие SQL-описания структуры БД.

Выполнено:
- Аналитика оформлена в `CASE_5_ANALYTICAL_REVIEW.md`.
- WEB-приложение реализовано на Python (FastAPI).
- База данных реализована на PostgreSQL.
- SQL-скрипт инициализации и структуры находится в `sql/init.sql`.

Примечание: в формулировке кейса упомянуты Delphi/IIS/MySQL, но по вашему решению реализация выполнена на Python + PostgreSQL, что также корректно для демонстрации WEB-архитектуры.

## Функциональность API
- `GET /health` — проверка доступности API.
- `GET /tours` — список активных туров.
- `GET /services` — перечень дополнительных услуг.
- `POST /orders` — создание заявки на тур.
- `GET /orders` — список созданных заявок.

## Структура БД (PostgreSQL)
SQL-скрипт: `sql/init.sql`

Таблицы:
- `tours` — каталог туров.
- `services` — каталог услуг.
- `orders` — заявки клиентов.

Ключевые элементы:
- PK во всех таблицах (`tour_id`, `service_id`, `order_id`).
- FK: `orders.tour_id -> tours.tour_id`, `orders.service_id -> services.service_id`.
- Ограничения `CHECK` для бизнес-правил (`nights > 0`, `persons > 0`, `price/base_price >= 0`).

## Технологический стек
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker / Docker Compose

## Клонирование и запуск через Docker
SSH:
```powershell
git clone git@github.com:Romanweiss/Synergy_2s_Case_4_WebApp.git
cd Synergy_2s_Case_4_WebApp
docker compose up --build
```

HTTPS:
```powershell
git clone https://github.com/Romanweiss/Synergy_2s_Case_4_WebApp.git
cd Synergy_2s_Case_4_WebApp
docker compose up --build
```

После запуска:
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/health`

## Troubleshooting
Если проект запускался ранее на старой схеме БД и появляется ошибка вида
`column orders.service_id does not exist`, выполните полный пересоздание контейнеров и тома БД:

```powershell
docker compose down -v
docker compose up --build
```

## Проверка API
```powershell
curl.exe -s http://localhost:8000/tours
curl.exe -s http://localhost:8000/services
```

```powershell
curl.exe -X POST "http://localhost:8000/orders" `
  -H "Content-Type: application/json" `
  -d '{"full_name":"Ivan Petrov","phone":"+79990001122","tour_id":1,"service_id":1,"persons":2,"start_date":"2026-03-10"}'
```

```powershell
curl.exe -s http://localhost:8000/orders
```

## Состав проекта
- `app/` — исходный код FastAPI-приложения.
- `sql/init.sql` — SQL-скрипт структуры БД и стартовых данных.
- `CASE_5_ANALYTICAL_REVIEW.md` — аналитический обзор рыночных WEB-систем.
- `task_solution_description.txt` — подробное описание процесса решения (для отчёта).
- `docker-compose.yml`, `Dockerfile` — контейнеризация и запуск.
