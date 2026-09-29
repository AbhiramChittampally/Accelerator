import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})

for label, content in df.items():
    print(f"Column Name: {label}")
    print(f"Column Data:\n{content}\n")
