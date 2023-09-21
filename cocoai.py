import ast
import os
import click


class StatementCounter(ast.NodeVisitor):
    def __init__(self):
        self.statement_count = 0

    def generic_visit(self, node):
        if isinstance(node, ast.stmt):
            self.statement_count += 1
        super().generic_visit(node)


@click.command()
@click.argument('target_repo_path')
def main(target_repo_path):
    # Path to the cloned repository is now set from the command line

    file_data = []

    total_function_count = 0

    for foldername, subfolders, filenames in os.walk(target_repo_path):
        for filename in filenames:
            if filename.endswith(".py"):
                absolute_file_path = os.path.join(foldername, filename)
                relative_file_path = os.path.relpath(absolute_file_path, target_repo_path)

                with open(
                        absolute_file_path, "r", encoding="utf-8", errors="ignore") as file:
                    tree = ast.parse(file.read(), filename=absolute_file_path)

                    counter = StatementCounter()
                    counter.visit(tree)
                    statement_count = counter.statement_count
                    total_function_count += statement_count

                    file.seek(0)
                    line_count = statement_count
                    file_data.append((filename, relative_file_path, function_count, line_count))

    print("| Filename | Path | Number of Statements | Number of Lines |")
    print("| --- | --- | --- | --- |")
    for filename, path, statement_count, line_count in file_data:
        print(f"| {filename} | {path} | {statement_count} | {line_count} |")
    print(f"| Total |  | {total_function_count} |  |")

if __name__ == "__main__":
    main()
