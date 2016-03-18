import JackTokenizer
import CompilationEngine
import os
rfile = r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\10\Square\Square.jack"
wfile = os.path.splitext(rfile)[0] + 'FinalVersion.xml'
wfile = open(wfile,'w')
jackTokenizer = JackTokenizer.jacktokenizer(rfile, wfile)
compiler = CompilationEngine.compilationengine(wfile)
compiler.compileClass(jackTokenizer)
wfile.close()

