CREATE TABLE users (
    user_id     SERIAL PRIMARY KEY,
    email       VARCHAR(100) NOT NULL UNIQUE,
    full_name   VARCHAR(100) NOT NULL,
    status      VARCHAR(20)  NOT NULL DEFAULT 'active', -- active, suspended, churned
    signup_date DATE         NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE merchants (
    merchant_id SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    category    VARCHAR(50),  -- e.g. 'fashion', 'electronics', 'beauty'
    country     VARCHAR(50)  DEFAULT 'US'
);

CREATE TABLE orders (
    order_id     SERIAL PRIMARY KEY,
    user_id      INT          NOT NULL REFERENCES users(user_id),
    status       VARCHAR(20)  NOT NULL DEFAULT 'pending', -- pending, completed, cancelled, refunded
    total_amount DECIMAL(10,2) NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
    item_id      SERIAL PRIMARY KEY,
    order_id     INT           NOT NULL REFERENCES orders(order_id),
    merchant_id  INT           NOT NULL REFERENCES merchants(merchant_id),
    product_name VARCHAR(150)  NOT NULL,
    price        DECIMAL(10,2) NOT NULL,
    quantity     INT           NOT NULL DEFAULT 1
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id   INT           NOT NULL REFERENCES orders(order_id),
    user_id    INT           NOT NULL REFERENCES users(user_id),
    method     VARCHAR(30)   NOT NULL, -- 'installment', 'full', 'refund'
    amount     DECIMAL(10,2) NOT NULL,
    status     VARCHAR(20)   NOT NULL DEFAULT 'pending', -- pending, approved, declined, refunded
    paid_at    TIMESTAMP     DEFAULT NOW()
);

-- SAMPLE DATA


INSERT INTO users (email, full_name, status, signup_date) VALUES
('ana.gomez@gmail.com',    'Ana Gómez',      'active',    '2023-01-15'),
('carlos.r@hotmail.com',   'Carlos Ríos',    'active',    '2023-03-20'),
('maria.p@outlook.com',    'María Peña',     'churned',   '2022-11-05'),
('john.doe@gmail.com',     'John Doe',       'active',    '2024-01-10'),
('sara.k@gmail.com',       'Sara Kim',       'suspended', '2023-07-22'),
('luis.m@gmail.com',       'Luis Mora',      'active',    '2024-02-18'),
('patricia.n@yahoo.com',   'Patricia Núñez', 'active',    '2023-09-01'),
('david.w@gmail.com',      'David Wu',       'active',    '2023-06-14');

INSERT INTO merchants (name, category, country) VALUES
('Urban Outfitters',  'fashion',     'US'),
('TechZone',          'electronics', 'US'),
('GlowUp Beauty',     'beauty',      'US'),
('Sneaker Palace',    'fashion',     'US'),
('HomeGoods Co.',     'home',        'US');

INSERT INTO orders (user_id, status, total_amount, created_at) VALUES
(1, 'completed',  120.00, NOW() - INTERVAL '5 days'),
(1, 'completed',  250.50, NOW() - INTERVAL '20 days'),
(2, 'completed',   89.99, NOW() - INTERVAL '3 days'),
(2, 'cancelled',   45.00, NOW() - INTERVAL '10 days'),
(3, 'completed',  300.00, NOW() - INTERVAL '40 days'),
(4, 'completed',  199.00, NOW() - INTERVAL '2 days'),
(4, 'completed',  310.00, NOW() - INTERVAL '8 days'),
(4, 'completed',   75.50, NOW() - INTERVAL '15 days'),
(6, 'completed',  415.00, NOW() - INTERVAL '1 day'),
(7, 'completed',   60.00, NOW() - INTERVAL '6 days'),
(7, 'refunded',    95.00, NOW() - INTERVAL '12 days'),
(8, 'completed',  505.00, NOW() - INTERVAL '4 days');

INSERT INTO order_items (order_id, merchant_id, product_name, price, quantity) VALUES
(1,  1, 'Linen Blazer',         60.00, 1),
(1,  3, 'Vitamin C Serum',      60.00, 1),
(2,  4, 'Air Force 1 Shoes',   125.25, 2),
(3,  2, 'Wireless Earbuds',     89.99, 1),
(5,  1, 'Winter Jacket',       150.00, 1),
(5,  5, 'Throw Pillow Set',    150.00, 1),
(6,  2, 'Mechanical Keyboard', 199.00, 1),
(7,  4, 'Jordan 1 Retro',      155.00, 2),
(8,  1, 'Denim Jeans',          75.50, 1),
(9,  2, 'Gaming Monitor',      415.00, 1),
(10, 3, 'Face Moisturizer',     60.00, 1),
(12, 2, 'Laptop Stand',        100.00, 1),
(12, 2, 'USB-C Hub',           105.00, 2),
(12, 4, 'New Balance 550',     195.00, 1);

INSERT INTO payments (order_id, user_id, method, amount, status, paid_at) VALUES
(1,  1, 'installment', 120.00, 'approved',  NOW() - INTERVAL '5 days'),
(2,  1, 'installment', 250.50, 'approved',  NOW() - INTERVAL '20 days'),
(3,  2, 'full',         89.99, 'approved',  NOW() - INTERVAL '3 days'),
(5,  3, 'full',        300.00, 'approved',  NOW() - INTERVAL '40 days'),
(6,  4, 'installment', 199.00, 'approved',  NOW() - INTERVAL '2 days'),
(7,  4, 'installment', 310.00, 'approved',  NOW() - INTERVAL '8 days'),
(8,  4, 'full',         75.50, 'approved',  NOW() - INTERVAL '15 days'),
(9,  6, 'installment', 415.00, 'approved',  NOW() - INTERVAL '1 day'),
(10, 7, 'full',         60.00, 'approved',  NOW() - INTERVAL '6 days'),
(11, 7, 'full',         95.00, 'refunded',  NOW() - INTERVAL '12 days'),
(12, 8, 'installment', 505.00, 'approved',  NOW() - INTERVAL '4 days');

-- Exercise 1 :You have a table orders(order_id, user_id, amount, status, created_at).
--Write a query to find the total amount spent per user, only for orders with status 'completed', and return the top 5 spenders.
SELECT user_id,SUM(total_amount) total_spent
    FROM orders
    WHERE status='completed' 
    GROUP BY user_id
    ORDER BY total_spent DESC
    LIMIT 5;

-- Exercise 2: Given users(user_id, name, signup_date) and orders(order_id, user_id, amount, created_at), 
--find all users who have never placed an order.
SELECT usr.full_name, usr.user_id FROM users usr
    LEFT JOIN orders ord ON ord.user_id=usr.user_id
    GROUP BY usr.user_id, usr.full_name
    HAVING COUNT(order_id)=0

-- Exercise 3: Using the orders table, rank each user's orders by amount (highest first) and return only each user's most expensive order.
WITH rk AS
	(SELECT user_id, order_id ,total_amount
	RANK() OVER(PARTITION BY user_id ORDER BY total_amount) AS highest_order
	FROM orders)
SELECT * FROM rk WHERE rk.highest_order=1

-- Exercise 4:Find all users who placed more than 3 orders in the last 30 days and whose average order value exceeds $50.
SELECT usr.full_name, usr.user_id,AVG(ord.total_amount) avg_order FROM users usr
    JOIN orders ord ON ord.user_id=usr.user_id
    WHERE ord.created_at >= NOW() - INTERVAL '30 days'
    GROUP BY ord.user_id
    HAVING AVG(ord.total_amount)>=50 AND COUNT(ord.order_id) > 3