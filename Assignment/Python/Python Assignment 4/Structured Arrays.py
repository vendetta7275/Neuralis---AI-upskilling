import numpy as np

# Question 1: Create a structured array with fields 'name' (string), 'age' (integer), and 'weight' (float). Add some data and sort the array by age.


dtype1 = [('name', 'U20'), ('age', 'i4'), ('weight', 'f4')]

students = np.array([
    ('John', 20, 65.5),
    ('Alice', 18, 55.2),
    ('Bob', 22, 70.8),
    ('Emma', 19, 60.0)
], dtype=dtype1)

print("Original Structured Array:")
print(students)

sorted_students = np.sort(students, order='age')

print("\nSorted by Age:")
print(sorted_students)


# Question 2: Create a structured array with fields 'x' and 'y' (both integers). Add some data and compute the Euclidean distance between each pair of points


dtype2 = [('x', 'i4'), ('y', 'i4')]

points = np.array([
    (1, 2),
    (4, 6),
    (7, 8),
    (2, 5)
], dtype=dtype2)

print("\nPoints:")
print(points)

n = len(points)

print("\nEuclidean Distances:")

for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = points[i]
        x2, y2 = points[j]

        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        print(f"Distance between Point {i+1} and Point {j+1}: {distance:.2f}")