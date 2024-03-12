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
num=input("输入list中的元素个数：")
num=int(num)
nums=[]
print("请输入元素：")
for i in range(0,num):
    nums.append(int(input()))
nums.sort()
print("排序后的list为：",nums.sort())
target=int(input("请输入要查找的元素："))
print("下标为",BinarySearch(nums,target))