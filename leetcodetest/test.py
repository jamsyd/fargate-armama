class Solution(object):

    def minPartitions(self, n):
        """
        :type n: str
        :rtype: int
        """

        lst = []

        i = 0
        while i < len(n):
            
            lst.append(int(n[i]))
            i+=1

        print(max(lst))

Solution().minPartitions(str(83429))