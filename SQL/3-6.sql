/*=========================================================
    PARENT TABLE
=========================================================*/

CREATE TABLE Customers
(
    customer_id INT AUTO_INCREMENT,

    customer_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE,

    phone VARCHAR(15) UNIQUE,

    age INT,

    city VARCHAR(50) DEFAULT 'Hyderabad',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_customers
        PRIMARY KEY (customer_id),

    CONSTRAINT chk_customer_age
        CHECK (age >= 18)
);



/*=========================================================
    SECOND PARENT TABLE
=========================================================*/

CREATE TABLE Products
(
    product_id INT AUTO_INCREMENT,

    product_name VARCHAR(100) NOT NULL,

    category VARCHAR(50) NOT NULL,

    price DECIMAL(10,2) NOT NULL,

    stock_qty INT DEFAULT 0,

    status VARCHAR(20) DEFAULT 'Available',

    CONSTRAINT pk_products
        PRIMARY KEY(product_id),

    CONSTRAINT chk_price
        CHECK(price > 0),

    CONSTRAINT chk_stock
        CHECK(stock_qty >= 0)
);



/*=========================================================
    CHILD TABLE
=========================================================*/

CREATE TABLE Orders
(
    order_id INT AUTO_INCREMENT,

    customer_id INT NOT NULL,

    order_date DATE DEFAULT CURRENT_DATE,

    total_amount DECIMAL(10,2) DEFAULT 0,

    status VARCHAR(20) DEFAULT 'Pending',

    CONSTRAINT pk_orders
        PRIMARY KEY(order_id),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY(customer_id)
        REFERENCES Customers(customer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_total
        CHECK(total_amount >= 0)
);



/*=========================================================
    BRIDGE TABLE
    (Composite Primary Key)
=========================================================*/

CREATE TABLE OrderItems
(
    order_id INT,

    product_id INT,

    quantity INT NOT NULL DEFAULT 1,

    unit_price DECIMAL(10,2) NOT NULL,

    CONSTRAINT pk_order_items
        PRIMARY KEY(order_id, product_id),

    CONSTRAINT fk_orderitems_order
        FOREIGN KEY(order_id)
        REFERENCES Orders(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_orderitems_product
        FOREIGN KEY(product_id)
        REFERENCES Products(product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_quantity
        CHECK(quantity > 0),

    CONSTRAINT chk_unit_price
        CHECK(unit_price > 0)
);