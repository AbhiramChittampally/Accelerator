USE fs;

EXPLAIN
SELECT
    name,
    price
FROM FoodItems
WHERE name = 'Chicken Biryani';

CREATE INDEX idx_food_cover
ON FoodItems(name, price);

EXPLAIN
SELECT
    name,
    price
FROM FoodItems
WHERE name = 'Chicken Biryani';

SELECT
    name,
    price
FROM FoodItems
WHERE name = 'Chicken Biryani';