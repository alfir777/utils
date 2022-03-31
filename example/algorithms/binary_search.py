def binary_search(nums, search_num):
    lowest = 0
    highest = len(nums) - 1
    index = None
    while (lowest <= highest) and (index is None):
        mid = (lowest + highest) // 2
        if nums[mid] == search_num:
            index = mid
        else:
            if search_num < nums[mid]:
                highest = mid - 1
            else:
                lowest = mid + 1
    return index


assert binary_search([1, 4, 6, 8, 9, 10], 6) == 2
