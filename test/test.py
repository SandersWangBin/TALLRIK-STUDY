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


from Parser import *
root = genBinTree(genRpnList('<a>; ( (<b>,<c>,<d>*[0:]) | (<e> ; <f>*[2]) )'))
print
#printTreeUpDown(root)
mergeLoopTreeDownUp(root)
mergeSameOpTreeDownUp(root)
updateLoopTreeDownUp(root)
#print
#printTreeUpDown(root)
#print

printTreeUpDown(root)
print

generateNextList(root)
fire('<a>')
generateNextList(root)
fire('<e>')
generateNextList(root)
fire('<f>')
generateNextList(root)
fire('<f>')
generateNextList(root)

printTreeUpDown(root)
print

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
