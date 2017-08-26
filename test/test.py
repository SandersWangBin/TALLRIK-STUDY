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
root = genBinTree(genRpnList('<a>; ( (<b>,<c>,<d>*[0:]) | <e> ; <f>*[5] )'))
print
printTreeUpDown(root)
print
printTreeDownUp(root)
