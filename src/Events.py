#!/usr/bin/python

import os, imp

class Events(object):
    SYMBOL_COLON = ':'
    SYMBOL_DOT   = '.'

    TYPE_MOD   = 'MOD'
    TYPE_FUNC  = 'FUNC'
    TYPE_CLASS = 'CLASS'

    KEYWORD_TYPE  = '$TYPE'
    KEYWORD_MOD   = '$MOD'
    KEYWORD_CLASS = '$CLASS'
    KEYWORD_FUNC  = '$FUNC'
    KEYWORD_INSTANCE = '$INSTANCE'

    def __init__(self):
        self.events = dict()

    def register(self, eventStr):
        r, t, a = self._parserEventStr(eventStr)
        if r:
            me = self._touchModElement(a[0])
            if t == Events.TYPE_FUNC:
                self._touchFuncElement(me, a[1])
            elif t == Events.TYPE_CLASS:
                oe = self._touchClassElement(me, a[1])
                self._touchFuncElement(oe, a[2])

    def _parserEventStr(self, eventStr):
        if Events.SYMBOL_COLON in eventStr:
            m, f = eventStr.rsplit(Events.SYMBOL_COLON, 1)
            if Events.SYMBOL_DOT in f:
                o, f = f.rsplit(Events.SYMBOL_DOT, 1)
                return True, Events.TYPE_CLASS, (m,o,f)
            else:
                return True, Events.TYPE_FUNC, (m, f)
        return False, None, None

    def _touchModElement(self, m):
        me = self.events.get(m, None)
        if me == None:
            self.events[m] = dict()
            self.events[m][Events.KEYWORD_TYPE] = Events.TYPE_MOD
            self.events[m][Events.KEYWORD_INSTANCE]  = self._loadModule(m)
            return self.events[m]
        else: return me

    def _loadModule(self, path):
        code_file = os.path.basename(path)
        base = code_file.replace(".py", "")
        with open(path, 'rb') as fin:
            return imp.load_source(base, path, fin)

    def _touchClassElement(self, e, o):
        oe = e.get(o, None)
        if oe == None:
            e[o] = dict()
            e[o][Events.KEYWORD_TYPE] = Events.TYPE_CLASS
            e[o][Events.KEYWORD_INSTANCE] = getattr(e[Events.KEYWORD_INSTANCE], o)()
            return e[o]
        else: return oe

    def _touchFuncElement(self, e, f):
        fe = e.get(f, None)
        if fe == None:
            e[f] = dict()
            e[f][Events.KEYWORD_TYPE] = Events.TYPE_FUNC
            e[f][Events.KEYWORD_INSTANCE] = getattr(e[Events.KEYWORD_INSTANCE], f)
            return e[f]
        else: return fe

    def __str__(self):
        return str(self.events)