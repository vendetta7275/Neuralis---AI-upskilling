import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with columns 'Date', 'Category', and 'Value'. Create a pivot table to compute the sum of 'Value' for each 'Category' by 'Date'.

dates = pd.date_range('2021-01-01', periods=10)

df1 = pd.DataFrame({
    'Date': np.random.choice(dates, size=20),
    'Category': np.random.choice(['A', 'B', 'C'], size=20),
    'Value': np.random.randint(10, 100, size=20)
})

print("Original DataFrame:")
print(df1)

pivot1 = pd.pivot_table(
    df1,
    values='Value',
    index='Date',
    columns='Category',
    aggfunc='sum',
    fill_value=0
)

print("\nPivot Table (Sum of Value by Date and Category):")
print(pivot1)


# Question 2: Create a Pandas DataFrame with columns 'Year', 'Quarter', and 'Revenue'. Create a pivot table to compute the mean 'Revenue' for each 'Quarter' by 'Year'.

df2 = pd.DataFrame({
    'Year': np.random.choice([2021, 2022, 2023], size=20),
    'Quarter': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], size=20),
    'Revenue': np.random.randint(1000, 10000, size=20)
})

print("\nOriginal Revenue Data:")
print(df2)

pivot2 = pd.pivot_table(
    df2,
    values='Revenue',
    index='Year',
    columns='Quarter',
    aggfunc='mean',
    fill_value=0
)

print("\nPivot Table (Mean Revenue by Year and Quarter):")
print(pivot2)