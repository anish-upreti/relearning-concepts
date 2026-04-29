# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # two pointers technique
        slow = fast = head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            if slow == fast:
                return True

        return False
    
    ## Time - O(n)
    ## space - O(1)



## Alternate solution using hashing
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:

        # hash table technique
        visited_node = set()
        curr = head

        while curr:
            if curr in visited_node:
                return True

            visited_node.add(curr)
            curr = curr.next

        return False
    
    ## time - O(n)
    ## space - O(n)