def sort_bubble(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


assert sort_bubble([1, 4, 6, 9, 8]) == [1, 4, 6, 8, 9]
