#!/usr/bin/python

import sys

sys.path.append('../src/')
from Events import Events

e = Events()
e.register('../userDesign/hello.py:printHello')
e.register('../userDesign/hello.py:Hello#0', 456)
e.register('../userDesign/hello.py:Hello#0.printText')

print e

e.fire('../userDesign/hello.py:printHello')
e.fire('../userDesign/hello.py:Hello#0.printText', 123, 'ok')


def fireNodes(exp, nodes):
    from Parser import *
    root = genBinTree(genRpnList(exp))
    mergeLoopTreeDownUp(root)
    mergeSameOpTreeDownUp(root)
    #updateLoopTreeDownUp(root)
    print 'Expression:', exp
    print 'node list:', nodes
    print 'The original tree:'
    printTreeUpDown(root)
    print
    
    nextList = generateNextList(root)
    for n in nodes.split(' '):
        fire(n, nextList)
        nextList = generateNextList(root)

    print 'The final tree:'
    printTreeUpDown(root)
    print

def fireNodes2(exp, nodes):
    from Tree import *
    from Parser import *
    mt = MergedTree(genRpnList(exp))
    mt.printTreeUpDown()
    mt.printWishList()
    mt.printCandiList()

    for n in nodes.split(' '):
        print '==== ', n, ' ===='
        mt.fire(n)
        mt.printTreeUpDown()
        mt.printWishList()
        mt.printCandiList()

    print
    print



#fireNodes2('<a>; ( (<b>,<c>,<d>*[0:]) | (<e> ; <f>*[2]) )', '<a> <c> <d> <b>')
#fireNodes2('<a>; ( (<b>,<c>,<d>*[0:]) | (<e> ; <f>*[2]) )', '<a> <e> <f> <f>')
#fireNodes2('<a>*[0:]; <b>*[0:]', '<a> <b>')
#fireNodes2('<a>*[0:]; <b>*[0:]', '<b>')
#fireNodes2('(<a>*[0:], <b>*[0:])*[0:2]; <c>', '<b> <a>')
fireNodes2('(<a>*[0:1], <b>*[0:])*[0:2]; <c>', '<b> <a> <a> <b> <b> <c>')

'''
def verifyLoop(loopStr, loopStr2, fires=1):
    from Tree import Loop
    l = Loop(loopStr)
    print loopStr, str(l)
    print ' * ', loopStr2, 
    print '=>', str(l.timesLoopStr(loopStr2))
    print 'fire: ' + str(fires) + ' ', 
    for f in range(fires): l.fire()
    print l

verifyLoop('[]', '[]')
verifyLoop('[5]', '[2]')
verifyLoop('[3:5]', '[1:4]')
verifyLoop('[:5]', '[:2]')
verifyLoop('[3:]', '[4:]')
verifyLoop('[:]', '[:]')
verifyLoop('[0:5]', '[2]')
verifyLoop('[0:5]', '[0:]')

#print
#printTreeDownUp(root)
'''
