from lexer import lexer
from parser import Parser
from interpreter import Interpreter

def main():
    print("\n`7MM\"\"\"YMM   .M\"\"\"bgd   .g8\"\"\"bgd `7MM\"\"\"Mq.  `7MMF'`7MM\"\"\"Mq. MMP\"\"MM\"\"YMM")
    print("  MM    `7  ,MI    \"Y .dP'     `M   MM   `MM.   MM    MM   `MM.P'   MM   `7")
    print("  MM   d    `MMb.     dM'       `   MM   ,M9    MM    MM   ,M9      MM")      
    print("  MMmmMM      `YMMNq. MM            MMmmdM9     MM    MMmmdM9       MM")     
    print("  MM   Y  , .     `MM MM.           MM  YM.     MM    MM            MM")    
    print("  MM     ,M Mb     dM `Mb.     ,'   MM   `Mb.   MM    MM            MM")    
    print(".JMMmmmmMMM P\"Ybmmd\"    `\"bmmmd'  .JMML. .JMM..JMML..JMML.        .JMML.\n")
    print("================================================================================\n")

if __name__ == '__main__':
    main()
    code = open('src/test.es', 'r').read()
    tokens = lexer(code)
    #print(list(tokens))
    parser = Parser(list(tokens))
    ast = parser.parse()
    i = Interpreter()
    i.eval(ast)