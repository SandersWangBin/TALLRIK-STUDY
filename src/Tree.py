#!/usr/bin/python

class TNode:
    def __init__(self, type, item):
        self.type = type
        self.item = item
        self.parent = None
        self.children = list()

    def __str__(self):
        result = self.type + ': ' + self.item
        if self.parent != None: result += ' ^: ' + self.parent.item
        if len(self.children) > 0: result += ' v: ' + ', '.join([e.item for e in self.children])
        return result