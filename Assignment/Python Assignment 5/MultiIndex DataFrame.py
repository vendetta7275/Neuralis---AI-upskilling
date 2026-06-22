import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with a MultiIndex (hierarchical index). Perform some basic indexing and slicing operations on the MultiIndex DataFrame

index = pd.MultiIndex.from_tuples(
    [
        ('Class A', 'Student 1'),
        ('Class A', 'Student 2'),
        ('Class B', 'Student 1'),
        ('Class B', 'Student 2'),
        ('Class C', 'Student 1'),
        ('Class C', 'Student 2')
    ],
    names=['Class', 'Student']
)

df1 = pd.DataFrame(
    np.random.randint(50, 100, size=(6, 3)),
    index=index,
    columns=['Math', 'Science', 'English']
)

print("MultiIndex DataFrame:")
print(df1)

print("\nData for Class A:")
print(df1.loc['Class A'])

print("\nData for Class B, Student 1:")
print(df1.loc[('Class B', 'Student 1')])

print("\nData for Class A and Class B:")
print(df1.loc[['Class A', 'Class B']])


# Question 2: Create a Pandas DataFrame with MultiIndex consisting of 'Category' and 'SubCategory'. Fill the DataFrame with random data and compute the sum of values for each 'Category' and 'SubCategory'.

index2 = pd.MultiIndex.from_tuples(
    [
        ('Electronics', 'Mobile'),
        ('Electronics', 'Laptop'),
        ('Clothing', 'Men'),
        ('Clothing', 'Women'),
        ('Food', 'Snacks'),
        ('Food', 'Drinks')
    ],
    names=['Category', 'SubCategory']
)

df2 = pd.DataFrame(
    {
        'Value': np.random.randint(100, 1000, size=6)
    },
    index=index2
)

print("\nCategory MultiIndex DataFrame:")
print(df2)

category_sum = df2.groupby(level='Category').sum()

print("\nSum by Category:")
print(category_sum)

subcategory_sum = df2.groupby(level=['Category', 'SubCategory']).sum()

print("\nSum by Category and SubCategory:")
print(subcategory_sum)