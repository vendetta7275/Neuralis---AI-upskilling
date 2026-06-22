import numpy as np
import numpy.ma as ma

# Question 1: Create a masked array of shape (4, 4) with random integers and mask the elements greater than 10. Compute the sum of the unmasked element


arr1 = np.random.randint(1, 21, size=(4, 4))

print("Original Array:")
print(arr1)

masked_arr1 = ma.masked_greater(arr1, 10)

print("\nMasked Array (values > 10 are masked):")
print(masked_arr1)

sum_unmasked = masked_arr1.sum()

print("\nSum of Unmasked Elements:")
print(sum_unmasked)


# Question 2: Create a masked array of shape (3, 3) with random integers and mask the diagonal elements. Replace the masked elements with the mean of the unmasked elements


arr2 = np.random.randint(1, 21, size=(3, 3))

print("\nOriginal Array:")
print(arr2)

mask = np.eye(3, dtype=bool)

masked_arr2 = ma.array(arr2, mask=mask)

print("\nMasked Array (Diagonal Masked):")
print(masked_arr2)

mean_value = masked_arr2.mean()

print("\nMean of Unmasked Elements:")
print(mean_value)

filled_array = masked_arr2.filled(mean_value)

print("\nArray after Replacing Diagonal with Mean:")
print(filled_array)