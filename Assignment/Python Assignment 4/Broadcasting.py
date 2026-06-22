import numpy as np

# Question 1: Create a NumPy array of shape (3, 3) filled with random integers. Add a 1D array of shape (3,) to each row of the 2D array using broadcasting.

arr1 = np.random.randint(1, 10, size=(3, 3))

vector1 = np.array([10, 20, 30])

print("Original 3x3 Array:")
print(arr1)

print("\n1D Array:")
print(vector1)

result1 = arr1 + vector1

print("\nResult after Broadcasting Addition:")
print(result1)


# Question 2: Create a NumPy array of shape (4, 4) filled with random integers. Subtract a 1D array of shape (4,) from each column of the 2D array using broadcasting

arr2 = np.random.randint(1, 20, size=(4, 4))

vector2 = np.array([1, 2, 3, 4])

print("\nOriginal 4x4 Array:")
print(arr2)

print("\n1D Array:")
print(vector2)

result2 = arr2 - vector2.reshape(4, 1)

print("\nResult after Broadcasting Subtraction:")
print(result2)