/*Problem 2: Dynamic Menu Pricing Tier View 
-----------------------------------------
Scenario: The kitchen needs a quick-reference dashboard that 
automatically categorizes food items into different business segments
based on their current pricing.

The Task: Create a view named v_menu_segments that displays food_id,
name, price, category, and a calculated column named pricing_tier.
If the price is above 200, label it 'Premium'; 
if between 100 and 200, label it 'Standard';
otherwise, label it 'Budget'.


Expected output:
---------------
+---------+----------------------+--------+--------------+
| food_id | name                 | price  | pricing_tier |
+---------+----------------------+--------+--------------+
|       1 | Paneer Butter Masala | 250.00 | Premium      |
|       2 | Chicken Biryani      | 300.00 | Premium      |
|       3 | Masala Dosa          | 120.00 | Standard     |
|       4 | Samosa               |  30.00 | Budget       |
|       5 | Gulab Jamun          |  50.00 | Budget       |
+---------+----------------------+--------+--------------+


*/
USE fs;

CREATE VIEW v_menu_segments AS
SELECT
    food_id,
    name,
    price,
    category,
    CASE
        WHEN price > 200 THEN 'Premium'
        WHEN price BETWEEN 100 AND 200 THEN 'Standard'
        ELSE 'Budget'
    END AS pricing_tier
FROM FoodItems;