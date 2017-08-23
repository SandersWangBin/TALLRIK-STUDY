import sys

sys.path.append('../src/')
from Events import Events

e = Events()
e.register('../userDesign/hello.py:printHello')
e.register('../userDesign/hello.py:Hello.printText')

print e

e.events['../userDesign/hello.py']['printHello']['$INSTANCE']()
e.events['../userDesign/hello.py']['Hello']['printText']['$INSTANCE']('ok')