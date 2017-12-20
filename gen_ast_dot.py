import textwrap
from parsing.parser import Parser
from parsing.lexer import Lexer
from parsing.ast import NodeVisitor


class ASTVisualizer(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
            node [shape=circle, fontsize=12, fontname="Courier", height=.1];
            ranksep=.3;
            edge [arrowsize=.5]
        
        """)]
        self.dot_body = []
        self.dot_footer = ['}']

    def visit_Num(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, node.value)
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

    def visit_BinOp(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, node.op.value)
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        self.visit(node.right)

        for child_node in (node.left, node.right):
            s = '    node{} -> node{}\n'.format(node.num, child_node.num)
            self.dot_body.append(s)

    def visit_UnaryOp(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, node.op.value)
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

        self.visit(node.expr)
        s = '    node{} -> node{}\n'.format(node.num, node.expr.num)
        self.dot_body.append(s)

    def visit_VariableAssignment(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, "Assignment")
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        self.visit(node.right)

        for child_node in (node.left, node.right):
            s = '    node{} -> node{}\n'.format(node.num, child_node.num)
            self.dot_body.append(s)

    def visit_VariableDeclaration(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, "Variable")
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

        self.visit(node.symbol)
        self.visit(node.type)
        if node.expr is not None:
            self.visit(node.expr)
            for child_node in (node.symbol, node.type, node.expr):
                s = '    node{} -> node{}\n'.format(node.num, child_node.num)
                self.dot_body.append(s)
        else:
            for child_node in (node.symbol, node.type):
                s = '    node{} -> node{}\n'.format(node.num, child_node.num)
                self.dot_body.append(s)

    def visit_FunctionDeclaration(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, "Function")
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

        self.visit(node.symbol)
        s = '    node{} -> node{}\n'.format(node.num, node.symbol.num)
        self.dot_body.append(s)
        if node.arguments is not None:
            s = '    node{} [label="{}"]\n'.format(self.ncount, "Arguments")
            self.dot_body.append(s)
            body_pos = self.ncount
            self.ncount += 1
            s = '    node{} -> node{}\n'.format(node.num, body_pos)
            self.dot_body.append(s)
            for argument in node.arguments:
                self.visit(argument)
                s = '    node{} -> node{}\n'.format(body_pos, argument.num)
                self.dot_body.append(s)
        self.visit(node.type)
        s = '    node{} -> node{}\n'.format(node.num, node.type.num)
        self.dot_body.append(s)
        if node.body is not None:
            s = '    node{} [label="{}"]\n'.format(self.ncount, "Body")
            self.dot_body.append(s)
            body_pos = self.ncount
            self.ncount += 1
            s = '    node{} -> node{}\n'.format(node.num, body_pos)
            self.dot_body.append(s)
            for statement in node.body:
                self.visit(statement)
                s = '    node{} -> node{}\n'.format(body_pos, statement.num)
                self.dot_body.append(s)

    def visit_Symbol(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

    def visit_Type(self, node):
        s = '    node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node.num = self.ncount
        self.ncount += 1

    def gendot(self):
        tree = self.parser.parse()
        s = '    node{} [label="{}"]\n'.format(self.ncount, "Root")
        self.dot_body.append(s)
        self.ncount += 1
        for statement in tree:
            self.visit(statement)
            s = '    node{} -> node{}\n'.format(1, statement.num)
            self.dot_body.append(s)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)


def main():
    lexer = Lexer("""
    
var a : Int = 3 * 3 + c / 2 * (4 + b)

    """)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.gendot()
    print(content)


if __name__ == "__main__":
    main()
