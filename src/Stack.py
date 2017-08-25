#!/usr/bin/python

class Stack(object):
    def __init__(self):
        self._storage = list()

    def push(self, item):
        self._storage.append(item)

    def pop(self):
        return self._storage.pop()

    def peek(self):
        return self._storage[-1]

    def isEmpty(self):
        return len(self._storage) == 0
