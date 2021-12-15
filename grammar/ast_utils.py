from ast import NodeVisitor, AST, iter_fields, NodeTransformer
import inspect
import types
import ast


def transform_code(f, transformer):
  f_ast = ast.parse(inspect.getsource(f))
  new_tree = ast.fix_missing_locations(transformer.visit(f_ast))
  old_code = f.__code__
  code = compile(new_tree, old_code.co_filename, 'exec')
  new_f = types.FunctionType(code.co_consts[0], f.__globals__)
  return new_f


class ASTMagicNumberDetector(NodeVisitor):
    magic_numbers = 0

    def check_value(self, value):
        if value not in [0, 1, 1j]:
            self.magic_numbers += 1

    def visit_Num(self, node):
        if self.check_value(node.n):
            self.magic_numbers += 1

    def visit_Constant(self, node):
        if self.check_value(node.value):
            self.magic_numbers += 1


class ASTDotVisitor(NodeVisitor):
    def __init__(self):
        self.txt = "digraph{\n"
        self.n_node = 0

    def generic_visit(self, node, n=0):
        node_values = []
        for field, value in iter_fields(node):
            if not (isinstance(value, list) or isinstance(value, AST)):
                node_values.append(str(field) + "=" + repr(value))
        self.txt += f's{self.n_node} [label="{node.__class__.__name__}({", ".join(node_values)})"]\n'
        self.n_node += 1

        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.txt += f's{n} -> s{self.n_node} [label="{field}"]\n'
                        self.generic_visit(item, self.n_node)
            elif isinstance(value, AST):
                self.txt += f's{n} -> s{self.n_node} [label="{field}"]\n'
                self.generic_visit(value, self.n_node)

        if n == 0:
            self.txt += "\n}"
            print(self.txt)


class ASTReplaceNum(NodeTransformer):
    def __init__(self, n) -> None:
        super().__init__()
        self.n = n

    def visit_Num(self, node):
        node.n = self.n
        return node

    def visit_Constant(self, node):
        node.value = self.n
        return node


class ASTRemoveConstantIf(NodeTransformer):
    def visit_If(self, node):        
        if type(node.test) == ast.Constant:
            if node.test.value == True:
                return self.visit(node.body[0])
            elif node.test.value == False:
                return self.visit(node.orelse[0])
        return self.visit(node)
