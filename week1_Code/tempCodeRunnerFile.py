def binary(nums,target,left,right):
    if left>right:
        return -1
    mid=(left+right)//2
    if nums[mid]>target:
        return binary(nums,target,left,mid-1)
    elif nums[mid]<target:
        return binary(nums,target,mid+1,right)
    else:
        return mid
def BinarySearch(nums, target):
    left=0
    right=len(nums)-1
    return binary(nums,target,left,right)