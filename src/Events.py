#!/usr/bin/python

import os, imp

class Events(object):
    SYMBOL_COLON = ':'
    SYMBOL_DOT   = '.'
    SYMBOL_SIGN  = '#'

    TYPE_MOD  = 'MOD'
    TYPE_FUNC = 'FUNC'
    TYPE_OBJ  = 'OBJ'

    KEYWORD_TYPE     = '$TYPE'
    KEYWORD_MOD      = '$MOD'
    KEYWORD_OBJ      = '$OBJ'
    KEYWORD_OBJFUNC  = '$OBJFUNC'
    KEYWORD_FUNC     = '$FUNC'
    KEYWORD_INSTANCE = '$INSTANCE'

    def __init__(self):
        self.events = dict()

    def register(self, eventStr, *args):
        r, t, a = self._parserEventStr(eventStr)
        if r:
            me = self._touchModElement(a[0])
            if t == Events.TYPE_FUNC:
                self._touchFuncElement(me, a[1])
            elif t == Events.KEYWORD_OBJ:
                self._touchObjElement(me, a[1], *args)
            elif t == Events.KEYWORD_OBJFUNC:
                oe = self._touchObjElement(me, a[1], *args)
                self._touchFuncElement(oe, a[2])

    def fire(self, eventStr, *args):
        r, t, a = self._parserEventStr(eventStr)
        if r:
            me = self._getModElement(a[0])
            if t == Events.TYPE_FUNC and me != None:
                self._getFuncElement(me, a[1])[Events.KEYWORD_INSTANCE](*args)
            elif t == Events.KEYWORD_OBJFUNC and me != None:
                oe = self._getObjElement(me, a[1])
                if oe != None:
                    self._getFuncElement(oe, a[2])[Events.KEYWORD_INSTANCE](*args)

    def _parserEventStr(self, eventStr):
        if Events.SYMBOL_COLON in eventStr:
            m, f = eventStr.rsplit(Events.SYMBOL_COLON, 1)
            if Events.SYMBOL_DOT in f:
                o, f = f.rsplit(Events.SYMBOL_DOT, 1)
                return True, Events.KEYWORD_OBJFUNC, (m,o,f)
            elif Events.SYMBOL_SIGN in f:
                return True, Events.KEYWORD_OBJ, (m, f)
            else:
                return True, Events.TYPE_FUNC, (m, f)
        return False, None, None

    def _getModElement(self, m):
        return self.events.get(m, None)

    def _touchModElement(self, m):
        me = self._getModElement(m)
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

    def _getObjElement(self, e, o):
        return e.get(o, None)

    def _getClassName(self, o):
        return o.rsplit(Events.SYMBOL_SIGN, 1)[0]

    def _touchObjElement(self, e, o, *args):
        oe = self._getObjElement(e, o)
        if oe == None:
            e[o] = dict()
            e[o][Events.KEYWORD_TYPE] = Events.TYPE_OBJ
            e[o][Events.KEYWORD_INSTANCE] = \
                getattr(e[Events.KEYWORD_INSTANCE], \
                self._getClassName(o))(*args)
            return e[o]
        else: return oe

    def _getFuncElement(self, e, f):
        return e.get(f, None)

    def _touchFuncElement(self, e, f):
        fe = self._getFuncElement(e, f)
        if fe == None:
            e[f] = dict()
            e[f][Events.KEYWORD_TYPE] = Events.TYPE_FUNC
            e[f][Events.KEYWORD_INSTANCE] = getattr(e[Events.KEYWORD_INSTANCE], f)
            return e[f]
        else: return fe

    def __str__(self):
        return 'self.events: ' + str(self.events)
    
