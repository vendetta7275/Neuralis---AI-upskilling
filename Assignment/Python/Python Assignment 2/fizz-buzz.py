//3. Iterate from 1 to n and return a list where multiples of 3 are "Fizz", 5 are "Buzz", and both are "FizzBuzz".

class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []

        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))

        return result

