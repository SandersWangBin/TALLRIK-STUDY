#!/usr/bin/python

from Stack import Stack

SYMBOL_PARENLEFT = "("
SYMBOL_PARENRIGHT = ")"
SYMBOL_LOOP = "*"
SYMBOL_AND = ","
SYMBOL_OR = "|"
SYMBOL_NEXT = ";"
SYMBOL_VARLEFT = "<"
SYMBOL_VARRIGHT = ">"
SYMBOL_CONSTANTLEFT = "["
SYMBOL_CONSTANTRIGHT = "]"
SYMBOL_SPACE = " "

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
    elif left == SYMBOL_CONSTANTLEFT: return SYMBOL_CONSTANTRIGHT
    else: return left

def genRpnExp(runorExp):
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
                    rpnList.append(opStack.pop())
                opStack.push(c)
        elif c == SYMBOL_PARENLEFT:
            opStack.push(c)
        elif c == SYMBOL_PARENRIGHT:
            temp = opStack.pop()
            while (temp != SYMBOL_PARENLEFT and not opStack.isEmpty()):
                rpnList.append(temp)
                temp = opStack.pop()
        elif c == SYMBOL_VARLEFT or SYMBOL_CONSTANTLEFT:
            right = _lookupRight(c)
            temp = c
            i += 1
            c = runorExp[i]
            while c != right:
                temp += c
                i += 1
                c = runorExp[i]
            temp += c
            rpnList.append(temp)
        else:
            pass
        i += 1

    while not opStack.isEmpty(): rpnList.append(opStack.pop())
    print rpnList