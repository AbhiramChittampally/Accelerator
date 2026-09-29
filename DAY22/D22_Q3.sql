USE fs;

EXPLAIN
SELECT *
FROM FoodItems
WHERE category = 'Main Course';

CREATE INDEX idx_category
ON FoodItems(category);

EXPLAIN
SELECT *
FROM FoodItems
WHERE category = 'Main Course';

SELECT *
FROM FoodItems
WHERE category = 'Main Course';