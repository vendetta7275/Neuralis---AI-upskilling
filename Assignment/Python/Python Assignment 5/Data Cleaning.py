import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with 3 columns and 5 rows filled with random integers. Introduce some NaN values. Fill the NaN values with the mean of the respective columns

df1 = pd.DataFrame(
    np.random.randint(1, 100, size=(5, 3)),
    columns=['A', 'B', 'C']
)

df1.loc[1, 'A'] = np.nan
df1.loc[3, 'C'] = np.nan

print("Original DataFrame with NaN values:")
print(df1)

df1_filled = df1.fillna(df1.mean())

print("\nDataFrame after filling NaN with column mean:")
print(df1_filled)


# Question 2: Create a Pandas DataFrame with 4 columns and 6 rows filled with random integers. Introduce some NaN values. Drop the rows with any NaN values

df2 = pd.DataFrame(
    np.random.randint(1, 100, size=(6, 4)),
    columns=['W', 'X', 'Y', 'Z']
)

df2.loc[2, 'X'] = np.nan
df2.loc[4, 'Z'] = np.nan

print("\nOriginal DataFrame with NaN values:")
print(df2)

df2_cleaned = df2.dropna()

print("\nDataFrame after dropping rows with NaN values:")
print(df2_cleaned)