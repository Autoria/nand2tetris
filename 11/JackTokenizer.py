import re
import os
class jacktokenizer(object):
    _comment = re.compile(r'((//)(.*?)\n)|\n')
    _keyword = ('class','constructor','function','method','field','static','var',
               'int','char','boolean','void','true','false','null','this','let',
               'do','if','else','while','return')
    _symbol = ('{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~')
    def __init__(self, rfile, wfile):
        self.Constructor(rfile)
        self._wfile = wfile
    def Constructor(self, file_name):
        rfile = open(file_name, 'r')
        self.tokens = rfile.read()
        
        self.tokens = re.sub(self._comment, ' ', self.tokens)
        
        
        while '/*' in self.tokens:
            commentLeft = self.tokens.find('/*')
            commentRight = self.tokens.find('*/')
            left = self.tokens[:commentLeft]
            right = self.tokens[commentRight+2:]
            self.tokens = left+right
            commentLeft = self.tokens.find('/*')
        
        self.tokenList = []
        temp = ''
        INSTRING = 0
        for i in range(len(self.tokens)):
            cur_token = self.tokens[i]
            if INSTRING:
                if cur_token == '"':
                    temp += cur_token
                    self.tokenList.append(temp)
                    temp = ''
                    INSTRING = 0
                else:
                    temp += cur_token
            elif cur_token.isalpha():
                temp += cur_token
            elif cur_token.isdigit():
                temp += cur_token
            elif cur_token == '"':
                temp += cur_token
                INSTRING = 1
            else:
                if temp != '':
                    self.tokenList.append(temp)
                    temp = ''
                if cur_token in self._symbol:
                    self.tokenList.append(cur_token)

                
        self.tokens = self.tokenList
        print(self.tokens)
        self.cur_token = ''
        self.cur_line = -1
        rfile.close()
        print('len of tokens: %d' %(len(self.tokens)) )
    def hasMoreTokens(self):
        if (self.cur_line + 1) < len(self.tokens):
            return True
        else:
            return False
        
    def advance(self):
        self.cur_line += 1
        line = self.tokens[self.cur_line]
        if line == '' and self.hasMoreTokens():
            self.advance()
        else:
            self.cur_token = line
            
            
            

    def tokenType(self):
        if self.cur_token in self._keyword:
            return 'KEYWORD'
        elif self.cur_token in self._symbol:
            return 'SYMBOL'
        elif self.cur_token.isdigit():
            return 'INT_CONST'
        elif self.cur_token.isidentifier():
            return 'IDENTIFIER'
        elif '"' in self.cur_token:
            return 'STRING_CONST'

    def keyword(self):
        if self.tokenType() == 'KEYWORD':
            self._wfile.write('  <keyword> '+self.cur_token+' </keyword>\n')
    def symbol(self):
        if self.tokenType() == 'SYMBOL':
            if self.cur_token == '>':  
                self._wfile.write('  <symbol> &gt; </symbol>\n')  
            elif self.cur_token == '<':  
                self._wfile.write('  <symbol> &lt; </symbol>\n')  
            elif self.cur_token == '&':  
                self._wfile.write('  <symbol> &amp; </symbol>\n')  
            else:  
                self._wfile.write('  <symbol> '+self.cur_token+' </symbol>\n')
    def identifier(self):
        if self.tokenType() == 'IDENTIFIER':  
            self._wfile.write('  <identifier> '+self.cur_token+' </identifier>\n')
    def intVal(self):
        if self.tokenType() == 'INT_CONST':  
            self._wfile.write('  <integerConstant> '+self.cur_token+' </integerConstant>\n')  
    def stringVal(self):
        if self.tokenType() == 'STRING_CONST':  
            self._wfile.write('  <stringConstant> '+self.cur_token.strip('"')+' </stringConstant>\n')
    def writeToken(self):
        if self.tokenType() == 'KEYWORD':
            self.keyword()
        elif self.tokenType() == 'SYMBOL':
            self.symbol()
        elif self.tokenType() == 'IDENTIFIER':
            self.identifier()
        elif self.tokenType() == 'INT_CONST':
            self.intVal()
        elif self.tokenType() == 'STRING_CONST':
            self.stringVal()

