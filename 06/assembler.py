import sys
import Parser
import Code
import SymbolTable


class Assembler(object):
    """Assembler class"""
    def __init__(self, in_file):
        self.in_file = in_file
        self.out_file = self._get_out_file(in_file)
        self.symbol_table = SymbolTable.SymbolTable()
        self.symbol_address = 16

    def assemble(self):
        self.first_pass()
        self.second_pass()

    def first_pass(self):
        """for constructing symbol table"""
        parser = Parser.Parser(self.in_file)
        cur_address = 0
        while parser.hasMoreCommands():
            parser.advance()
            if not parser.hasMoreCommands():
                break
            if (parser.commandType() == parser.A_COMMAND 
                or parser.commandType() == parser.C_COMMAND):
                cur_address += 1
            elif parser.commandType() == parser.L_COMMAND:
                self.symbol_table.add_entry(parser.symbol(), cur_address)
    def second_pass(self):
        parser = Parser.Parser(self.in_file)
        outf = open(self.out_file, 'w')
        code = Code.Code()
        while parser.hasMoreCommands():
            parser.advance()
            if not parser.hasMoreCommands():
                break
            if parser.commandType() == parser.A_COMMAND:
                (outf.write(code.gen_a_code(self._get_address
                (parser.symbol())) + '\n'))
            elif parser.commandType() == parser.C_COMMAND:
                (outf.write(code.gen_c_code(parser.comp(), parser.dest(),
                parser.jump()) + '\n'))
            elif parser.commandType == parser.L_COMMAND:
                pass
        outf.close()

    def _get_address(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbol_table.get_address(symbol)

    @staticmethod
    def _get_out_file(in_file):
        if in_file.endswith('.asm'):
            return in_file.replace('.asm', '.hack')
        else:
            return in_file + '.hack'
def main():
    in_file = r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\06\max\max.asm"
    asm = Assembler(in_file)
    asm.assemble()
    
main()
