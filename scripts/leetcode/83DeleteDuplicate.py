from IPython import embed
class ListNode:
    """
    Definition for singly-linked list.
    """
    def __init__(self, x):
        self.val = x
        self.next = None
    
    def __repr__(self):
        return 'ListNode %s and next is %s ' % (self.val, self.next.val)

class Solution:
    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if not head:
            return None
        tmp = head
        while not tmp is None:
            if tmp.next is None:
                break
            if tmp.next.val == tmp.val:
                tmp.next = tmp.next.next
            else:
                tmp = tmp.next
        return head

 
if __name__ == '__main__':
    h1 = ListNode(1)
    h2 = ListNode(1)
    h3 = ListNode(2)
    h4 = ListNode(3)
    h5 = ListNode(3)
    h6 = ListNode(4)
    h1.next = h2
    h2.next = h3
    h3.next = h4
    h4.next = h5
    h5.next = h6
    embed()
    s = Solution()
    s.deleteDuplicates(h1)
    embed()





