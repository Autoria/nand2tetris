import re
class Parser(object):
    _comment = re.compile(r'//.*$')
    Arith=('add','sub','neg','eq','gt','lt','and','or','not')  
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self._lines = file.read()
        self._lines = self._lines.split('\n')
        self.cur_command = ''
        self.cur_line = 0
        file.close()
    def hasMoreCommands(self):
        if (self.cur_line + 1) < len(self._lines):
            return True
        else:
            return False
    def advance(self):
        self.cur_line += 1
        line = self._lines[self.cur_line]
        line = re.sub(self._comment,'',line)
        print("curline:", self.cur_line, "line: ", line) ###
        if line == '' and self.hasMoreCommands():
            self.advance()
        else:
            self.cur_command = line.strip()

    def commandType(self):
        if self.cur_command.find('push') >= 0:
            return 'C_PUSH'
        elif self.cur_command.find('pop') >= 0:
            return 'C_POP'
        elif self.cur_command in self.Arith:
            return 'C_ARITHMETIC'
        elif self.cur_command.find('label') >= 0:
            return 'C_LABEL'
        elif self.cur_command.find('if-goto') >= 0:
            return 'C_IF'
        elif self.cur_command.find('goto') >= 0:
            return 'C_GOTO'
        elif self.cur_command.find('call') >= 0:
            return 'C_CALL'
        elif self.cur_command.find('function') >= 0:
            return 'C_FUNCTION'
        elif self.cur_command.find('return') >= 0:
            return 'C_RETURN'
        
    def arg1(self):
        if self.commandType() == 'C_ARITHMETIC':
            return self.cur_command
        else:
            stripped = self.cur_command.split(' ')
            return stripped[1]
    def arg2(self):
        if self.commandType() == 'C_PUSH' or 'C_POP' or 'C_FUNCTION' or 'C_CALL':
            stripped = self.cur_command.split(' ')
            return stripped[2]
