from random import randint
from struct import pack

class dummysensor:

    def __init__(self, definition, mini, maxi, minnorm, maxnorm, stype, unit, prefix):
        self.stype = stype
        self.unit = unit
        self.prefix = prefix
        self.min_val = mini
        self.max_val = maxi
        self.min_norm = minnorm
        self.max_norm = maxnorm
        self.value = randint(self.min_val, self.max_val)
        self.record_support = 0
        if len(definition) > 32:
            self.description = definition[:32]
        else:
            self.description = definition #Limit 32 Characters

    def updateval(self):
        self.value = randint(self.min_val, self.max_val)

    def rdmdef(self, sensno):
        retval = bytearray()
        retval.extend(sensno.to_bytes(1, 'big'))
        retval.extend(pack('B', self.stype))
        retval.extend(pack('B', self.unit))
        retval.extend(pack('B', self.prefix))
        retval.extend(pack('!h', self.min_val))
        retval.extend(pack('!h', self.max_val))
        retval.extend(pack('!h', self.min_norm))
        retval.extend(pack('!h', self.max_norm))
        retval.extend(self.record_support.to_bytes(1, 'big'))
        if len(self.description) > 32:
            retval.extend(bytes(self.description[:32], 'utf-8'))
        else:
            retval.extend(bytes(self.description, 'utf-8')) #Limit 32 Characters
        return retval