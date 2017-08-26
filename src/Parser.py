#!/usr/bin/python

from Stack import Stack
from Tree import TNode

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