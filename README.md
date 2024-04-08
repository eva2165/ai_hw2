# Sudoku Solver
This is a homework submission for COMSW4701 Artificial Intelligence.

There is one file, `sudoku.py`. It can solve a sudoku board as a single argument, e.g. `python sudoku.py <input_string>`. If given no argument, it will solve the list of boards located in `sudokus_start.txt` and write the solutions to `output.txt` (the format of each is one string representation of a board per line).

A Sudoku board's representation in input/output is a string concatenation of each tile in row-major order, where an empty tile is a 0.
