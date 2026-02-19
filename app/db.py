import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://tourism:tourism@db:5432/tourism"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def _wait_for_db(max_attempts: int = 30, delay_seconds: float = 1.0) -> None:
    last_error: Exception | None = None
    for _ in range(max_attempts):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as exc:  # pragma: no cover - startup infra dependency
            last_error = exc
            time.sleep(delay_seconds)

    if last_error:
        raise last_error


def run_startup_migrations() -> None:
    _wait_for_db()

    statements = (
        """
        CREATE TABLE IF NOT EXISTS services (
          service_id   BIGSERIAL PRIMARY KEY,
          service_name TEXT NOT NULL UNIQUE,
          price        NUMERIC(12,2) NOT NULL CHECK (price >= 0),
          is_active    BOOLEAN NOT NULL DEFAULT TRUE
        );
        """,
        """
        DO $$
        BEGIN
          IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'orders'
          ) THEN
            ALTER TABLE orders
              ADD COLUMN IF NOT EXISTS service_id BIGINT;
          END IF;
        END $$;
        """,
        """
        DO $$
        BEGIN
          IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'orders'
          ) AND EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'services'
          ) AND NOT EXISTS (
            SELECT 1
            FROM pg_constraint
            WHERE conname = 'fk_orders_service_id'
          ) THEN
            ALTER TABLE orders
              ADD CONSTRAINT fk_orders_service_id
              FOREIGN KEY (service_id) REFERENCES services(service_id);
          END IF;
        END $$;
        """,
        """
        DO $$
        BEGIN
          IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'orders'
          ) THEN
            EXECUTE 'CREATE INDEX IF NOT EXISTS idx_orders_service_id ON orders(service_id)';
          END IF;
        END $$;
        """,
        """
        INSERT INTO services (service_name, price, is_active)
        SELECT 'Insurance', 2500, TRUE
        WHERE NOT EXISTS (
          SELECT 1 FROM services WHERE service_name = 'Insurance'
        );
        """,
        """
        INSERT INTO services (service_name, price, is_active)
        SELECT 'Airport Transfer', 1800, TRUE
        WHERE NOT EXISTS (
          SELECT 1 FROM services WHERE service_name = 'Airport Transfer'
        );
        """,
        """
        INSERT INTO services (service_name, price, is_active)
        SELECT 'Guided City Tour', 3200, TRUE
        WHERE NOT EXISTS (
          SELECT 1 FROM services WHERE service_name = 'Guided City Tour'
        );
        """,
    )

    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
