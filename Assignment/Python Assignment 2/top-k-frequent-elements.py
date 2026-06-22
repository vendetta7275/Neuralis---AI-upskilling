//11. Given an integer array nums and an integer K, return the k most frequent elements. You may return the answer in any order.

from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        count = Counter(nums)

        return [num for num, freq in count.most_common(k)]