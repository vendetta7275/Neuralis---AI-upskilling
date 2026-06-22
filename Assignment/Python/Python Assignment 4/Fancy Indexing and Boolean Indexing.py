import numpy as np

# Question 1: create a NumPy array of shape (5, 5) filled with random integers. Use fancy indexing to extract the elements at the corners of the array

arr1 = np.random.randint(1, 21, size=(5, 5))

print("Original 5x5 Array:")
print(arr1)

corner_elements = arr1[[0, 0, 4, 4], [0, 4, 0, 4]]

print("\nCorner Elements:")
print(corner_elements)


# Question 2: Create a NumPy array of shape (4, 4) filled with random integers. Use boolean indexing to set all elements greater than 10 to 10

arr2 = np.random.randint(1, 21, size=(4, 4))

print("\nOriginal 4x4 Array:")
print(arr2)

arr2[arr2 > 10] = 10

print("\nArray after setting values > 10 to 10:")
print(arr2)