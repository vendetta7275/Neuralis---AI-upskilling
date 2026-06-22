import pandas as pd
import numpy as np

# Question 1: Create a Pandas DataFrame with 2 columns: 'Category' and 'Value'. Fill the 'Category' column with random categories ('A', 'B', 'C') and the 'Value' column with random integers. Group the DataFrame by 'Category' and compute the sum and mean of 'Value' for each category

categories = np.random.choice(['A', 'B', 'C'], size=10)
values = np.random.randint(1, 100, size=10)

df1 = pd.DataFrame({
    'Category': categories,
    'Value': values
})

print("Original DataFrame:")
print(df1)

result1 = df1.groupby('Category')['Value'].agg(['sum', 'mean'])

print("\nSum and Mean by Category:")
print(result1)


# Question 2: Create a Pandas DataFrame with 3 columns: 'Product', 'Category', and 'Sales'. Fill the DataFrame with random data. Group the DataFrame by 'Category' and compute the total sales for each category

products = ['Product1', 'Product2', 'Product3',
            'Product4', 'Product5', 'Product6']

categories = np.random.choice(
    ['Electronics', 'Clothing', 'Food'],
    size=6
)

sales = np.random.randint(100, 1000, size=6)

df2 = pd.DataFrame({
    'Product': products,
    'Category': categories,
    'Sales': sales
})

print("\nOriginal Sales Data:")
print(df2)

total_sales = df2.groupby('Category')['Sales'].sum()

print("\nTotal Sales by Category:")
print(total_sales)