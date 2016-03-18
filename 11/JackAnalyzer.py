import JackTokenizer
import CompilationEngine
import os
import VMWriter
import SymbolTable
rfile = r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\11\Pong\Ball.jack"
xml = os.path.splitext(rfile)[0] + 'MyVersion.xml'
vm = os.path.splitext(rfile)[0] + 'MyVersion.vm'
xml = open(xml,'w')
vm = open(vm,'w')
jackTokenizer = JackTokenizer.jacktokenizer(rfile, xml)
vmWriter = VMWriter.VMWriter(vm)
symbolTable = SymbolTable.SymbolTable()
compiler = CompilationEngine.compilationengine(xml,symbolTable,vmWriter)
compiler.compileClass(jackTokenizer)

xml.close()
vmWriter.close()
