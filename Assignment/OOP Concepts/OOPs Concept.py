from abc import ABC, abstractmethod
import math

# Class Creation + Encapsulation
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.__age = age  
        self.grade = grade

    # Setter method
    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("Age must be positive")

    # Getter method
    def get_age(self):
        return self.__age

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.__age}")
        print(f"Grade: {self.grade}")


# Inheritance
class HighSchoolStudent(Student):
    def __init__(self, name, age, grade, grade_level):
        super().__init__(name, age, grade)
        self.grade_level = grade_level

    # Method Overriding
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.get_age()}")
        print(f"Grade: {self.grade}")
        print(f"Grade Level: {self.grade_level}")


# Polymorphism
def print_student_info(student):
    student.display_info()


# Abstraction
class Shape(ABC):

    @abstractmethod
    def calculate_area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width


# Output

print("===== Student =====")
student1 = Student("John", 18, "A")
student1.display_info()

print("\nUpdating Age...")
student1.set_age(19)
print("Updated Age:", student1.get_age())

print("\n===== High School Student =====")
student2 = HighSchoolStudent("Alice", 16, "A+", 11)
student2.display_info()

print("\n===== Polymorphism =====")
print_student_info(student1)
print()
print_student_info(student2)

print("\n===== Abstraction =====")
circle = Circle(5)
rectangle = Rectangle(10, 4)

print("Circle Area:", round(circle.calculate_area(), 2))
print("Rectangle Area:", rectangle.calculate_area())