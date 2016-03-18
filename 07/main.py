import parser07
import codeWriter
codewrite = codeWriter.CodeWriter()
wfile = codewrite.setFileName(r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\07\StackArithmetic\SimpleAdd\SimpleAdd.vm")
parser = parser07.Parser(r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\07\StackArithmetic\SimpleAdd\SimpleAdd.vm")
while parser.hasMoreCommands():
    if parser.commandType() == 'C_PUSH':
        codewrite.writePushPop(wfile, 'C_PUSH', parser.arg1(), parser.arg2())
        
    elif parser.commandType() == 'C_ARITHMETIC':
        codewrite.writeArithmetic(wfile, parser.arg1())
    parser.advance()
wfile.close() 
