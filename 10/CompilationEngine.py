import JackTokenizer


class compilationengine(object):
    '''readAndWrite/tokenPrefetch'''
    def __init__(self, wfile):
        self._wfile = wfile
        
    def compileVarDec(self, jackTokens):
        #'var'type varName (','varName)*';'
        self._wfile.write('  <varDec>\n  <keyword> var </keyword>\n')  #'var'
        jackTokens.advance()
        token = jackTokens.cur_token
        while token != ';':
            jackTokens.writeToken()
            jackTokens.advance()
            token = jackTokens.cur_token
        jackTokens.writeToken() #';'

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
        jackTokens.advance()
        jackTokens.writeToken() #('void'|type)
        jackTokens.advance()
        jackTokens.writeToken() #subroutineName
        jackTokens.advance()
        jackTokens.writeToken() #'('
        self.compileParameterList(jackTokens)
        jackTokens.writeToken() #')'
        self.compileSubroutineBody(jackTokens)
        self._wfile.write('  <subroutineDec>\n')
        
    def compileParameterList(self, jackTokens):
        #((type varName)(','type varName)*)?
        self._wfile.write('  <parameterList>\n')
        jackTokens.advance()
        token = jackTokens.cur_token
        while token != ')':
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
        self._wfile.write('  ')
        jackTokens.writeToken() # ('static'|'field')
        jackTokens.advance()
        token = jackTokens.cur_token
        while token != ';':
            self._wfile.write('  ')
            jackTokens.writeToken()
            jackTokens.advance()
            token = jackTokens.cur_token
        self._wfile.write('  ')
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
                jackTokens.advance()
                jackTokens.writeToken() #'['
                self.compileExpression(jackTokens) #expression
                jackTokens.writeToken() #']'
            elif temp == '(':
                self.compileSubroutineCall(jackTokens)
            else:
                jackTokens.writeToken()
        elif token in ('-','~'):
            jackTokens.writeToken()
            self.compileTerm(jackTokens)
        elif token == '(':
            jackTokens.writeToken()
            self.compileExpression(jackTokens)
            jackTokens.writeToken()
        else:
            jackTokens.writeToken()
        self._wfile.write('  </term>\n')

    def compileSubroutineCall(self, jackTokens):
        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp == '.':
            jackTokens.writeToken() #(className|varName)
            jackTokens.advance()
            jackTokens.writeToken() #'.'
            jackTokens.advance()
            jackTokens.writeToken() #subroutineName
            jackTokens.advance()
            jackTokens.writeToken() #'('
            
            self.compileExpressionList(jackTokens) #expressionList
            jackTokens.writeToken() #')'
            
        elif temp == '(':
            jackTokens.writeToken() #subroutineName
            jackTokens.advance()
            jackTokens.writeToken() #'('
            self.compileExpressionList(jackTokens) #expressionList
            jackTokens.writeToken() #')'
            

    def compileExpression(self, jackTokens):
        self._wfile.write('  <expression>\n')
        self.compileTerm(jackTokens)
        jackTokens.advance()
        token = jackTokens.cur_token
        while token in ('+','-','*','/','&','|','<','>','='):
            jackTokens.writeToken()
            self.compileTerm(jackTokens)
            jackTokens.advance()
            token = jackTokens.cur_token
        self._wfile.write('  </expression>\n')

    def compileExpressionList(self, jackTokens):
        #(expression(','expression)*)?
        self._wfile.write('  <expressionList>\n')
        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp != ')':
            self.compileExpression(jackTokens)
        elif temp == ')':    #__空集的状态要记得判断
            jackTokens.advance()
        token = jackTokens.cur_token
        while token == ',':
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
        
        
        self._wfile.write('  </doStatement>\n')

    def compileLet(self, jackTokens):
        self._wfile.write('  <letStatement>\n')
        
        jackTokens.writeToken() #'let'
        jackTokens.advance()
        jackTokens.writeToken() #varName
        jackTokens.advance()
        token = jackTokens.cur_token
        if token == '[':
            jackTokens.writeToken() #'['
            self.compileExpression(jackTokens) #expression
            jackTokens.writeToken() #']'
            jackTokens.advance()
        jackTokens.writeToken() #'='
        self.compileExpression(jackTokens) #expression
        jackTokens.writeToken() #';'
        
        self._wfile.write('  </letStatement>\n')

    def compileIf(self, jackTokens):
        self._wfile.write('  <ifStatement>\n')
        
        jackTokens.writeToken() #'if'
        
        jackTokens.advance()
        jackTokens.writeToken() #'('
        self.compileExpression(jackTokens) #'expression'
        jackTokens.writeToken() #')'
        jackTokens.advance()
        jackTokens.writeToken() #'{'
        self.compileStatements(jackTokens)
        jackTokens.writeToken() #'}'
        
        temp = jackTokens.tokens[jackTokens.cur_line + 1]
        if temp == 'else':
            jackTokens.advance()
            jackTokens.writeToken() #('else'
            jackTokens.advance()
            jackTokens.writeToken() #'{'
            self.compileStatements(jackTokens) #statments
            jackTokens.writeToken() #'}'
        self._wfile.write('  </ifStatement>\n')

    def compileWhile(self, jackTokens):
        self._wfile.write('  <whileStatement>\n')
        
        jackTokens.writeToken() #'while'
        jackTokens.advance()
        jackTokens.writeToken() #'('
        self.compileExpression(jackTokens)
        jackTokens.writeToken() #')'
        jackTokens.advance()
        jackTokens.writeToken() #'{'
        self.compileStatements(jackTokens)
        jackTokens.writeToken() #'}'
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
        
        self._wfile.write('  <returnStatement>\n')
        
        
            
        
