import sys
from antlr4 import *
from MiniCLexer import MiniCLexer
from MiniCParser import MiniCParser
from MiniCListener import MiniCListener


def main(argv):
    input = FileStream(argv[1])
    lexer = MiniCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = MiniCParser(stream)
    tree = parser.program()
    listner = MiniCListener()
    walker = ParseTreeWalker()
    walker.walk(listner, tree)
    
    
    

if __name__ == '__main__':
    main(sys.argv)
