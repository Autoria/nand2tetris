import JackTokenizer


class compilationengine(object):
    '''readAndWrite/tokenPrefetch'''
    WHILE_FLAG = 0
    IF_FLAG = 0
    JACK_OS = ('Math',  'Array',  'Output', 'Screen', 'Keyboard', 'Memory', 'Sys')
    def __init__(self, wfile, symbolTables, VMWriter):
        self._wfile = wfile
        self.symbolTables = symbolTables
        self.VMWriter = VMWriter
        
    def compileVarDec(self, jackTokens):
        #'var'type varName (','varName)*';'
        self._wfile.write('  <varDec>\n  <keyword> var </keyword>\n')  #'var'
        symbleKind = 'var'
        jackTokens.advance()
        jackTokens.writeToken() #type
        symbleType = jackTokens.cur_token
        jackTokens.advance()
        token = jackTokens.cur_token
        
        
        while token != ';':
            if token != ',':
                self.localNum += 1
                self.symbolTables.Define(token, symbleType, symbleKind)
            jackTokens.writeToken()
            jackTokens.advance()
            token = jackTokens.cur_token
        jackTokens.writeToken()#';'

        self._wfile.write('  </varDec>\n')

    def compileSubroutineBody(self, jackTokens):
        #'{' varDec* statements '}'
        self._wfile.write('  <subroutineBody>\n') 
        jackTokens.advance()
        jackTokens.writeToken() #write token '{'
        jackTokens.advance()
        token = jackTokens.cur_token
        while token == 'var':
            self.compileVarDec(jackTokens)
            jackTokens.advance()
            token = jackTokens.cur_token
        self.VMWriter.writeFunction(self.routineName, self.localNum)
        if self.routineType == 'constructor':
            self.VMWriter.writePush('constant', self.symbolTables.VarCount('field'))
            self.VMWriter.writeCall('Memory.alloc',1)
            self.VMWriter.writePop('pointer', 0)
        elif self.routineType == 'method':
            self.VMWriter.writePush('argument', 0)
            self.VMWriter.writePop('pointer', 0)
        self.compileStatements(jackTokens) #statements
        jackTokens.writeToken()            # '}' 
        self._wfile.write('  </subroutineBody>\n')
    def compileStatements(self, jackTokens):
        #statment*
        self._wfile.write('  <statements>\n')
        token = jackTokens.cur_token
        while token != '}':
            if token == 'let':
                self.compileLet(jackTokens)
            elif token == 'if':
                self.compileIf(jackTokens)
            elif token == 'while':
                self.compileWhile(jackTokens)
            elif token == 'do':
                self.compileDo(jackTokens)
            elif token == 'return':
                self.compileReturn(jackTokens)
            jackTokens.advance()
            token = jackTokens.cur_token
        self._wfile.write('  </statements>\n') 

    def compileSubroutineDec(self, jackTokens):
        #('constructor'|'function'|'method')('void'|type)subroutineName'('
        #parameterList')'subroutineBody
        self._wfile.write('  <subroutineDec>\n')
        jackTokens.writeToken() #('constructor'|'function'|'method')
        self.routineType = jackTokens.cur_token
        jackTokens.advance()
        jackTokens.writeToken() #('void'|type)
        self.routineReturnType = jackTokens.cur_token ####
        jackTokens.advance()
        jackTokens.writeToken() #subroutineName
        self.routineName = self.className +'.'+ jackTokens.cur_token
        jackTokens.advance()
        jackTokens.writeToken() #'('
        self.symbolTables.startSubroutine()
        if self.routineType == 'method':
            self.symbolTables.Define('this', self.className, 'argument')
        self.compileParameterList(jackTokens)
        jackTokens.writeToken() #')'
        self.localNum = 0
        self.IF_FLAG = 0
        self.WHILE_FLAG = 0
        self.compileSubroutineBody(jackTokens)
        self._wfile.write('  <subroutineDec>\n')
        
    def compileParameterList(self, jackTokens):
        #((type varName)(','type varName)*)?
        self._wfile.write('  <parameterList>\n')
        
        jackTokens.advance()
        token = jackTokens.cur_token
        
        while token != ')':
            if token != ',':
                
                symbolType = token
                jackTokens.writeToken() #type
                jackTokens.advance()
                jackTokens.writeToken() #varName
                symbolName = jackTokens.cur_token
                self.symbolTables.Define(symbolName, symbolType, 'argument')
            elif token == ',':
                
                jackTokens.writeToken()
            jackTokens.advance()
            token = jackTokens.cur_token
        self._wfile.write('  </parameterList>\n')
        
    def compileClass(self, jackTokens):
        #'class'classname'{'classVarDec*subroutineDec*'}'
        self._wfile.write('<class>\n')
        jackTokens.advance()
        jackTokens.writeToken() #'class'
        jackTokens.advance()
        jackTokens.writeToken() #className
        self.className = jackTokens.cur_token
        jackTokens.advance()
        jackTokens.writeToken() #'{'
        jackTokens.advance()
        token = jackTokens.cur_token
        while token in ('static','field'):
            self.compileClassVarDec(jackTokens) #'classVarDec'
            jackTokens.advance()
            token = jackTokens.cur_token
        while token != '}':
            self.compileSubroutineDec(jackTokens)#'subroutineDec'
            jackTokens.advance()
            token = jackTokens.cur_token
        jackTokens.writeToken() #'}'
        self._wfile.write('</class>\n')

    def compileClassVarDec(self, jackTokens):
        #('static'|'field')type varName(','varName)*';'
        self._wfile.write('  <classVarDec>\n')
        jackTokens.writeToken() # ('static'|'field')
        symbleKind = jackTokens.cur_token
        jackTokens.advance()
        token = jackTokens.cur_token 
        jackTokens.writeToken() #type
        symbleType = token
        jackTokens.advance()
        token = jackTokens.cur_token
        while token != ';':
            if token != ',':
                self.symbolTables.Define(token, symbleType, symbleKind)
            jackTokens.writeToken()
            jackTokens.advance()
            token = jackTokens.cur_token
        jackTokens.writeToken()#';'
        
        self._wfile.write('  </classVarDec>\n')

    def compileTerm(self, jackTokens):
        #
        self._wfile.write('  <term>\n')
        jackTokens.advance()
        token = jackTokens.cur_token
        tType = jackTokens.tokenType()
        if tType == 'IDENTIFIER':
            temp = jackTokens.tokens[jackTokens.cur_line + 1]
            if temp == '.':
                self.compileSubroutineCall(jackTokens)
            elif temp == '[':
                jackTokens.writeToken() #varName
                varName = jackTokens.cur_token
                jackTokens.advance()
                jackTokens.writeToken() #'['
                self.compileExpression(jackTokens) #expression
                jackTokens.writeToken() #']'
                self.VMWriter.writePush('local',  self.symbolTables.IndexOf(varName))
                self.VMWriter.writeArithmetic('add')
                self.VMWriter.writePop('pointer', 1)
                self.VMWriter.writePush('that', 0)
                
            elif temp == '(':
                self.compileSubroutineCall(jackTokens)
            else:
                jackTokens.writeToken()
                if token in self.symbolTables.subroutineSymbols:
                    if self.symbolTables.KindOf(token) == 'var':
                        self.VMWriter.writePush('local', self.symbolTables.IndexOf(token))
                    elif self.symbolTables.KindOf(token) == 'argument':
                        self.VMWriter.writePush('argument', self.symbolTables.IndexOf(token))
                elif token in self.symbolTables.classSymbols:
                    if self.symbolTables.KindOf(token) == 'field':
                        self.VMWriter.writePush('this', self.symbolTables.IndexOf(token))
                    elif self.symbolTables.KindOf(token) == 'static':
                        self.VMWriter.writePush('static', self.symbolTables.IndexOf(token))
                    
        elif token in ('-','~'):
            jackTokens.writeToken()
            unaryOp = jackTokens.cur_token
            self.compileTerm(jackTokens)
            if unaryOp == '-':
                self.VMWriter.writeArithmetic('neg')
            else:
                self.VMWriter.writeArithmetic('not')
        elif token == '(':
            jackTokens.writeToken()
            self.compileExpression(jackTokens)
            jackTokens.writeToken()
        else:
            jackTokens.writeToken()
            if jackTokens.cur_token.isdigit():
                self.VMWriter.writePush('constant', jackTokens.cur_token)
            elif jackTokens.cur_token == 'true':
                self.VMWriter.writePush('constant', 0)
                self.VMWriter.writeArithmetic('not')
            elif jackTokens.cur_token == 'false':
                self.VMWriter.writePush('constant', 0)
            elif jackTokens.cur_token == 'this':
                self.VMWriter.writePush('pointer', 0)
            elif jackTokens.cur_token == 'null':
                self.VMWriter.writePush('constant', 0)
            elif jackTokens.tokenType() == 'STRING_CONST':
                
                
                self.VMWriter.writePush('constant', len(jackTokens.cur_token.strip('""')))
                self.VMWriter.writeCall('String.new', 1)
                RES = jackTokens.cur_token.strip('"')
                while RES:
                    self.VMWriter.writePush('constant', ord(RES[0]))
                    self.VMWriter.writeCall('String.appendChar', 2)
                    RES = RES[1:]
                

        self._wfile.write('  </term>\n')

    def compileSubroutineCall(self, jackTokens):
        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp == '.':
            jackTokens.writeToken() #(className|varName)
            subroutineName = jackTokens.cur_token
            
            jackTokens.advance()
            jackTokens.writeToken() #'.'
            jackTokens.advance()
            jackTokens.writeToken() #subroutineName
            subroutineName = subroutineName+'.'+jackTokens.cur_token ### 
            jackTokens.advance()
            if subroutineName.split('.')[0] in self.symbolTables.subroutineSymbols:
                self.VMWriter.writePush('local', self.symbolTables.IndexOf(subroutineName.split('.')[0]))

            elif subroutineName.split('.')[0] in self.symbolTables.classSymbols:
                self.VMWriter.writePush('this', self.symbolTables.IndexOf(subroutineName.split('.')[0]))

            jackTokens.writeToken() #'('
            
            self.compileExpressionList(jackTokens) #expressionList
            jackTokens.writeToken() #')'
            if subroutineName.split('.')[0] in self.JACK_OS:
                self.VMWriter.writeCall(subroutineName, self.expressionNum)
            elif subroutineName.split('.')[0] in self.symbolTables.subroutineSymbols:
                subroutineName = self.symbolTables.TypeOf(subroutineName.split('.')[0]) + '.' + subroutineName.split('.')[1]
                self.expressionNum += 1
                self.VMWriter.writeCall(subroutineName, self.expressionNum)
            elif subroutineName.split('.')[0] in self.symbolTables.classSymbols:
                subroutineName = self.symbolTables.TypeOf(subroutineName.split('.')[0]) + '.' + subroutineName.split('.')[1]
                self.expressionNum += 1
                self.VMWriter.writeCall(subroutineName, self.expressionNum)
            else:
                self.VMWriter.writeCall(subroutineName, self.expressionNum)

        elif temp == '(':
            jackTokens.writeToken() #subroutineName
            subroutineName = jackTokens.cur_token
            jackTokens.advance()
            jackTokens.writeToken() #'('
            self.compileExpressionList(jackTokens) #expressionList
            jackTokens.writeToken() #')'
            self.VMWriter.writePush('pointer', 0) 
            self.expressionNum += 1
            self.VMWriter.writeCall(self.className + '.' + subroutineName, self.expressionNum)

    def compileExpression(self, jackTokens):
        self._wfile.write('  <expression>\n')
        self.compileTerm(jackTokens)
        jackTokens.advance()
        token = jackTokens.cur_token
        while token in ('+','-','*','/','&','|','<','>','='):
            jackTokens.writeToken()
            Operator = jackTokens.cur_token
            self.compileTerm(jackTokens)
            if Operator == '+':
                self.VMWriter.writeArithmetic('add')
            elif Operator == '-':
                self.VMWriter.writeArithmetic('sub')
            elif Operator == '*':
                self.VMWriter.writeCall('Math.multiply', 2)
            elif Operator == '/':
                self.VMWriter.writeCall('Math.divide', 2)
            elif Operator == '<':
                self.VMWriter.writeArithmetic('lt')
            elif Operator == '>':
                self.VMWriter.writeArithmetic('gt')
            elif Operator == '&':
                self.VMWriter.writeArithmetic('and')
            elif Operator == '=':
                self.VMWriter.writeArithmetic('eq')
            elif Operator == '|':
                self.VMWriter.writeArithmetic('or')
            jackTokens.advance()
            token = jackTokens.cur_token
        self._wfile.write('  </expression>\n')

    def compileExpressionList(self, jackTokens):
        #(expression(','expression)*)?
        self._wfile.write('  <expressionList>\n')
        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp != ')':
            self.compileExpression(jackTokens)
            self.expressionNum = 1
        elif temp == ')':    #__空集的状态要记得判断
            jackTokens.advance()
            self.expressionNum = 0
        token = jackTokens.cur_token
        while token == ',':
            self.expressionNum += 1
            jackTokens.writeToken() #','
            self.compileExpression(jackTokens)
            token = jackTokens.cur_token
            
        self._wfile.write('  </expressionList>\n')

    def compileDo(self, jackTokens):
        '''cur_token different from compileDo to compileTerm when call subroutinecall'''
        self._wfile.write('  <doStatement>\n')
        
        jackTokens.writeToken() #'do'
        jackTokens.advance()
        self.compileSubroutineCall(jackTokens) #subroutineCall
        jackTokens.advance()
        jackTokens.writeToken() #';'
        
        self.VMWriter.writePop('temp', 0)
        self._wfile.write('  </doStatement>\n')

    def compileLet(self, jackTokens):
        self._wfile.write('  <letStatement>\n')
        
        jackTokens.writeToken() #'let'
        jackTokens.advance()
        jackTokens.writeToken() #varName\
        self.varName = jackTokens.cur_token
        jackTokens.advance()
        token = jackTokens.cur_token
        self.OFFSET = False
        if token == '[':
            self.OFFSET = True
            jackTokens.writeToken() #'['
            self.compileExpression(jackTokens) #expression
            jackTokens.writeToken() #']'
            jackTokens.advance()
            if self.symbolTables.KindOf(self.varName) == 'var':
                self.VMWriter.writePush('local', self.symbolTables.IndexOf(self.varName))
            elif self.symbolTables.KindOf(self.varName) == 'argument':
                self.VMWriter.writePush('argument', self.symbolTables.IndexOf(self.varName))
            self.VMWriter.writeArithmetic('add')
            
            
        jackTokens.writeToken() #'='

        self.compileExpression(jackTokens) #expression
        
        if self.varName in self.symbolTables.subroutineSymbols:
            if self.symbolTables.KindOf(self.varName) == 'var':
                if self.symbolTables.TypeOf(self.varName) == 'Array':
                    if self.OFFSET:
                        self.VMWriter.writePop('temp', 0)
                        self.VMWriter.writePop('pointer', 1)
                        self.VMWriter.writePush('temp', 0)
                        self.VMWriter.writePop('that', 0)
                    else:
                        self.VMWriter.writePop('local', self.symbolTables.IndexOf(self.varName))
                else:
                        self.VMWriter.writePop('local', self.symbolTables.IndexOf(self.varName))
            elif self.symbolTables.KindOf(self.varName) == 'argument':
                if self.OFFSET:
                        self.VMWriter.writePop('temp', 0)
                        self.VMWriter.writePop('pointer', 1)
                        self.VMWriter.writePush('temp', 0)
                        self.VMWriter.writePop('that', 0)
                else:
                    self.VMWriter.writePop('argument', self.symbolTables.IndexOf(self.varName))
        elif self.varName in self.symbolTables.classSymbols:
            if self.symbolTables.KindOf(self.varName) == 'field':
                self.VMWriter.writePop('this',self.symbolTables.IndexOf(self.varName))
            elif self.symbolTables.KindOf(self.varName) == 'static':
                self.VMWriter.writePop('static',self.symbolTables.IndexOf(self.varName))
            
        jackTokens.writeToken() #';'
        
        self._wfile.write('  </letStatement>\n')

    def compileIf(self, jackTokens):
        self._wfile.write('  <ifStatement>\n')
        
        jackTokens.writeToken() #'if'
        
        jackTokens.advance()
        jackTokens.writeToken() #'('
        self.compileExpression(jackTokens) #'expression'
        jackTokens.writeToken() #')'
        tempFlag = self.IF_FLAG
        self.VMWriter.writeIf('IF_TRUE'+str(tempFlag))
        self.VMWriter.writeGoto('IF_FALSE'+str(tempFlag))
        self.VMWriter.writeLabel('IF_TRUE'+str(tempFlag))
        self.IF_FLAG += 1
        jackTokens.advance()
        jackTokens.writeToken() #'{'
        self.compileStatements(jackTokens)
        jackTokens.writeToken() #'}'

        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp == 'else':
            self.VMWriter.writeGoto('IF_END'+str(tempFlag))
        self.VMWriter.writeLabel('IF_FALSE'+str(tempFlag))
        if temp == 'else':
            jackTokens.advance()
            jackTokens.writeToken() #('else'
            jackTokens.advance()
            jackTokens.writeToken() #'{'
            self.compileStatements(jackTokens) #statments
            jackTokens.writeToken() #'}'
            self.VMWriter.writeLabel('IF_END'+str(tempFlag))
        self._wfile.write('  </ifStatement>\n')

    def compileWhile(self, jackTokens):
        self._wfile.write('  <whileStatement>\n')
        
        jackTokens.writeToken() #'while'
        self.VMWriter.writeLabel('WHILE_EXP' + str(self.WHILE_FLAG))
        tempFlag = self.WHILE_FLAG
        self.WHILE_FLAG += 1
        
        jackTokens.advance()
        jackTokens.writeToken() #'('
        self.compileExpression(jackTokens)
        self.VMWriter.writeArithmetic('not')
        self.VMWriter.writeIf('WHILE_END' + str(tempFlag))
        
        jackTokens.writeToken() #')'
        jackTokens.advance()
        jackTokens.writeToken() #'{'
        self.compileStatements(jackTokens)
        jackTokens.writeToken() #'}'
        
        self.VMWriter.writeGoto('WHILE_EXP' + str(tempFlag))
        self.VMWriter.writeLabel('WHILE_END' + str(tempFlag))
        self._wfile.write('  </whileStatement>\n')

    def compileReturn(self, jackTokens):
        self._wfile.write('  <returnStatement>\n')
        
        jackTokens.writeToken() #'return'
        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp != ';':
            self.compileExpression(jackTokens)
            jackTokens.writeToken() #';'
        else:
            jackTokens.advance()
            jackTokens.writeToken() #';'
        if self.routineReturnType == 'void':
            self.VMWriter.writePush('constant', 0)
        self.VMWriter.writeArithmetic('return')
        self._wfile.write('  <returnStatement>\n')
        
        
            
        
