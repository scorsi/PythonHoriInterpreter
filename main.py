from parsing.lexer import Lexer
from parsing.parser import Parser
from analyzer.semanticanalyzer import SemanticAnalyzer
from analyzer.treeanalyzer import GlobalSymbolTableCreator
from symbol.symbol import VarSymbol, ValSymbol
from parsing.ast import FunctionDeclaration


def main():
    lexer = Lexer("""
    
func test(var aa : Int) : Int {
    aa
}

var a : Int = (2 + 3) / 2
var b : Int = a

func toto (val bb : Int) : Float {
    var c : Int = a
}

    """)
    parser = Parser(lexer)
    tree = parser.parse()

    global_symtab_generator = GlobalSymbolTableCreator()
    global_symtab_generator.visit(tree)

    global_table = global_symtab_generator.global_table

    print(global_symtab_generator.global_table)
    if len(global_symtab_generator.errors) > 0:
        for error in global_symtab_generator.errors:
            print("Error: %s" % error)
        print("Errors has been found. Execution stopped.")
        return

    semantic_analyzer = SemanticAnalyzer(global_table)
    for statement in tree:
        if isinstance(statement, FunctionDeclaration):
            semantic_analyzer.visit(statement)

    print(semantic_analyzer.get_stack().get_last_scope())

    for error in semantic_analyzer.errors:
        print("Error: %s" % error)
    for warning in semantic_analyzer.warnings:
        print("Warning : %s" % warning)
    if len(semantic_analyzer.errors) > 0:
        print("Errors has been found. Execution stopped.")


if __name__ == "__main__":
    main()
