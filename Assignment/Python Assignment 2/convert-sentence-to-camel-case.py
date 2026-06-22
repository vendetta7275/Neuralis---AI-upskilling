// 7. Convert a given space-separated string into CamelCase.

class Solution:
    def convertToCamelCase(self, s):
        words = s.split()

        if not words:
            return ""

        result = words[0]

        for word in words[1:]:
            result += word[0].upper() + word[1:]

        return result