#!/usr/bin/python

from Stack import Stack
from Tree import TNode, Loop

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

SYMBOL_PRIORITY = {SYMBOL_LOOP: 1, \
                   SYMBOL_AND:  2, \
                   SYMBOL_OR:   2, \
                   SYMBOL_NEXT: 3}

SYMBOL_OP = [SYMBOL_LOOP, SYMBOL_AND, SYMBOL_OR, SYMBOL_NEXT]
def _isOp(op):
    return op in SYMBOL_OP

def _isLowerOp(op1, op2):
    if not _isOp(op1) or not _isOp(op2): return False
    else: return SYMBOL_PRIORITY[op1] < SYMBOL_PRIORITY[op2]

def _isHigherOp(op1, op2):
    if not _isOp(op1) or not _isOp(op2): return False
    else: return SYMBOL_PRIORITY[op1] >= SYMBOL_PRIORITY[op2]

def _lookupRight(left):
    if left == SYMBOL_PARENLEFT: return SYMBOL_PARENRIGHT
    elif left == SYMBOL_VARLEFT: return SYMBOL_VARRIGHT
    elif left == SYMBOL_CONSLEFT: return SYMBOL_CONSRIGHT
    else: return left

def genRpnList(runorExp):
    print runorExp
    rpnList = list()
    opStack = Stack()
    i = 0
    while i < len(runorExp):
        c = runorExp[i]
        if c == SYMBOL_SPACE:
            pass
        elif _isOp(c):
            if opStack.isEmpty() or \
            _isLowerOp(c, opStack.peek()) or \
            opStack.peek() == SYMBOL_PARENLEFT:
                opStack.push(c)
            else:
                while (not opStack.isEmpty() and \
                _isHigherOp(c, opStack.peek())):
                    rpnList.append((TYPE_OP, opStack.pop()))
                opStack.push(c)
        elif c == SYMBOL_PARENLEFT:
            opStack.push(c)
        elif c == SYMBOL_PARENRIGHT:
            op = opStack.pop()
            while (op != SYMBOL_PARENLEFT and not opStack.isEmpty()):
                rpnList.append((TYPE_OP, op))
                op = opStack.pop()
        elif c == SYMBOL_VARLEFT or SYMBOL_CONSLEFT:
            right = _lookupRight(c)
            type = TYPE_VAR if c == SYMBOL_VARLEFT else TYPE_CONS
            temp = c
            i += 1
            c = runorExp[i]
            while c != right:
                temp += c
                i += 1
                c = runorExp[i]
            temp += c
            rpnList.append((type, temp))
        else:
            pass
        i += 1
    while not opStack.isEmpty(): rpnList.append((TYPE_OP, opStack.pop()))
    print rpnList
    return rpnList

def _genTNode(element):
    return TNode(element[0], element[1])

def genBinTree(rpnList):
    rpnStack = Stack()
    for e in rpnList:
        type, item = e
        if type == TYPE_CONS or type == TYPE_VAR:
            rpnStack.push(_genTNode(e))
        elif type == TYPE_OP:
            node = _genTNode(e)
            r = rpnStack.pop()
            r.parent = node
            r.childRank = 1
            l = rpnStack.pop()
            l.parent = node
            node.children.append(l)
            node.children.append(r)
            rpnStack.push(node)
    return rpnStack.pop()

def _handleTreeUpDown(node, _handleNode):
    _handleNode(node)
    for child in node.children: _handleTreeUpDown(child, _handleNode)

def _handleTreeDownUp(node, _handleNode):
    for child in node.children: _handleTreeDownUp(child, _handleNode)
    _handleNode(node)

def _printNode(node):
    if node != None: print str(node)

def printTreeUpDown(root):
    _handleTreeUpDown(root, _printNode)

def printTreeDownUp(root):
    _handleTreeDownUp(root, _printNode)

def _mergeLoopNode(node):
    if node.type == TYPE_OP and node.item == SYMBOL_LOOP:
        node.children[0].loop.timesLoopStr(node.children[1].item)
        node.parent.children[node.childRank] = node.children[0]
        node.children[0].parent = node.parent
        node.children[1].parent = None
        for rank in range(0,len(node.parent.children)):
            node.parent.children[rank].childRank = rank
        node.parent = None
        del node.children

def mergeLoopTreeDownUp(root):
    _handleTreeDownUp(root, _mergeLoopNode)

def _mergeSameOpNode(node):
    if node.type == TYPE_OP and node.parent != None:
        if node.item == node.parent.item:
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

def mergeSameOpTreeDownUp(root):
    _handleTreeDownUp(root, _mergeSameOpNode)

def _updateLoopNode(node):
    if node.type == TYPE_OP and len(node.children) > 0:
        l = Loop('[0:0]')
        for child in node.children:
            if child.enable: l.plus(child.loop)
        node.loop.times(l)

def updateLoopTreeDownUp(root):
    _handleTreeDownUp(root, _updateLoopNode)

def _genAvailList(node):
    availList = list()
    if node.type == TYPE_OP:
        for child in node.children:
            if child.avail and child.enable:
                availList.append(child)
                if node.item == SYMBOL_NEXT: break
    return availList

def _handleAvailTreeUpDown(node, _handleNode):
    _handleNode(node)
    #print node.item, ': ',
    #for child in _genAvailList(node): print child.item,
    #print
    for child in _genAvailList(node): _handleAvailTreeUpDown(child, _handleNode)

def _handleAvailTreeDownUp(node, _handleNode):
    for child in node._genAvailList(node): _handleTreeDownUp(child, _handleNode)
    _handleNode(node)

def _addNextList(node):
    if node.type == TYPE_VAR: nextList.append(node)

def generateNextList(root):
    global nextList
    nextList = list()
    _handleAvailTreeUpDown(root, _addNextList)
    for node in nextList: print node.item,
    print

def _handleSingleTreeDownUp(node, _handleNode):
    _handleNode(node)
    if node.parent != None: _handleSingleTreeDownUp(node.parent, _handleNode)

def _fireNode(node):
    node.loop.fire()
    node.avail = node.loop.avail()
    if node.parent != None:
        if node.parent.type == TYPE_OP and node.parent.item == SYMBOL_OR:
            for child in node.parent.children:
                if child.childRank != node.childRank: child.enable = False
        elif node.parent.type == TYPE_OP and node.parent.item == SYMBOL_AND:
            for child in node.parent.children:
                if child.childRank != node.childRank:
                    child.loop.stopFire()
                    child.avail = child.loop.avail()
    node.loop.reset()
    _updateLoopNode(node)

def fireNode(node):
    _handleSingleTreeDownUp(node, _fireNode)

def fire(item):
    for node in nextList:
        if node.item == item:
            fireNode(node)
