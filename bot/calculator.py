import ast
import operator

def ceval(expr: str) -> str:
    expr = expr.replace('^', '**')
    allowed_operators = {
        ast.Add: operator.add, 
        ast.Sub: operator.sub, 
        ast.Mult: operator.mul, 
        ast.Div: operator.truediv, 
        ast.Pow: operator.pow,
        ast.BitXor: operator.pow
    }

    class Eval(ast.NodeVisitor):
        def visit_BinOp(self, node):
            if type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](self.visit(node.left), self.visit(node.right))
            raise ValueError("Неподдерживаемая операция")
        
        def visit_Num(self, node):
            return node.n
        
        def visit_Expr(self, node):
            return self.visit(node.value)
        
    try:
        tree = ast.parse(expr, mode='eval')
        return Eval().visit(tree.body)
    except:
        return "Неправильное выражение"