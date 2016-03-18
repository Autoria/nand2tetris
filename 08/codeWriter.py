import os
SKIPNUM1=0
SKIPNUM2=0
RETURNFLAG=0
class CodeWriter(object):
    def __init__(self):
        pass
    def setFileName(self,filename):
        self.filename = filename
        self.filesplitext = os.path.splitext(filename)
        wfile = open(self.filesplitext[0] + '.asm', 'w')
        return wfile
    def writeArithmetic(self, wfile, command):
        global SKIPNUM1, SKIPNUM2
        if command == 'add':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n')
        elif command == 'sub':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n')
        elif command == 'neg':
            wfile.write('@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n')
        elif command == 'and':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M&D\n@SP\nM=M+1\n')
        elif command == 'or':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n')
        elif command == 'not':  
            wfile.write('@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n')
        elif command == 'eq':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n\
                        @TRUE'+str(SKIPNUM1)+'\nD;JEQ\nD=0\n@FALSE'+str(SKIPNUM2)+'\n0;JMP\n\
                        (TRUE'+str(SKIPNUM1)+')\nD=-1\n\
                        (FALSE'+str(SKIPNUM2)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            SKIPNUM1 += 1
            SKIPNUM2 += 1
        elif command == 'gt':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n\
                        @TRUE'+str(SKIPNUM1)+'\nD;JGT\nD=0\n@FALSE'+str(SKIPNUM2)+'\n0;JMP\n\
                        (TRUE'+str(SKIPNUM1)+')\nD=-1\n\
                        (FALSE'+str(SKIPNUM2)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            SKIPNUM1 += 1
            SKIPNUM2 += 1
        elif command == 'lt':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n\
                        @TRUE'+str(SKIPNUM1)+'\nD;JLT\nD=0\n@FALSE'+str(SKIPNUM2)+'\n0;JMP\n\
                        (TRUE'+str(SKIPNUM1)+')\nD=-1\n\
                        (FALSE'+str(SKIPNUM2)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            SKIPNUM1 += 1
            SKIPNUM2 += 1
    def writePushPop(self, wfile, command, segment, index, filename):
        if command == 'C_PUSH':
            if segment == 'constant':
                wfile.write('@'+str(index)+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'local':
                wfile.write('@LCL\nD=M\n@'+str(index)+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'argument':
                wfile.write('@ARG\nD=M\n@'+str(index)+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'this':
                wfile.write('@THIS\nD=M\n@'+str(index)+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'that':
                wfile.write('@THAT\nD=M\n@'+str(index)+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'pointer':
                if index == '0':
                    wfile.write('@3\n')
                elif index == '1':
                    wfile.write('@4\n')
                wfile.write('D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'static':
                staticname = filename.strip('.vm') + '.' + str(index)
                wfile.write('@'+str(staticname)+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'temp':
                wfile.write('@'+str(int(index) + 5)+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif command == 'C_POP':
            if segment == 'local':
                wfile.write('@SP\nM=M-1\nA=M\nD=M\n@LCL\nA=M\n')
                for i in range (0,int(index)):  
                    wfile.write('A=A+1\n') 
                wfile.write('M=D\n')
            elif segment == 'argument':
                wfile.write('@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\n')
                for i in range (0,int(index)):  
                    wfile.write('A=A+1\n')
                wfile.write('M=D\n')
            elif segment == 'this':
                wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THIS\nA=M\n')
                for i in range (0,int(index)):
                    wfile.write('A=A+1\n')
                wfile.write('M=D\n')
            elif segment == 'that':
                #wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THAT\nA=M\n')
                #for i in range (0,int(index)):  
                #    wfile.write('A=A+1\n')
                #wfile.write('M=D\n')                  
                wfile.write('@'+index+'\nD=A\n@THAT\nA=M+D\nD=M\n@SP\nM=M+1\nA=M\nD=M\n')

                
            elif segment == 'pointer':
                wfile.write('@SP\nM=M-1\nA=M\nD=M\n')
                if index == '0':
                    wfile.write('@3\n')
                elif index == '1':
                    wfile.write('@4\n')
                wfile.write('M=D\n')
            elif segment == 'temp':
                wfile.write('@SP\nM=M-1\nA=M\nD=M\n@'+str(5+int(index))+'\nM=D\n')
            elif segment == 'static':
                staticname = filename.strip('.vm')+'.'+str(index)
                wfile.write('@SP\nM=M-1\nA=M\nD=M\n@'+staticname+'\nM=D\n')
    def writeLabel(self, wfile, label):
        wfile.write('('+label+')\n')
    def writeIf(self, wfile, label):
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@'+label+'\nD;JNE\n')
    def writeGoto(self, wfile, label):
        wfile.write('@SP\nA=M-1\nD=M\n@'+label+'\nD;JMP\n')
    def writeFunction(self, wfile, functionName, numlocals):  
        wfile.write('('+functionName+')\n@LCL\nD=M\n@SP\nM=D\n')  
        for i in range(0,int(numlocals)):  
            wfile.write('@SP\nA=M\nM=0\nD=A+1\n@SP\nM=D\n')
    def writeReturn(self, wfile):
        wfile.write('@LCL\nD=M\n@R13\nM=D\n\
@5\nA=D-A\nD=M\n@R14\nM=D\n\
@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n\
@ARG\nD=M+1\n@SP\nM=D\n\
@R13\nA=M-1\nD=M\n@THAT\nM=D\n\
@13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n\
@13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n\
@13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n\
@14\nA=M\n0;JMP\n')


    def writeCall(self, wfile, functionName, numArgs):  
        global RETURNFLAG  
        wfile.write('@return_address'+str(RETURNFLAG)+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\
            \n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
            \n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
            \n@'+numArgs+'\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\
            \n@'+functionName+'\n0;JMP\n(return_address'+str(RETURNFLAG)+')\n')
        RETURNFLAG+=1 
    @staticmethod
    def close(wfile):
        wfile.close()
