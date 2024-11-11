"""
A linter that simply detects places where list comprehensions could be utilized

List comprehensions are typically:

- Faster
- Less lines of code

There's a few spots where list comprehensions can be used:

- Replacing a for loop
- Replacing a map function

We are currently just focused on identifying the for loop instances

Detection Algorithm:

1.) a for loop
2a.) an optional filter (e.g. if iter_item > 10 )
2b.) a single modifying expression to the iter_item (e.g. iter_item = iter_item.strip())
2c.) an append to an existing empty list (arr.append(iter_item))
     This can either be arr += iter_item or arr.append(iter_item)
"""

import ast


TEST_FILE = "test.py"

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


if __name__ == "__main__":
    file_contents = open(TEST_FILE, "r").read()
    tree = ast.parse(file_contents)
    ListComprehensionFinder().visit(tree)
