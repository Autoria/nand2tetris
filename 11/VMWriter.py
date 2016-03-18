class VMWriter(object):
    def __init__(self,wfile):  
        self.Constructor(wfile)
    def Constructor(self,wfile):
        self.wfile = wfile
    def writePush(self, segment, index):
        self.wfile.write('push '+segment+' '+str(index)+'\n')
    def writePop(self, segment, index):
        self.wfile.write('pop '+segment+' '+str(index)+'\n')
    def writeArithmetic(self, command):
        self.wfile.write(command+'\n')
    def writeLabel(self, label):
        self.wfile.write('label '+label+'\n')
    def writeGoto(self, label):
        self.wfile.write('goto '+label+'\n')
    def writeIf(self, label):
        self.wfile.write('if-goto '+label+'\n')
    def writeCall(self, name, nArgs):
        self.wfile.write('call '+name+' '+str(nArgs)+'\n' )
    def writeFunction(self, name, nArgs):
        self.wfile.write('function '+name+' '+str(nArgs)+'\n')
    def close(self):
        self.wfile.close()
