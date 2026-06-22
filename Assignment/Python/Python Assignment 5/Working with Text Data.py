import pandas as pd

# Question 1: Create a Pandas Series with 5 random text strings. Convert all the strings to uppercase.

series1 = pd.Series(['apple', 'banana', 'cherry', 'mango', 'orange'])

print("Original Series:")
print(series1)

uppercase_series = series1.str.upper()

print("\nUppercase Series:")
print(uppercase_series)


# Question 2: Create a Pandas Series with 5 random text strings. Extract the first three characters of each string.all dataset (Iris/Titanic): cleaning, summary stats, 3–4 plots in a Jupyter notebook

series2 = pd.Series(['python', 'pandas', 'numpy', 'jupyter', 'dataset'])

print("\nOriginal Series:")
print(series2)

first_three_chars = series2.str[:3]

print("\nFirst Three Characters:")
print(first_three_chars)