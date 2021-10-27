# Satdoku

Satdoku is a set of Python scripts that are useful to solve Sudoku problems
using a SAT solver.

These scripts are based on SDK and DIMACS formats.

There are three scripts:

- *sdk2cnf.py*: produce a CNF formula encoding the given sudoku problem.
- *model2sdk.py*: produce a sudoku grid associated to a given SAT model.
- *sdk2latex.py*: produce a LaTeX tabular repsenting the given sudoku grid.
