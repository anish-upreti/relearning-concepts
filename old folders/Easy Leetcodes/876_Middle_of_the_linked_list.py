# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        length = 0

        while curr:
            length += 1
            curr = curr.next

        m = length//2

        for i in range(m):
            head = head.next

        return head
    
    ## Time - O(n)
    ## space - O(1)


## Alternate solution -- using two pointer
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:

        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow
