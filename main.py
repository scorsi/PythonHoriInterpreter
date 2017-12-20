from parsing.lexer import Lexer
from parsing.parser import Parser
from analyzer.semanticanalyzer import SemanticAnalyzer
from analyzer.treeanalyzer import GlobalSymbolTableCreator
from interpreter.interpreter import Interpreter
from symbol.symbol import VarSymbol, ValSymbol
from parsing.ast import FunctionDeclaration


def main():
    lexer = Lexer("""

func main() : Int {
    var aze : Int = 3
    aze = aze * 3
    var b : Int = aze
}

    """)
    parser = Parser(lexer)
    tree = parser.parse()

    print("Start GlobalSymbolTable Creation")

    global_symtab_generator = GlobalSymbolTableCreator()
    global_symtab_generator.visit(tree)

    global_table = global_symtab_generator.global_table

    # print(global_table)
    if len(global_symtab_generator.errors) > 0:
        for error in global_symtab_generator.errors:
            print("Error: %s" % error)
        print("Errors has been found. Execution stopped.")
        return

    print("Start Semantic Analyze")

    semantic_analyzer = SemanticAnalyzer(global_table)
    for statement in tree:
        if isinstance(statement, FunctionDeclaration):
            semantic_analyzer.visit(statement)

    for error in semantic_analyzer.errors:
        print("Error: %s" % error)
    for warning in semantic_analyzer.warnings:
        print("Warning : %s" % warning)
    if len(semantic_analyzer.errors) > 0:
        print("Errors has been found. Execution stopped.")
        return

    print("Start Interpreter")

    interpreter = Interpreter(global_table)
    interpreter.interpret()


if __name__ == "__main__":
    main()
