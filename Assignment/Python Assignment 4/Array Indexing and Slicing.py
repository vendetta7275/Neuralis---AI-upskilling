import numpy as np

# Question 1:  Create a NumPy array of shape (6, 6) with values from 1 to 36. Extract the sub-array consisting of the 3rd to 5th rows and 2nd to 4th columns

arr1 = np.arange(1, 37).reshape(6, 6)

print("Original Array:")
print(arr1)

sub_array = arr1[2:5, 1:4]

print("\nSub-array (3rd to 5th rows, 2nd to 4th columns):")
print(sub_array)


# Question 2: Create a NumPy array of shape (5, 5) with random integers. Extract the elements on the border.

arr2 = np.random.randint(1, 100, size=(5, 5))

print("\nRandom 5x5 Array:")
print(arr2)

top_row = arr2[0, :]
bottom_row = arr2[-1, :]
left_col = arr2[1:-1, 0]
right_col = arr2[1:-1, -1]

border_elements = np.concatenate(
    [top_row, right_col, bottom_row[::-1], left_col[::-1]]
)

print("\nBorder Elements:")
print(border_elements)