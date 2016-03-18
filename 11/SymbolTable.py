
class SymbolTable(object):
    
    def __init__(self):
        self.Constructor()
    def Constructor(self):
        self.classSymbols = {}
        self.subroutineSymbols = {}
        self.symbols = {'static':self.classSymbols ,'field':self.classSymbols,
                                  'argument':self.subroutineSymbols, 'var':self.subroutineSymbols}
        self.index = {'static':0, 'field':0, 'argument':0, 'var':0}
    def startSubroutine(self):
        self.subroutineSymbols.clear()
        self.index['argument'] = self.index['var'] = 0
    def Define(self, Name, Type, Kind):
        self.symbols[Kind][Name] = (Type, Kind, self.index[Kind])
        self.index[Kind] += 1
    def VarCount(self, Kind):
        return sum(1 for n,(t,k,i) in self.symbols[Kind].items() if k == Kind)
    def KindOf(self, name):
        if name in self.subroutineSymbols:
            return self.subroutineSymbols[name][1]
        elif name in self.classSymbols:
            return self.classSymbols[name][1]
        else:
            return None
    def TypeOf(self, name):
        if name in self.subroutineSymbols:
            return self.subroutineSymbols[name][0]
        elif name in self.classSymbols:
            return self.classSymbols[name][0]
        else:
            return None
    def IndexOf(self, name):
        if name in self.subroutineSymbols:
            return self.subroutineSymbols[name][2]
        elif name in self.classSymbols:
            return self.classSymbols[name][2]
        else:
            return None
