// Given an integer array, return True if any value appears at least twice in the array, and return False if every element is distinct
class Solution:
    def containsDuplicate(self, nums):
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False