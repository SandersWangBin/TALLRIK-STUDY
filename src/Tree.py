#!/usr/bin/python
import re
import sys
from Stack import Stack

SYMBOL_PARENLEFT = "("
SYMBOL_PARENRIGHT = ")"
SYMBOL_LOOP = "*"
SYMBOL_AND = ","
SYMBOL_OR = "|"
SYMBOL_NEXT = ";"
SYMBOL_VARLEFT = "<"
SYMBOL_VARRIGHT = ">"
SYMBOL_CONSLEFT = "["
SYMBOL_CONSRIGHT = "]"
SYMBOL_SPACE = " "

TYPE_OP   = "OP"
TYPE_VAR  = "VAR"
TYPE_CONS = "CONS"

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

    def _updateLoop(self):
        if count >= self.max:
            self.loops += 1
            self.loopIn = 0

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

    def clone(self):
        if len(self.loopStrList) > 0:
            newLoop = Loop(self.loopStrList[0])
            for i in range(1, len(self.loopStrList)):
                newLoop.timesLoopStr(self.loopStrList[i])
            return newLoop
        else: return None
            
    def reset(self):
        if len(self.loopStrList) > 0:
            self.min, self.max = self._parserLoopStr(self.loopStrList[0])
            for i in range(1, len(self.loopStrList)):
                loopMin, loopMax = self._parserLoopStr(self.loopStrList[i])
                self._times(loopMin, loopMax)
            self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)

    def restart(self):
        self.fireCount = 0
        self.loopStatus, self.fireStatus = self._updateStatus(self.fireCount)

    def startFire(self):
        if self.fireStatus == Loop.FIRE_STATUS_TODO: self.fireStatus = Loop.FIRE_STATUS_DOING

    def stopFire(self):
        if self.fireStatus == Loop.FIRE_STATUS_DOING \
        and (self.loopStatus != Loop.LOOP_STATUS_LESS \
        or (self.loopStatus == Loop.LOOP_STATUS_LESS \
        and self.fireCount >= self.min - 1)):
            self.fireStatus = Loop.FIRE_STATUS_DONE
            return True
        else: return False

    def loopStr(self):
        max = str(self.max) if self.max != Loop.VALUE_MAX_INT else '~'
        return '[' + str(self.min) + ':' + max + ']'

    def __str__(self):
        return self.loopStr() + ' ' + \
        str(self.fireCount) + self.fireStatus + self.loopStatus

class TNode:
    def __init__(self, type, item):
        self.type = type
        self.item = item
        self.childRank = 0
        self.loop = Loop('[]')
        self.avail = True   # count for loop
        self.enable = True  # disable when one of or branches is fired
        self.almostDone = False # all of children are almost done (done + in)
        self.mustDo = False # at least one of children must be done
        self.parent = None
        self.children = list()
        self.copy = None    # point to the copy of init TNode.

    def clone(self):
        newTNode = TNode(self.type, self.item)
        newTNode.childRank = self.childRank
        newTNode.loop = self.loop.clone()
        newTNode.avail = self.avail
        newTNode.enable = self.enable
        newTNode.almostDone = self.almostDone
        newTNode.mustDo = self.mustDo
        return newTNode

    def __str__(self):
        result = self.type + ': ' + self.item + ' (' + str(self.childRank) + ')'
        result += 'loop: ' + str(self.loop) + ' avail(' + str(self.avail) + ') enable(' + str(self.enable) + ')'
        result += ' almostDone' if self.almostDone else ''
        result += ' mustDo' if self.mustDo else ''
        if self.parent != None: result += ' ^: ' + self.parent.item
        if len(self.children) > 0: result += ' v: ' + ' '.join([e.item for e in self.children])
        return result

