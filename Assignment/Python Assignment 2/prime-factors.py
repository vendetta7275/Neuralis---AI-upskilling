//2. Given a number n. Find its unique prime factors in increasing order.
class Solution:
    def primeFac(self, n):
        factors = []

        if n % 2 == 0:
            factors.append(2)
            while n % 2 == 0:
                n //= 2

        i = 3
        while i * i <= n:
            if n % i == 0:
                factors.append(i)
                while n % i == 0:
                    n //= i
            i += 2

        if n > 1:
            factors.append(n)

        return factors