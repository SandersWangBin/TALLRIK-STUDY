#!/usr/bin/python
import re
import sys

class Loop:
    REG_SINGLE = '\[([0-9]*)\]'
    REG_RANGE  = '\[([0-9]*):([0-9]*)\]'

    LOOP_STATUS_LESS = '$LESS'
    LOOP_STATUS_IN   = '$IN'
    LOOP_STATUS_MAX  = '$MAX'
    LOOP_STATUS_MORE = '$MORE'

    FIRE_STATUS_TODO   = '$TODO'
    FIRE_STATUS_MUSTDO = '$MUSTDO'
    FIRE_STATUS_DOING  = '$DOING'
    FIRE_STATUS_DONE   = '$DONE'

    VALUE_MAX_INT = sys.maxint

    def __init__(self, loopStr='[1]'):
        self.loopStrList = list()
        self.loopStrList.append(loopStr)
        self.min ,self.max = self._parserLoopStr(loopStr)
        self.fireCount = 0
        self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)

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
                max = int(value2) if value2.isdigit() else Loop.VALUE_MAX_INT
            else:
                min, max = 1, 1
        return min, max

    def _updateLoopStatus(self, count):
        if count > self.max: return Loop.LOOP_STATUS_MORE
        elif count == self.max: return Loop.LOOP_STATUS_MAX
        elif count >= self.min and count < self.max: return Loop.LOOP_STATUS_IN
        else: return Loop.LOOP_STATUS_LESS

    def _updateFireStatus(self, count):
        if count <= 0: return Loop.FIRE_STATUS_TODO
        else:
            if count >= self.max: return Loop.FIRE_STATUS_DONE
            elif count >= self.min and count < self.max: return Loop.FIRE_STATUS_DOING
            else: return Loop.FIRE_STATUS_MUSTDO

    def _updateStatus(self, count):
        loopStatus = self._updateLoopStatus(count)
        fireStatus = self._updateFireStatus(count)
        return loopStatus, fireStatus

    def fire(self):
        self.fireCount += 1
        self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)

    def _times(self, loopMin, loopMax):
        self.min = self.min * loopMin
        if self.max == Loop.VALUE_MAX_INT or loopMax == Loop.VALUE_MAX_INT:
            self.max = Loop.VALUE_MAX_INT
        else: self.max = self.max * loopMax

    def timesLoopStr(self, loopStr):
        self.loopStrList.append(loopStr)
        loopMin, loopMax = self._parserLoopStr(loopStr)
        self._times(loopMin, loopMax)
        self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)
        return self

    def times(self, loop):
        self._times(loop.min, loop.max)
        self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)
        return self

    def _plus(self, loopMin, loopMax):
        self.min = self.min + loopMin
        if self.max == Loop.VALUE_MAX_INT or loopMax == Loop.VALUE_MAX_INT:
            self.max = Loop.VALUE_MAX_INT
        else: self.max = self.max + loopMax

    def plus(self, loop):
        self._plus(loop.min, loop.max)
        self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)
        return self

    def avail(self):
        if self.fireStatus == Loop.FIRE_STATUS_DONE or self.loopStatus == Loop.LOOP_STATUS_MAX \
        or self.loopStatus == Loop.LOOP_STATUS_MORE:
            return False
        else: return True

    def reset(self):
        if len(self.loopStrList) > 0:
            self.min, self.max = self._parserLoopStr(self.loopStrList[0])
            for i in range(1, len(self.loopStrList)):
                loopMin, loopMax = self._parserLoopStr(self.loopStrList[i])
                self._times(loopMin, loopMax)
            self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)
        
    def __str__(self):
        return '[' + str(self.min) + ':' + str(self.max) + '] ' + \
        str(self.fireCount) + self.fireStatus + self.loopStatus

class TNode:
    def __init__(self, type, item):
        self.type = type
        self.item = item
        self.childRank = 0
        self.loop = Loop('[]')
        self.avail = True   # count for loop
        self.enable = True  # disable when one of or branches is fired
        self.parent = None
        self.children = list()

    def __str__(self):
        result = self.type + ': ' + self.item + ' (' + str(self.childRank) + ')'
        result += 'loop: ' + str(self.loop) + ' avail: ' + str(self.avail) + ' enable: ' + str(self.enable)
        if self.parent != None: result += ' ^: ' + self.parent.item
        if len(self.children) > 0: result += ' v: ' + ' '.join([e.item for e in self.children])
        return result
    
