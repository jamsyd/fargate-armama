# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def deepestLeavesSum(self, root):
        q    = [root]
        ans  = 0
        qlen = 0
        curr =  0
        
        while len(q):
            qlen = len(q)
            ans  = 0
            for _ in range(qlen):
                
                curr = q.pop(0)
                ans += curr.val

                if curr.left: 
                    q.append(curr.left)

                if curr.right: 
                    q.append(curr.right)
        return ans
    
## Alternative solution
# class Solution:
#     def deepestLeavesSum(self, root: TreeNode) -> int:
        
#         self.max_depth = self.find_max_depth(root)
        
#         self.deepest_sum = 0
#         self.get_deepest_sum(root, 1)
        
#         return self.deepest_sum
        
        
#     def get_deepest_sum(self, root, depth):
#         if not root:
#             return
                
#         if not root.left and not root.right:        
#             if depth == self.max_depth:
#                 self.deepest_sum += root.val
#             return
        
#         self.get_deepest_sum(root.left, depth + 1)
#         self.get_deepest_sum(root.right, depth + 1)
        
#         return
    
#     def find_max_depth(self, root):
#         if not root:
#             return 0
        
#         if not root.left and not root.right:
#             return 1
            
#         left = self.find_max_depth(root.left)
#         right = self.find_max_depth(root.right)
        
#         return max(left, right) + 1