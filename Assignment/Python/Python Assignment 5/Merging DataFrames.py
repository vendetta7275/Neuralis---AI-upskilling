import pandas as pd

# Question 1: Create two Pandas DataFrames with a common column. Merge the DataFrames using the common column.

df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Name': ['John', 'Alice', 'Bob', 'Emma']
})

df2 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Score': [85, 92, 78, 88]
})

print("DataFrame 1:")
print(df1)

print("\nDataFrame 2:")
print(df2)

merged_df = pd.merge(df1, df2, on='ID')

print("\nMerged DataFrame:")
print(merged_df)


# Question 2: Create two Pandas DataFrames with different columns. Concatenate the DataFrames along the rows and along the columns

df3 = pd.DataFrame({
    'A': [10, 20, 30],
    'B': [40, 50, 60]
})

df4 = pd.DataFrame({
    'C': [70, 80, 90],
    'D': [100, 110, 120]
})

print("\nDataFrame 3:")
print(df3)

print("\nDataFrame 4:")
print(df4)

concat_rows = pd.concat([df3, df4], axis=0)

print("\nConcatenated Along Rows:")
print(concat_rows)

concat_cols = pd.concat([df3, df4], axis=1)

print("\nConcatenated Along Columns:")
print(concat_cols)