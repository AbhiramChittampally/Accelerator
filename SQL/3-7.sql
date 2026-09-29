/* Primary Key */
CREATE TABLE Employees
(
    employee_id INT PRIMARY KEY,
    email VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    status VARCHAR(20),
    created_at DATE
);

/* Single-column Index */
CREATE INDEX idx_email
ON Employees(email);

/* Composite Index */
CREATE INDEX idx_department_salary
ON Employees(department, salary);

/* Unique Index */
CREATE UNIQUE INDEX idx_email_unique
ON Employees(email);

/* Function-Based Index (database-specific syntax) */
CREATE INDEX idx_upper_name
ON Employees(UPPER(email));

/* Partial Index (PostgreSQL example) */
CREATE INDEX idx_active_emp
ON Employees(created_at)
WHERE status='Active';