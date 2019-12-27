from random import randint

class dummysensor:
    stype = 0
    unit = 0
    prefix = 0
    min_val = -100
    max_val = 100
    min_norm = -50
    max_norm = 50
    value = 0
    record_support = 0
    description = 0 #Limit 32 Characters

    def __init__(self):
        pass

    def updateval(self):
        self.value = randint(self.min_val, self.max_val)