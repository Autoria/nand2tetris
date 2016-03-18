import re
class Parser(object):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3
    _comment = re.compile(r'//.*$')

    def __init__(self, file_name):
        """Constructor"""
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
        print("curline:", self.cur_line , "line:",line)  ###
        if line == '' and self.hasMoreCommands():
            self.advance()
        else:
            self.cur_command = line.strip()
        
        
    def commandType(self):
        if re.match(r'^@.*',self.cur_command):
            return Parser.A_COMMAND
        elif re.match(r'^\(.*\)$',self.cur_command):
            return Parser.L_COMMAND
        else:
            return Parser.C_COMMAND
    def symbol(self):
        """A_COMMAND or L_COMMAND"""
        if self.commandType() is Parser.A_COMMAND:
            return re.match(r'(^@)(.*)', self.cur_command).group(2)
        if self.commandType() is Parser.L_COMMAND:
            return re.match(r'(^\()(.*)(\)$)',self.cur_command).group(2)
        else:
            print("you can't get that cus that's not a A_COMMAND or L_COMMAND")
    def dest(self):
        if self.commandType() is Parser.C_COMMAND:
            matched = re.match(r'^(.*)=.*$',self.cur_command)
            if not matched:
                dest = ''
            else:
                dest = matched.group(1)
            return dest
    def comp(self):
        if self.commandType() is Parser.C_COMMAND:
            matched = re.match(r'^.*=(.*$)',self.cur_command)
            if not matched:
                comp = ''
            else:
                comp = matched.group(1)
            return comp
    def jump(self):
    	if self.commandType() is Parser.C_COMMAND:
            matched = re.match(r'^.*;(\w+)$',self.cur_command)
            if not matched:
                jump = ''
            else:
                jump = matched.group(1)
            return jump
