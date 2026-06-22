//13. Find the common elements between two arrays.


class Solution:
    def intersection(self, nums1, nums2):
        return list(set(nums1) & set(nums2))