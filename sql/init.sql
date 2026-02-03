CREATE TABLE IF NOT EXISTS tours (
  tour_id      BIGSERIAL PRIMARY KEY,
  tour_name    TEXT NOT NULL,
  country      TEXT NOT NULL,
  city         TEXT,
  nights       INT NOT NULL CHECK (nights > 0),
  base_price   NUMERIC(12,2) NOT NULL CHECK (base_price >= 0),
  is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
  order_id     BIGSERIAL PRIMARY KEY,
  full_name    TEXT NOT NULL,
  phone        TEXT NOT NULL,
  tour_id      BIGINT NOT NULL REFERENCES tours(tour_id),
  persons      INT NOT NULL CHECK (persons > 0),
  start_date   DATE NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO tours (tour_name, country, city, nights, base_price, is_active)
VALUES
('Римские каникулы', 'Италия', 'Рим', 7, 85000, TRUE),
('Море и солнце', 'Турция', 'Анталья', 10, 95000, TRUE)
ON CONFLICT DO NOTHING;
