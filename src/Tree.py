#!/usr/bin/python
import re

class Loop:
    REG_SINGLE = '\[([0-9]*)\]'
    REG_RANGE  = '\[([0-9]*):([0-9]*)\]'

    STATUS_LESS = '$LESS'
    STATUS_IN   = '$IN'
    STATUS_MORE = '$MORE'

    def __init__(self, loopStr='[1]'):
        self.min ,self.max = self._parserLoopStr(loopStr)
        self.used = 0
        self.status = self._updateStatus(self.used)

    def _parserLoopStr(self, loopStr):
        min, max = 1, 1
        m = re.search(Loop.REG_SINGLE, loopStr)
        if m:
            value = m.group(1)
            if value.isdigit(): min, max = int(value), int(value)
            else: min, max = 1, 1
        else:
            m = re.search(Loop.REG_RANGE, loopStr)
            if m:
                value1, value2 = m.group(1), m.group(2)
                min = int(value1) if value1.isdigit() else 1
                max = int(value2) if value2.isdigit() else -1
            else:
                min, max = 1, 1
        return min, max

    def _updateStatus(self, u):
        if u < self.min: return Loop.STATUS_LESS
        elif u >= self.min and u <= self.max: return Loop.STATUS_IN
        else: return Loop.STATUS_MORE

    def use(self):
        self.used += 1
        return self._updateStatus()

    def times(self, loopStr):
        loopMin, loopMax = self._parserLoopStr(loopStr)
        self.min = self.min * loopMin
        if self.max < 0 or loopMax < 0: self.max = -1
        else: self.max = self.max * loopMax
        return self

    def __str__(self):
        return '[' + str(self.min) + ':' + str(self.max) + '] ' + \
        str(self.used) + self.status

class TNode:
    def __init__(self, type, item):
        self.type = type
        self.item = item
        self.childRank = 0
        self.loop = Loop('[]')
        self.parent = None
        self.children = list()

    def __str__(self):
        result = self.type + ': ' + self.item + ' (' + str(self.childRank) + ')'
        result += 'loop: ' + str(self.loop)
        if self.parent != None: result += ' ^: ' + self.parent.item
        if len(self.children) > 0: result += ' v: ' + ', '.join([e.item for e in self.children])
        return result