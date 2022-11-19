from pulp import *

def main():
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    ROWS = COLS = range(len(sudoku))
    VALS = range(1, 10)

    def get_box_indices(index):
        start_row = (index // 3) * 3
        start_column = (index % 3) * 3
        return [(row, column) for row in range(start_row, start_row + 3) for column in range(start_column, start_column + 3)]

    def set_constraints(problem):
        for row in ROWS:
            for col in COLS:         
                # Starting numbers entered as constraints
                if sudoku[row][col] != 0:
                    problem += decision_vars[row][col][sudoku[row][col]] == 1
                # Every cell must have exactly one value
                problem += lpSum(decision_vars[row][col][val] for val in VALS) == 1
            for val in VALS:
                # Exactly one unique value per row
                problem += lpSum(decision_vars[row][col][val] for col in COLS) == 1
                # Exactly one unique value per col
                problem += lpSum(decision_vars[col][row][val] for col in COLS) == 1
                # Every 3x3 box must contain each value exactly once
                problem += lpSum(decision_vars[box_row][box_col][val] for box_row, box_col in get_box_indices(row)) == 1

    def print_sudoku():
        print("SUDOKU SOLUTION:")
        for row in ROWS:
            if row % 3 == 0 and row != 0:
                print("- - - - - - - - - - - - ")
            for col in COLS:
                for val in VALS:
                    if value(decision_vars[row][col][val]) == 1:
                        sudoku[row][col] = val
                if col % 3 == 0 and col != 0:
                    print(" | ", end="")
                if col == 8:
                    print(sudoku[row][col])
                else:
                    print(str(sudoku[row][col]) + " ", end="")

    # We don't need to specify minimize or maximize since there is no objective function (pulp creates dummy objective function)
    problem = LpProblem("Sudoku") 
    # There are 81 boxes in total and there can be value from 1 to 9 in each box (81 * 9 = 729 decision vars)
    decision_vars = LpVariable.dicts("x", indices=(ROWS, COLS, VALS), cat="Binary")
    set_constraints(problem)
    # Write formulation of the problem to file
    problem.writeLP("sudoku.lp")
    problem.solve()
    print(f"Status: {LpStatus[problem.status]}")
    # Print solved sudoku
    print_sudoku()

if __name__ == "__main__":
    main()