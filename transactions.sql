CREATE TABLE transactions (
    transaction_id  SERIAL PRIMARY KEY,
    user_id         INT            NOT NULL,
    amount          DECIMAL(10, 2),
    created_at      TIMESTAMP      NOT NULL DEFAULT NOW()
);
 
INSERT INTO transactions (user_id, amount, created_at) VALUES
(1,  120.00, '2024-01-05 10:00:00'),
(2,   45.50, '2024-01-12 14:30:00'),
(3,   80.00, '2024-01-18 09:15:00'),
(1,   60.00, '2024-02-03 11:00:00'),
(4,  200.00, '2024-02-14 16:45:00'),
(2,   35.00, '2024-02-20 08:00:00'),
(3,  150.00, '2024-03-01 13:00:00'),
(5,   90.00, '2024-03-10 17:30:00'),
(1,  110.00, '2024-03-22 10:00:00'),
(4,   55.00, '2024-03-28 12:00:00'),
(2,    NULL, '2024-01-10 09:00:00'),
(1,  120.00, '2024-01-05 10:00:00');

--Given a transactions table with user_id, amount, created_at, write a query that returns total
--revenue and number of transactions per month, ordered by most recent month first.
SELECT DATE_TRUNC('month', created_at) AS month,SUM(amount) AS revenue, COUNT(amount) AS number_transactions 
    FROM transactions
    GROUP BY DATE_TRUNC('month', created_at) 
    ORDER BY month DESC

--Second exercise
CREATE TABLE purchases (
    purchase_id     SERIAL PRIMARY KEY,
    user_id         INT            NOT NULL,
    amount          DECIMAL(10, 2) NOT NULL,
    purchase_date   DATE           NOT NULL
);
 
INSERT INTO purchases (user_id, amount, purchase_date) VALUES
(1,  75.00, '2024-01-08'),
(2,  120.00, '2024-01-15'),
(3,  200.00, '2024-01-22'),
(1,  50.00, '2024-02-05'),   
(2,  90.00, '2024-02-18'),   
(4,  300.00, '2024-01-30'),  
(5,  60.00, '2024-02-10'),   
(3,  180.00, '2024-02-25');  

--Find all users who made a purchase in January and also made a purchase in February. Return their user_id and total spend in each month.
SELECT pur.user_id,
    SUM(CASE WHEN DATE_TRUNC('month', purchase_date) = '2024-01-01' THEN 1 ELSE 0 END) AS january_spending,
    SUM(CASE WHEN DATE_TRUNC('month', purchase_date) = '2024-02-01' THEN 1 ELSE 0 END) AS february_spending
    FROM purchases pur
GROUP BY pur.user_id
HAVING 
    SUM(CASE WHEN DATE_TRUNC('month', purchase_date) = '2024-01-01' THEN 1 ELSE 0 END) > 0
    AND
    SUM(CASE WHEN DATE_TRUNC('month', purchase_date) = '2024-02-01' THEN 1 ELSE 0 END) > 0;

--Third exercise
CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    user_id     INT            NOT NULL,
    amount      DECIMAL(10, 2) NOT NULL,
    order_date  DATE           NOT NULL
);
 
INSERT INTO orders (user_id, amount, order_date) VALUES
(1,  50.00, '2024-01-03'),
(1, 200.00, '2024-01-17'),
(1,  80.00, '2024-02-05'),
(2, 150.00, '2024-01-10'),
(2,  40.00, '2024-01-25'),
(2, 300.00, '2024-02-12'),
(3, 100.00, '2024-01-08'),
(3,  60.00, '2024-02-20'),
(3, 250.00, '2024-03-01');

--From an orders table, return each order with a running total of revenue per user, and rank each user's orders from largest to smallest amount.
SELECT user_id, amount, order_date, 
    SUM(amount) OVER(PARTITION BY user_id ORDER BY order_date) as running_total,
    RANK() OVER(PARTITION BY user_id ORDER BY amount DESC) as rank 
FROM orders
ORDER BY user_id, order_date

--Fourth exercise
CREATE TABLE customers (
    id          SERIAL PRIMARY KEY,
    email       VARCHAR(255)   NOT NULL,
    full_name   VARCHAR(255),
    created_at  TIMESTAMP      NOT NULL DEFAULT NOW()
);
 
INSERT INTO customers (email, full_name, created_at) VALUES
('alice@email.com',   'Alice Johnson',  '2024-01-01 08:00:00'),
('bob@email.com',     'Bob Smith',      '2024-01-02 09:00:00'),
('alice@email.com',   'Alice J.',       '2024-01-15 10:00:00'),  
('carol@email.com',   'Carol White',    '2024-01-18 11:00:00'),
('bob@email.com',     'Robert Smith',   '2024-02-01 12:00:00'),  
('dave@email.com',    'Dave Brown',     '2024-02-10 13:00:00'),
('alice@email.com',   'A. Johnson',     '2024-03-05 14:00:00'),  
('eve@email.com',     'Eve Davis',      '2024-03-12 15:00:00');
--Given a customers table, find all email addresses that appear more than once, and return the email along with how many times it appears.
SELECT email, COUNT(email) AS appearences FROM customers
GROUP BY email
HAVING COUNT(email)>1