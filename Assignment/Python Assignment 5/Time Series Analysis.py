import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with a datetime index and one column filled with random integers. Resample the DataFrame to compute the monthly mean of the values

dates1 = pd.date_range(start='2021-01-01', periods=365, freq='D')

df1 = pd.DataFrame({
    'Value': np.random.randint(1, 100, size=365)
}, index=dates1)

print("Original DataFrame:")
print(df1.head())

monthly_mean = df1.resample('ME').mean()
print("\nMonthly Mean:")
print(monthly_mean)


# Question 2: Create a Pandas DataFrame with a datetime index ranging from '2021-01-01' to '2021-12-31' and one column filled with random integers. Compute the rolling mean with a window of 7 days

dates2 = pd.date_range(start='2021-01-01', end='2021-12-31', freq='D')

df2 = pd.DataFrame({
    'Value': np.random.randint(1, 100, size=len(dates2))
}, index=dates2)

print("\nOriginal DataFrame:")
print(df2.head(10))

df2['Rolling_Mean_7_Days'] = df2['Value'].rolling(window=7).mean()

print("\nDataFrame with 7-Day Rolling Mean:")
print(df2.head(15))