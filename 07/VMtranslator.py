import parser07
import codeWriter
codewrite = codeWriter.CodeWriter()
wfile = codewrite.setFileName(r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\07\MemoryAccess\PointerTest\PointerTest.vm")
parser = parser07.Parser(r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\07\MemoryAccess\PointerTest\PointerTest.vm")
wfile.write('@256\nD=A\n@SP\nM=D\n')
filename = 'StaticTest.vm'
while parser.hasMoreCommands():
    if parser.commandType() == 'C_PUSH':
        codewrite.writePushPop(wfile, parser.commandType(), parser.arg1(), parser.arg2(), filename)
    elif parser.commandType() == 'C_POP':
        codewrite.writePushPop(wfile, parser.commandType(), parser.arg1(), parser.arg2(), filename)
    elif parser.commandType() == 'C_ARITHMETIC':
        codewrite.writeArithmetic(wfile, parser.arg1())
    parser.advance()
wfile.close() 
