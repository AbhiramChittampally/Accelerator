CREATE DATABASE IF NOT EXISTS fs;
USE fs;

-- Customers
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT PRIMARY KEY,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    email       VARCHAR(100),
    phone       VARCHAR(15),
    address     VARCHAR(100)
);

INSERT INTO Customers VALUES
(1, 'Amit',  'Sharma', 'amit.sharma@gmail.com',  '9876543210', 'Delhi, India'),
(2, 'Priya', 'Singh',  'priya.singh@yahoo.com',  '8765432109', 'Mumbai, India'),
(3, 'Rahul', 'Verma',  'rahul.verma@gmail.com',  '7654321098', 'Bengaluru, India'),
(4, 'Neha',  'Patel',  'neha.patel@yahoo.com',   '6543210987', 'Ahmedabad, India'),
(5, 'Arjun', 'Gupta',  'arjun.gupta@gmail.com',  '9876501234', 'Hyderabad, India');

-- FoodItems
CREATE TABLE IF NOT EXISTS FoodItems (
    food_id      INT PRIMARY KEY,
    name         VARCHAR(100),
    description  VARCHAR(255),
    price        DECIMAL(8,2),
    category     VARCHAR(50),
    availability TINYINT(1)
);

INSERT INTO FoodItems VALUES
(1,  'Paneer Butter Masala', 'Rich creamy gravy with cottage cheese.',                   250.00, 'Main Course', 1),
(2,  'Chicken Biryani',      'Aromatic basmati rice cooked with chicken and spices.',    300.00, 'Main Course', 1),
(3,  'Masala Dosa',          'Crispy dosa with spicy potato filling.',                   120.00, 'Breakfast',   1),
(4,  'Samosa',               'Fried pastry with spicy potato filling.',                   30.00, 'Snacks',      1),
(5,  'Gulab Jamun',          'Sweet dessert balls soaked in sugar syrup.',                50.00, 'Desserts',    1),
(6,  'Butter Naan',          'Indian bread cooked in tandoor.',                           40.00, 'Breads',      1),
(7,  'Dal Tadka',            'Tempered lentils cooked with spices.',                     150.00, 'Main Course', 1),
(8,  'Chole Bhature',        'Spicy chickpea curry served with fried bread.',            100.00, 'Breakfast',   1),
(9,  'Veg Fried Rice',       'Rice stir-fried with veggies.',                            130.00, 'Main Course', 1),
(10, 'Mango Lassi',          'Sweet yogurt-based mango drink.',                           60.00, 'Beverages',   1);

-- Orders
CREATE TABLE IF NOT EXISTS Orders (
    order_id     INT PRIMARY KEY,
    customer_id  INT,
    food_id      INT,
    quantity     INT,
    order_date   DATETIME,
    status       VARCHAR(20),
    total_amount DECIMAL(8,2),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (food_id)     REFERENCES FoodItems(food_id)
);

INSERT INTO Orders VALUES
(1,  1, 2,  1, '2026-06-17 11:17:55', 'Delivered', 300.00),
(2,  1, 5,  3, '2026-06-17 11:17:55', 'Delivered', 150.00),
(3,  1, 6,  2, '2026-06-17 11:17:55', 'Delivered',  80.00),
(4,  2, 3,  2, '2026-06-17 11:17:55', 'Preparing', 240.00),
(5,  2, 10, 1, '2026-06-17 11:17:55', 'Preparing',  60.00),
(6,  2, 4,  4, '2026-06-17 11:17:55', 'Delivered', 120.00),
(7,  3, 1,  1, '2026-06-17 11:17:55', 'Cancelled', 250.00),
(8,  3, 7,  2, '2026-06-17 11:17:55', 'Delivered', 300.00),
(9,  3, 9,  1, '2026-06-17 11:17:55', 'Delivered', 130.00),
(10, 4, 8,  1, '2026-06-17 11:17:55', 'Pending',   100.00),
(11, 4, 2,  2, '2026-06-17 11:17:55', 'Pending',   600.00),
(12, 4, 5,  4, '2026-06-17 11:17:55', 'Preparing', 200.00),
(13, 4, 10, 2, '2026-06-17 11:17:55', 'Preparing', 120.00),
(14, 5, 3,  3, '2026-06-17 11:17:55', 'Delivered', 360.00),
(15, 5, 4,  5, '2026-06-17 11:17:55', 'Delivered', 150.00),
(16, 5, 6,  4, '2026-06-17 11:17:55', 'Delivered', 160.00),
(17, 5, 1,  1, '2026-06-17 11:17:55', 'Preparing', 250.00),
(18, 1, 8,  2, '2026-06-17 11:17:55', 'Delivered', 200.00),
(19, 2, 9,  2, '2026-06-17 11:17:55', 'Pending',   260.00),
(20, 3, 10, 3, '2026-06-17 11:17:55', 'Delivered', 180.00);

