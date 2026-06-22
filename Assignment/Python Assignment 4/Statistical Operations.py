import numpy as np

# Question 1: Create a NumPy array of shape (5, 5) filled with random integers. Compute the mean, median, standard deviation, and variance of the array

arr1 = np.random.randint(1, 101, size=(5, 5))

print("Original 5x5 Array:")
print(arr1)

mean_value = np.mean(arr1)
median_value = np.median(arr1)
std_value = np.std(arr1)
variance_value = np.var(arr1)

print("\nMean:", mean_value)
print("Median:", median_value)
print("Standard Deviation:", std_value)
print("Variance:", variance_value)


# Question 2: Create a NumPy array of shape (3, 3) with values from 1 to 9. Normalize the array (i.e., scale the values to have a mean of 0 and a standard deviation of 1)

arr2 = np.arange(1, 10).reshape(3, 3)

print("\nOriginal 3x3 Array:")
print(arr2)

normalized_arr = (arr2 - np.mean(arr2)) / np.std(arr2)

print("\nNormalized Array:")
print(normalized_arr)

print("\nMean of Normalized Array:", np.mean(normalized_arr))
print("Standard Deviation of Normalized Array:", np.std(normalized_arr))