"""
LinkedList class to maintain moving average efficiently

(removal and insertion in constant time)
"""


class Node:
    def __init__(self, val=0, before=None, after=None):
        self.val = val
        self.before = before
        self.after = after

class LinkedList:
    def __init__(self, capacity):
        self.start = Node()
        self.end = Node()
        self.start.after = self.end
        self.end.before = self.start
        self.sum = self.size = 0
        self.capacity = capacity

    def __len__(self):
        return self.size

    def __str__(self):
        build = "[ "
        pointer = self.start.after
        while pointer != self.end:
            build += str(pointer.val) + ", "
            pointer = pointer.after
        build += "]"
        return build

    def append(self, val: int):
        toAttach = Node(val)
        justBefore = self.end.before
        justBefore.after = toAttach
        self.end.before = toAttach
        toAttach.before = justBefore
        toAttach.after = self.end
        self.sum += val
        self.size += 1
    
    def getAvg(self):
        return self.sum / self.size

    def eject(self):
        if self.size == 0:
            return
        toRemove = self.start.after
        self.sum -= toRemove.val
        self.size -= 1
        self.start.after = toRemove.after
        toRemove.after.before = self.start

    def enforce(self):
        if len(self) > self.capacity:
            self.eject()

    def checkAgainst(self, val, low, high):
        if not len(self):
            return True
        avg = self.sum / self.size
        return low * avg <= val <= high * avg
