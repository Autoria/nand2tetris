import Parser
import Code
parser = Parser.Parser(r'C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\06\add\add.asm')
output_file = open(r'C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\06\prog.txt','w')
code = Code.Code()
while parser.hasMoreCommands():
    parser.advance()
    if not parser.hasMoreCommands():
        break
    if parser.commandType() is parser.A_COMMAND:
        #print (parser.symbol())
        output = code.gen_a_code(parser.symbol())
        output_file.write(output+'\n')
        print(output) #
        continue
    if parser.commandType() is parser.C_COMMAND:
        #print (parser.dest()+'='+parser.comp())
        output = code.gen_c_code(parser.comp(), parser.dest(), '')
        output_file.write(output+'\n')
        print(output) #
output_file.close()
