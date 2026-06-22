import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with 3 columns and 5 rows filled with random integers. Apply a function that doubles the values of the DataFrame

df1 = pd.DataFrame(
    np.random.randint(1, 20, size=(5, 3)),
    columns=['A', 'B', 'C']
)

print("Original DataFrame:")
print(df1)

def double_value(x):
    return x * 2

df1_doubled = df1.apply(double_value)

print("\nDataFrame after Doubling Values:")
print(df1_doubled)


# Question 2: Create a Pandas DataFrame with 3 columns and 6 rows filled with random integers. Apply a lambda function to create a new column that is the sum of the existing columns.

df2 = pd.DataFrame(
    np.random.randint(1, 20, size=(6, 3)),
    columns=['X', 'Y', 'Z']
)

print("\nOriginal DataFrame:")
print(df2)

df2['Total'] = df2.apply(
    lambda row: row['X'] + row['Y'] + row['Z'],
    axis=1
)

print("\nDataFrame with Total Column:")
print(df2)