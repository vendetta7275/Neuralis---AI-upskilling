import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with 4 columns and 6 rows filled with random integers. Set the index to be the first column.

df1 = pd.DataFrame(
    np.random.randint(1, 100, size=(6, 4)),
    columns=['Col1', 'Col2', 'Col3', 'Col4']
)

print("Original DataFrame:")
print(df1)

df1.set_index('Col1', inplace=True)

print("\nDataFrame after setting first column as index:")
print(df1)


# Question 2: Create a Pandas DataFrame with columns 'A', 'B', 'C' and index 'X', 'Y', 'Z'. Fill the DataFrame with random integers and access the element at row 'Y' and column 'B'

df2 = pd.DataFrame(
    np.random.randint(1, 100, size=(3, 3)),
    columns=['A', 'B', 'C'],
    index=['X', 'Y', 'Z']
)

print("\nDataFrame:")
print(df2)

# Access element at row Y and column B
value = df2.loc['Y', 'B']

print("\nElement at Row 'Y' and Column 'B':")
print(value)