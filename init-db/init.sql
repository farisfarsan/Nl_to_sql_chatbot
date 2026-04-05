-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2),
    stock INTEGER DEFAULT 0
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    total_price DECIMAL(10, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO users (name, email, city) VALUES
    ('Alice Johnson', 'alice@example.com', 'New York'),
    ('Bob Smith', 'bob@example.com', 'London'),
    ('Carol White', 'carol@example.com', 'Paris'),
    ('David Brown', 'david@example.com', 'New York'),
    ('Eva Green', 'eva@example.com', 'Tokyo');

-- Insert sample products
INSERT INTO products (name, category, price, stock) VALUES
    ('Laptop', 'Electronics', 999.99, 50),
    ('Smartphone', 'Electronics', 699.99, 100),
    ('Headphones', 'Electronics', 149.99, 200),
    ('Desk Chair', 'Furniture', 299.99, 30),
    ('Coffee Maker', 'Appliances', 89.99, 75),
    ('Python Book', 'Books', 39.99, 150),
    ('Monitor', 'Electronics', 399.99, 60);

-- Insert sample orders
INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES
    (1, 1, 1, 999.99),
    (1, 3, 2, 299.98),
    (2, 2, 1, 699.99),
    (3, 4, 1, 299.99),
    (4, 5, 2, 179.98),
    (5, 6, 3, 119.97),
    (2, 7, 1, 399.99),
    (3, 1, 1, 999.99),
    (4, 2, 2, 1399.98),
    (1, 6, 1, 39.99);
