import numpy as np

# Question 1: Create a NumPy array of shape (3, 3) with values from 1 to 9. Reshape the array to shape (1, 9) and then to shape (9, 1)

arr1 = np.arange(1, 10).reshape(3, 3)

print("Original 3x3 Array:")
print(arr1)

arr_row = arr1.reshape(1, 9)

print("\nReshaped to (1, 9):")
print(arr_row)

arr_col = arr1.reshape(9, 1)

print("\nReshaped to (9, 1):")
print(arr_col)


# Question 2: Create a NumPy array of shape (5, 5) filled with random integers. Flatten the array and then reshape it back to (5, 5)

arr2 = np.random.randint(1, 100, size=(5, 5))

print("\nOriginal 5x5 Array:")
print(arr2)

flat_arr = arr2.flatten()

print("\nFlattened Array:")
print(flat_arr)

reshaped_arr = flat_arr.reshape(5, 5)

print("\nReshaped Back to (5, 5):")
print(reshaped_arr)