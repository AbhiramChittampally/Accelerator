/*
Problem 5: Simple View Data Modification Rules 
-------------------------------------------------
Scenario: Developers want to update menu item availability from a 
simple interface without letting editors touch raw tables.

The Task: Create a simple view v_menu_availability on FoodItems. 
Demonstrate that this view is updatable by modifying a value directly
through the view, and explain the rules governing updatable views to
your students.

Expected output:
---------------
+---------+-------------+--------------+
| food_id | name        | availability |
+---------+-------------+--------------+
|       3 | Masala Dosa |            0 |
+---------+-------------+--------------+

*/
USE fs;

CREATE VIEW v_menu_availability AS
SELECT
    food_id,
    name,
    availability
FROM FoodItems;

UPDATE v_menu_availability
SET availability = 0
WHERE food_id = 3;

SELECT * 
FROM v_menu_availability
WHERE food_id = 3;