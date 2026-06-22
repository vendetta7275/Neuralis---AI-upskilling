import numpy as np

# Question 1: Create two NumPy arrays of shape (3, 4) filled with random integers. Perform element-wise addition, subtraction, multiplication, and division

arr1 = np.random.randint(1, 20, size=(3, 4))
arr2 = np.random.randint(1, 20, size=(3, 4))

print("Array 1:")
print(arr1)

print("\nArray 2:")
print(arr2)

addition = arr1 + arr2
subtraction = arr1 - arr2
multiplication = arr1 * arr2
division = arr1 / arr2

print("\nElement-wise Addition:")
print(addition)

print("\nElement-wise Subtraction:")
print(subtraction)

print("\nElement-wise Multiplication:")
print(multiplication)

print("\nElement-wise Division:")
print(division)


# Question 2: Create a NumPy array of shape (4, 4) with values from 1 to 16. Compute the row-wise and column-wise sum.

arr3 = np.arange(1, 17).reshape(4, 4)

print("\n4x4 Array:")
print(arr3)

row_sum = np.sum(arr3, axis=1)

column_sum = np.sum(arr3, axis=0)

print("\nRow-wise Sum:")
print(row_sum)

print("\nColumn-wise Sum:")
print(column_sum)