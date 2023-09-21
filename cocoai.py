import ast
import os
import click


class FunctionCounter(ast.NodeVisitor):
    def __init__(self):
        self.function_count = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)


@click.command()
@click.argument('target_repo_path')
def main(target_repo_path):
    # Path to the cloned repository is now set from the command line

    function_count = 0

    for foldername, subfolders, filenames in os.walk(target_repo_path):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(foldername, filename)

                with open(
                        file_path, "r", encoding="utf-8", errors="ignore") as file:
                    tree = ast.parse(file.read(), filename=file_path)

                    counter = FunctionCounter()
                    counter.visit(tree)
                    function_count += counter.function_count

    print(f"Number of functions: {function_count}")

if __name__ == "__main__":
    main()