-- dept
CREATE TABLE IF NOT EXISTS dept (
    deptno   INT PRIMARY KEY,
    dname    VARCHAR(50),
    location VARCHAR(50)
);

INSERT INTO dept VALUES
(10, 'Accounting', 'New York'),
(20, 'Research',   'Dallas'),
(30, 'Sales',      'Chicago'),
(40, 'Operations', 'Boston'),
(50, 'Finance',    'Tempe');

-- emp
CREATE TABLE IF NOT EXISTS emp (
    empno    INT PRIMARY KEY,
    ename    VARCHAR(50),
    job      VARCHAR(20),
    mgr      INT,
    hiredate DATE,
    sal      DECIMAL(8,2),
    comm     DECIMAL(8,2),
    deptno   INT,
    FOREIGN KEY (deptno) REFERENCES dept(deptno)
);

INSERT INTO emp VALUES
(7369, 'SMITH',  'CLERK',     7902, '1993-06-13', 800.00,  0.00,    20),
(7499, 'ALLEN',  'SALESMAN',  7698, '1998-08-15', 1600.00, 300.00,  10),
(7521, 'ALLEN',  'SALESMAN',  7698, '1996-03-26', 1250.00, 500.00,  30),
(7566, 'JONES',  'MANAGER',   7839, '1995-10-31', 2975.00, NULL,    20),
(7654, 'MARTIN', 'SALESMAN',  7698, '1998-12-05', 1250.00, 1400.00, 40),
(7698, 'BLAKE',  'MANAGER',   7839, '1992-06-11', 2850.00, NULL,    30),
(7782, 'CLARK',  'MANAGER',   7839, '1993-05-14', 2450.00, NULL,    10),
(7788, 'SCOTT',  'ANALYST',   7566, '1996-03-05', 3000.00, NULL,    20),
(7839, 'KEVIN',  'PRESIDENT', NULL, '1990-06-09', 5000.00, 0.00,    40),
(7844, 'KEVIN',  'SALESMAN',  7698, '1995-06-04', 1500.00, 0.00,    30),
(7876, 'KEVIN',  'CLERK',     7788, '1999-06-01', 100.00,  NULL,    20),
(7900, 'JAMES',  'CLERK',     7698, '2000-06-23', 950.00,  NULL,    20),
(7902, 'FORD',   'ANALYST',   7566, '1997-12-05', 3000.00, NULL,    20),
(7934, 'FORD',   'CLERK',     7782, '2000-01-21', 1300.00, NULL,    10);

-- salgrade
CREATE TABLE IF NOT EXISTS salgrade (
    grade INT PRIMARY KEY,
    losal DECIMAL(8,2),
    hisal DECIMAL(8,2)
);

INSERT INTO salgrade VALUES
(1, 700.00,  2222.00),
(2, 1201.00, 3333.00),
(3, 1401.00, 4444.00),
(4, 2001.00, 5555.00),
(5, 3001.00, 6666.00),
(6, 4001.00, 8888.00);
