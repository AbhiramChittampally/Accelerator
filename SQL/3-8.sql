-- | Plan Node / Metric     | Meaning                        | Good or Bad?                                                                     |
-- | ---------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
-- | Seq Scan               | Reads every row                | Good for small tables or large result sets; otherwise may indicate missing index |
-- | Index Scan             | Uses index then table          | Usually good                                                                     |
-- | Index Only Scan        | Reads only index               | Excellent when applicable                                                        |
-- | Bitmap Index Scan      | Builds bitmap of matching rows | Good for many matching rows                                                      |
-- | Bitmap Heap Scan       | Reads table pages from bitmap  | Good companion to bitmap index scan                                              |
-- | Cost                   | Estimated optimizer cost       | Estimate only                                                                    |
-- | Actual Time            | Measured execution time        | Real runtime                                                                     |
-- | Rows                   | Rows produced at that node     | Compare with estimates                                                           |
-- | Loops                  | Number of executions           | High values can signal inefficiency                                              |
-- | Rows Removed by Filter | Discarded rows                 | High numbers may indicate wasted work                                            |
-- Step 1: Examine the plan
EXPLAIN
SELECT customer_id,
       total_amount
FROM orders
WHERE customer_id = 101;

-- Step 2: Measure actual execution
EXPLAIN ANALYZE
SELECT customer_id,
       total_amount
FROM orders
WHERE customer_id = 101;

-- Step 3: If appropriate,
-- create or improve indexes,
-- rewrite inefficient queries,
-- then measure again.