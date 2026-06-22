import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with 3 columns and 5 rows filled with random integers. Add a new column that is the product of the first two columns

df1 = pd.DataFrame(
    np.random.randint(1, 10, size=(5, 3)),
    columns=['A', 'B', 'C']
)

print("Original DataFrame:")
print(df1)

df1['Product'] = df1['A'] * df1['B']

print("\nDataFrame after adding Product column:")
print(df1)


# Question 2: Create a Pandas DataFrame with 3 columns and 4 rows filled with random integers. Compute the row-wise and column-wise sum

df2 = pd.DataFrame(
    np.random.randint(1, 10, size=(4, 3)),
    columns=['X', 'Y', 'Z']
)

print("\nOriginal DataFrame:")
print(df2)

df2['Row_Sum'] = df2.sum(axis=1)

column_sum = df2.sum(axis=0)

print("\nDataFrame with Row-wise Sum:")
print(df2)

print("\nColumn-wise Sum:")
print(column_sum)