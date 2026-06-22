import numpy as np

# Question 1: Create a NumPy array of shape (5, 5) filled with random integers between 1 and 20. Replace all the elements in the third column with 1

arr1 = np.random.randint(1, 21, size=(5, 5))

print("Original Array:")
print(arr1)

arr1[:, 2] = 1

print("\nArray after replacing third column with 1:")
print(arr1)


# Question 2: Create a NumPy array of shape (4, 4) with values from 1 to 16. Replace the diagonal elements with 0.

arr2 = np.arange(1, 17).reshape(4, 4)

print("\nOriginal 4x4 Array:")
print(arr2)

np.fill_diagonal(arr2, 0)

print("\nArray after replacing diagonal elements with 0:")
print(arr2)