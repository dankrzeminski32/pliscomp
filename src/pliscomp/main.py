import click
import ast

def get_list_comprehension_eq(new_list_var, iter_item_var, iterable_var, filter_expr=None):
    return new_list_var + " = [" + iter_item_var + " for " + iter_item_var + " in " + iterable_var + "]"

class ListComprehensionFinder(ast.NodeVisitor):
    def __init__(self):
        self.list_assignments = {} # storing var_name -> list value
        super().__init__()
    
    def visit_Assign(self, node):
        if isinstance(node.value, ast.List):
            self.list_assignments[node.targets[0].id] = node.value.elts
        self.generic_visit(node)

    def visit_For(self, node):
        for body_node in node.body:
            if isinstance(body_node, ast.Expr):
                if isinstance(body_node.value, ast.Call):
                    func_node = body_node.value.func
                    if isinstance(func_node, ast.Attribute):
                        if func_node.attr == "append":
                            if not self.list_assignments[func_node.value.id]:
                                print(get_list_comprehension_eq(func_node.value.id, node.target.id,node.iter.id))
        self.generic_visit(node)


@click.command()
@click.argument("filename")
def main(filename):
    file_contents = open(filename, "r").read()
    tree = ast.parse(file_contents)
    ListComprehensionFinder().visit(tree)

if __name__ == "__main__":
    main()