class MergedTree:
    def __init__(self, rpnList):
        self.root = self._genBinTree(rpnList)
        self.mergeLoopTreeDownUp()
        self.mergeSameOpTreeDownUp()
        self.wishList = {}
        self.candiList = {}
        self._updateTreeFlagUpDown(self.root)
        self._generateWishList()
        self._copyTreeDownUp()

    def _genTNode(self, element):
        return TNode(element[0], element[1])

    def _genBinTree(self, rpnList):
        rpnStack = Stack()
        for e in rpnList:
            type, item = e
            if type == TYPE_CONS or type == TYPE_VAR:
                rpnStack.push(self._genTNode(e))
            elif type == TYPE_OP:
                node = self._genTNode(e)
                r = rpnStack.pop()
                r.parent = node
                r.childRank = 1
                l = rpnStack.pop()
                l.parent = node
                node.children.append(l)
                node.children.append(r)
                rpnStack.push(node)
        return rpnStack.pop()

    def _handleTreeUpDown(self, node, _handleNode):
        _handleNode(node)
        for child in node.children: self._handleTreeUpDown(child, _handleNode)
    
    def _handleTreeDownUp(self, node, _handleNode):
        for child in node.children: self._handleTreeDownUp(child, _handleNode)
        _handleNode(node)
    
    def _printNode(self, node):
        if node != None: print str(node)
    
    def printTreeUpDown(self):
        self._handleTreeUpDown(self.root, self._printNode)
    
    def printTreeDownUp(self):
        self._handleTreeDownUp(self.root, self._printNode)

    def _mergeLoopNode(self, node):
        if node.type == TYPE_OP and node.item == SYMBOL_LOOP:
            node.children[0].loop.timesLoopStr(node.children[1].item)
            node.parent.children[node.childRank] = node.children[0]
            node.children[0].parent = node.parent
            node.children[1].parent = None
            for rank in range(0,len(node.parent.children)):
                node.parent.children[rank].childRank = rank
            node.parent = None
            del node.children
    
    def mergeLoopTreeDownUp(self):
        self._handleTreeDownUp(self.root, self._mergeLoopNode)
    
    def _mergeSameOpNode(self, node):
        if node.type == TYPE_OP and node.parent != None:
            if node.item == node.parent.item \
            and node.loop.loopStr() == node.parent.loop.loopStr():
                if node.childRank == 0:
                    node.parent.children = node.children + node.parent.children[1:]
                else:
                    node.parent.children = node.parent.children[:node.childRank] + \
                    node.children + node.parent.children[node.childRank+1:]
                for child in node.children: child.parent = node.parent
                for rank in range(0,len(node.parent.children)):
                    node.parent.children[rank].childRank = rank
                node.parent = None
                del node.children
    
    def mergeSameOpTreeDownUp(self):
        self._handleTreeDownUp(self.root, self._mergeSameOpNode)


    def _copyNode(self, node):
        # copy itself
        # if children copy, link them
        newNode = node.clone()
        newNode.copy = node
        node.copy = newNode
        for child in node.children:
            newNode.children.append(child.copy)

    def _copyTreeDownUp(self):
        self._handleTreeDownUp(self.root, self._copyNode)

    # merge next list (wish list and candi list)
    def _genAvailList(self, node):
        availList = list()
        nextOne = False
        if node.type == TYPE_OP and node.avail and node.enable:
            mustList = [child for child in node.children if (child.mustDo \
            and child.loop.fireStatus == Loop.FIRE_STATUS_DOING)]
            if len(mustList) > 0: return mustList
            
            doingLessList = [child for child in node.children \
            if child.loop.loopStatus == Loop.LOOP_STATUS_LESS \
            and (child.loop.fireStatus == Loop.FIRE_STATUS_DOING \
            or child.loop.fireStatus == Loop.FIRE_STATUS_MUSTDO)]
            for i in range(0, len(doingLessList)):
                if (doingLessList[i].loop.fireCount == doingLessList[i].loop.min - 1 \
                and doingLessList[i].almostDone) \
                or doingLessList[i].loop.fireCount >= doingLessList[i].loop.min:
                    del doingLessList[i]
            if len(doingLessList) > 0:
                #self.wishList.clear()
                return doingLessList

            for child in node.children:
                if child.avail and child.enable:
                    availList.append(child)
                    if child.loop.loopStatus == Loop.LOOP_STATUS_LESS \
                    and not child.almostDone:
                        nextOne = False
                    else: nextOne = True
                    if node.item == SYMBOL_NEXT and not nextOne: break
        return availList

    def _handleAvailTreeUpDown(self, node, _handleNode):
        _handleNode(node)
        #print node.item, ': ',
        #for child in self._genAvailList(node): print child.item,
        #print
        for child in self._genAvailList(node): self._handleAvailTreeUpDown(child, _handleNode)

    def _genCandiList(self, node):
        availList = list()
        if node.type == TYPE_OP:
            for child in node.children:
                if child.avail and child.enable:
                    availList.append(child)
                    if child.loop.loopStatus == Loop.LOOP_STATUS_LESS:
                        nextOne = False
                    else: nextOne = True
                    if node.item == SYMBOL_NEXT and not nextOne: break
        return availList



    def _addWishList(self, node):
        if node.type == TYPE_VAR: self.wishList[node.item] = node

    def _generateWishList(self):
        self.wishList.clear()
        self._handleAvailTreeUpDown(self.root, self._addWishList)

    def _updateTreeFlagUpDown(self, node):
        allDone, almostDone, mustDo = self._handleChildren(node)
        node.almostDone = almostDone
        node.mustDo = mustDo
        for child in node.children: self._updateTreeFlagUpDown(child)

    
    def _addCandiList(self, node):
        if node.type == TYPE_VAR: self.candiList[node.item] = node

    def _cleanupCandiList(self):
        pass


    def _generateCandiList(self, node):
        self.candiList.clear()
        newNode = node.copy
        self._handleAvailTreeUpDown(newNode, self._addCandiList)
        for k, v in self.candiList.iteritems():
            self.candiList[k] = v.copy
        ################################################
        # THIS IS WRONG.
        # THE self.root should have self.copy for original
        # every node in self.root connects its counterpart
        # in the self.copy which only can be used in generate
        # the candidate.
        # in this function, node should be used in self.copy
        # _handleTreeUpDown should be _handleAvailTreeUpDown


    def printWishList(self):
        print 'wish list:',
        for child in self.wishList.keys(): print child,
        print

    def printCandiList(self):
        print 'candi list:', 
        for child in self.candiList.keys(): print child,
        print


    # fire wish
    def _handleSingleTreeDownUp(self, node, _handleNode):
        _handleNode(node)
        if node.parent != None: self._handleSingleTreeDownUp(node.parent, _handleNode)

    def _handleBrother(self, node):
        if node.parent != None:
            if node.parent.type == TYPE_OP and node.parent.item == SYMBOL_OR:
                for child in node.parent.children:
                    if child.childRank != node.childRank: child.enable = False
            elif node.parent.type == TYPE_OP and node.parent.item == SYMBOL_AND:
                for child in node.parent.children:
                    if child.childRank != node.childRank:
                        if child.loop.stopFire():
                            child.enable = False
                            child.avail = child.loop.avail()
            elif node.parent.type == TYPE_OP and node.parent.item == SYMBOL_NEXT:
                for i in range(0, node.childRank):
                    node.parent.children[i].enable = False
                    node.parent.children[i].loop.stopFire()

    def _handleChildren(self, node):
        ############ catch and case to fire
        if node.item == SYMBOL_AND and len(node.children) > 0:
            doneList = [child for child in node.children if child.loop.fireStatus == Loop.FIRE_STATUS_DONE]
            inList = [child for child in node.children if child.loop.loopStatus == Loop.LOOP_STATUS_IN \
                      and child.loop.fireStatus != Loop.FIRE_STATUS_DONE]
            mustList = [child for child in node.children if (child.loop.loopStatus == Loop.LOOP_STATUS_LESS \
                        or child.mustDo) and child.enable]
            allDone = (len(doneList) == len(node.children))
            almostDone = (len(inList) + len(doneList) == len(node.children))
            mustDo = len(mustList) > 0
            return allDone, almostDone, mustDo
        ############ catch or case to fire
        elif node.item == SYMBOL_OR and len(node.children) > 0:
            totalList = [child for child in node.children if child.enable]
            doneList = [child for child in node.children if child.loop.fireStatus == Loop.FIRE_STATUS_DONE \
                        and child.enable]
            inList = [child for child in node.children if (child.loop.loopStatus == Loop.LOOP_STATUS_IN \
                      or (child.almostDone and child.loop.fireCount == child.loop.min - 1))
                      and child.avail and child.enable]
            mustList = [child for child in node.children if ((child.loop.loopStatus == Loop.LOOP_STATUS_LESS and not child.almostDone) \
                        or child.mustDo) \
                        and child.avail and child.enable]
            #print 'handleChildren, or branch:', node.item, node.loop.loopStr(), str(len(doneList)), str(len(inList)),
            allDone = (len(doneList) == 1)
            almostDone = ((len(inList) + len(doneList) == len(totalList)) and len(inList) > 0)
            mustDo = len(mustList) > 0
            return allDone, almostDone, mustDo
        ############ catch next case to fire
        elif node.item == SYMBOL_NEXT and len(node.children) > 0:
            children = [child for child in node.children if child.enable]
            doneStatus, doneLen = 'TODO', 0
            inStatus, inLen = 'TODO', 0
            for i in range(0, len(children)):
                if children[i].loop.fireStatus == Loop.FIRE_STATUS_DONE \
                and doneStatus != 'DONE' and inStatus == 'TODO':
                    doneLen += 1
                    doneStatus = 'DOING'
                elif (children[i].loop.fireStatus != Loop.FIRE_STATUS_DONE \
                and children[i].loop.loopStatus == Loop.LOOP_STATUS_IN) \
                or child.almostDone:
                    doneStatus = 'DONE'
                    inLen += 1
                    inStatus = 'DOING'
            mustList = [child for child in node.children if (child.loop.loopStatus == Loop.LOOP_STATUS_LESS \
                        or child.mustDo) \
                        and child.avail and child.enable]
            allDone = doneLen == len(children)
            almostDone = ((doneLen + inLen) == len(children) and inLen > 0)
            mustDo = len(mustList) > 0
            return allDone, almostDone, mustDo
        else: return True, False, False

    def _restartNode(self, node):
        node.loop.restart()
        node.avail = node.loop.avail()
        node.enable = True

    def _restartTreeUpDown(self, node):
        self._handleTreeUpDown(node, self._restartNode)


    def _fireWish(self, node):
        if node.type != TYPE_OP:
            node.loop.fire()
            node.avail = node.loop.avail()
        else:
            allDone, almostDone, mustDo = self._handleChildren(node)
            node.almostDone = almostDone
            node.mustDo = mustDo
            if allDone:
                node.loop.fire() # count + 1
                # node.children (all) restart to 0
                if node.loop.loopStatus == Loop.LOOP_STATUS_LESS \
                or node.loop.loopStatus == Loop.LOOP_STATUS_IN:
                    for child in node.children: self._restartTreeUpDown(child)
                if node.loop.loopStatus == Loop.LOOP_STATUS_LESS:
                    # WHY STATUS IN should not update mustDo flag???
                    # BECAUSE STATUS IN the mustDo is not needed, still follow the previous loop
                    _, node.almostDone, node.mustDo = self._handleChildren(node)
            elif almostDone:
                #print '!!!! almost done'
                ## startFire
                ## if node.loop.loopStatus:
                ## -> less or in: candiList
                node.loop.startFire()
                if (node.loop.loopStatus == Loop.LOOP_STATUS_LESS \
                or node.loop.loopStatus == Loop.LOOP_STATUS_IN) \
                and node.loop.fireCount < node.loop.max - 1:
                    #print '!!!! generate candi list'
                    self._generateCandiList(node)
            else:
                # startFire
                node.loop.startFire()
                
            node.avail = node.loop.avail()
            if node.avail: pass ########################### how to count one time is done???
            else: node.loop.startFire()
        self._handleBrother(node)

    # fire candi
    # node.parent: alldone or almostdone, restart counter
    def _restartForCandi(self, node):
        if node.type != TYPE_OP:
            pass
        else:
            allDone, almostDone, mustDo = self._handleChildren(node)
            if allDone:
                # I do not think this case will happen
                pass
            elif almostDone:
                #print '!!!! almost done - completed'
                if (node.loop.loopStatus == Loop.LOOP_STATUS_LESS \
                or node.loop.loopStatus == Loop.LOOP_STATUS_IN) \
                and node.loop.fireCount < node.loop.max - 1:
                    #print '!!!! restart counts by candi list'
                    for child in node.children: self._restartTreeUpDown(child)
                    node.loop.fire() # count + 1
                    node.almostDone = False
                node.avail = node.loop.avail()
            else:
                # ignore this case
                pass

    # fire itself. upDown fire parent
    # calculate the alldone and almostDone, generate candiList
    # fire wish???
    def _fireCandi(self, node): pass


    def _getMustFromWishList(self):
        mustList = {}
        for node in self.wishList.values():
            if node.loop.loopStatus == Loop.LOOP_STATUS_LESS \
            and (node.loop.fireStatus == Loop.FIRE_STATUS_DOING \
            or node.loop.fireStatus == Loop.FIRE_STATUS_MUSTDO):
                mustList[node.item] = node
        if len(mustList) > 0: self.wishList = mustList

    # fire
    def fire(self, statement):
        if self.wishList.get(statement, None) != None:
            self.candiList.clear()
            self._handleSingleTreeDownUp(self.wishList[statement], self._fireWish)
            self._generateWishList()
            #self._getMustFromWishList()
            return
        else:
            if self.candiList.get(statement, None) != None:
                self._handleSingleTreeDownUp(self.candiList[statement], self._restartForCandi)
                self._handleSingleTreeDownUp(self.candiList[statement], self._fireWish)
                self.candiList.clear()
                self._generateWishList()
                #self._getMustFromWishList()
