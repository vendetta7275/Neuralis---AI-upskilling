import numpy as np

# Question 1: Create a NumPy array of shape (3, 3) representing a matrix. Compute its determinant, inverse, and eigenvalues

matrix = np.array([
    [2, 1, 3],
    [1, 4, 2],
    [3, 2, 5]
])

print("3x3 Matrix:")
print(matrix)

determinant = np.linalg.det(matrix)

inverse = np.linalg.inv(matrix)

eigenvalues = np.linalg.eigvals(matrix)

print("\nDeterminant:")
print(determinant)

print("\nInverse:")
print(inverse)

print("\nEigenvalues:")
print(eigenvalues)


# Question 2: Create two NumPy arrays of shape (2, 3) and (3, 2). Perform matrix multiplication on these arrays

arr1 = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

arr2 = np.array([
    [7, 8],
    [9, 10],
    [11, 12]
])

print("\nArray 1:")
print(arr1)

print("\nArray 2:")
print(arr2)

result = np.matmul(arr1, arr2)

print("\nMatrix Multiplication Result:")
print(result)