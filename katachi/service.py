class itemIter(object):
    def __init__(self, numbers):
        self._numbers = numbers
        self._i = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._i == len(self._numbers):
            raise StopIteration()
        value = self._numbers[self._i]
        self._i += 1
        return (str(value[0]),str(value[1]))
    def search(self,target):
        for value in self:
            if value[0] == target:
                return(value[1])
    def searchLearning(self,targets):
        items = []
        for target in targets:
            items.append(self.search(target))
        return items