CREATE TABLE IF NOT EXISTS tours (
  tour_id      BIGSERIAL PRIMARY KEY,
  tour_name    TEXT NOT NULL UNIQUE,
  country      TEXT NOT NULL,
  city         TEXT,
  nights       INT NOT NULL CHECK (nights > 0),
  base_price   NUMERIC(12,2) NOT NULL CHECK (base_price >= 0),
  is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS services (
  service_id   BIGSERIAL PRIMARY KEY,
  service_name TEXT NOT NULL UNIQUE,
  price        NUMERIC(12,2) NOT NULL CHECK (price >= 0),
  is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
  order_id     BIGSERIAL PRIMARY KEY,
  full_name    TEXT NOT NULL,
  phone        TEXT NOT NULL,
  tour_id      BIGINT NOT NULL REFERENCES tours(tour_id),
  service_id   BIGINT REFERENCES services(service_id),
  persons      INT NOT NULL CHECK (persons > 0),
  start_date   DATE NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_orders_tour_id ON orders(tour_id);
CREATE INDEX IF NOT EXISTS idx_orders_service_id ON orders(service_id);
CREATE INDEX IF NOT EXISTS idx_orders_start_date ON orders(start_date);

INSERT INTO tours (tour_name, country, city, nights, base_price, is_active)
VALUES
('Roman Holidays', 'Italy', 'Rome', 7, 85000, TRUE),
('Sea and Sun', 'Turkey', 'Antalya', 10, 95000, TRUE)
ON CONFLICT (tour_name) DO NOTHING;

INSERT INTO services (service_name, price, is_active)
VALUES
('Insurance', 2500, TRUE),
('Airport Transfer', 1800, TRUE),
('Guided City Tour', 3200, TRUE)
ON CONFLICT (service_name) DO NOTHING;
