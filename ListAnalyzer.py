
class ListAnalyzer:
    def __init__(self, list_one):
        self.list_one = sorted(list_one)

    def is_sequential(self, l_range=None):

        if l_range is not None:
            diff = max(self.list_one) - self.list_one[l_range]
            len_list = len(self.list_one[l_range:max(self.list_one)])
        else:
            diff = max(self.list_one) - min(self.list_one)
            len_list = len(self.list_one)

        return diff == len_list - 1

    def delete_max(self):
        if not self.list_one:
            return self.list_one
        # the maximum will always be deleted because the length of the list is constantly changing
        # ex: [1,4,7] -> not seq; [4,7] -> not seq; [7] -> seq (by our rule set)
        new_list = self.list_one
        for i in range(len(self.list_one)):
            if self.is_sequential(l_range=i):
                new_list = self.list_one[0:i]
                break
        self.list_one = new_list
        return new_list

    # splits the lists into their respective sequences then dumps them into a new list that could be iterated through
    def find_sequence(self):
        split_lists = []
        # used to maintain original list because object list will change
        iter_list = self.list_one
        i = 0
        k = 1
        while k < len(iter_list)+1:
            self.list_one = iter_list[i: k+1]

            if k == len(iter_list):
                split_lists.append(self.list_one)

            if not self.is_sequential():
                self.list_one = iter_list[i:k]
                split_lists.append(self.list_one)
                i = k
            k = k + 1

        return split_lists
