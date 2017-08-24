import sys

sys.path.append('../src/')
from Events import Events

e = Events()
e.register('../userDesign/hello.py:printHello')
e.register('../userDesign/hello.py:Hello#0.printText')

print e

e.fire('../userDesign/hello.py:printHello')
e.fire('../userDesign/hello.py:Hello#0.printText', 'ok')
