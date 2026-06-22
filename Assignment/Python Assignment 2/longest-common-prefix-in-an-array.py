//6. Given an array of strings, find the longest common prefix string shared among all of them.

class Solution:
    def longestCommonPrefix(self, arr):
        if not arr:
            return ""

        prefix = arr[0]

        for s in arr[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]

                if not prefix:
                    return ""

        return prefix