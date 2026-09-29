## Problem 2: E-Commerce Stream Processing via Chunking (Pd 2.5)
"""
Problem Statement:
A global retail platform receives transactions at a higher scale than available memory
 can support safely at once. To prevent Out-of-Memory (OOM) errors, 
 the data engine must ingest large ledger exports sequentially in small, 
 controlled memory windows (chunks).

The program must execute the following operations:

Load an order transactional file in chunks of 2 rows at a time using chunksize.
For each chunk processed, print the text --- Chunk Processed ---.
Extract and display the individual order records inside that chunk.
Keep a running tally of the total revenue (Amount) calculated safely across all processed chunks.
Print the absolute calculated total value after the stream ends.

Requirements:
Process orders.csv with pd.read_csv(..., chunksize=2).
Track and print cumulative sums incrementally.

Input File:
orders.csv

Output Format:
--- Chunk Processed ---
[Row Records]
...
Total Cumulative Revenue: [Value]

Sample orders.csv:
------------------
OrderID,Customer,Amount
TX101,Amit,1500
TX102,Sita,2300
TX103,John,850
TX104,Zara,4200

Test Case:
----------
case=1
output=
--- Chunk Processed ---
TX101 Amit 1500
TX102 Sita 2300
--- Chunk Processed ---
TX103 John 850
TX104 Zara 4200

Total Cumulative Revenue: 8850.0


"""
import pandas as pd
total=0
chunks=pd.read_csv("orders.csv", chunksize=2)
for chunk in chunks:
    print("--- Chunk Processed ---")
    print(chunk.to_string(index=False,header=False))
    total+=chunk["Amount"].sum()
print(f"\nTotal Cumulative Revenue: {float(total)}")