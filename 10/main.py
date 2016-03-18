import JackTokenizer
tokenizer = JackTokenizer.jacktokenizer(r"C:\Users\Liu_100\Desktop\nand2tetris\nand2tetris\projects\10\Square\SquareGame.jack")
tokenizer._wfile.write("<tokens>\n")

while(tokenizer.hasMoreTokens()):
    tokenizer.advance()
    tokenizer.writeToken()
tokenizer._wfile.write("</tokens>")
tokenizer._wfile.close()
