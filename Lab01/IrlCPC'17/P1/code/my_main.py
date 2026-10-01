# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------

import sys
import codecs

BOMB = 'x'


# ------------------------------------------
# 1. FUNCTION parse_in
# ------------------------------------------
def parse_in(input_file_name):
    file = open(input_file_name, "r", encoding='utf-8', errors='ignore')
    line = file.readline().strip().split(" ")
    num_rows = int(line[0])
    num_columns = int(line[1])
    matrix = [[] for _ in range(num_rows)]
    for row_i in range(num_rows):
        line = file.readline().strip().split(" ")
        for col_i in range(num_columns):
            matrix[row_i].append(line[col_i])
    file.close()
    return num_rows, num_columns, matrix


# ------------------------------------------
# 2. FUNCTION parse_out
# ------------------------------------------
def parse_out(output_file_name, num_rows, num_columns, sol_matrix):
    file = open(output_file_name, "w", encoding='utf-8', errors='ignore')
    for row in sol_matrix:
        file.write(" ".join(map(str, row)) + "\n")
    file.close()

def check_square(num_rows, num_columns, row, col, matrix):
    surrounding = 0
    row_gt_0 = row > 0
    row_lt_len = row < num_rows - 1
    col_gt_0 = col > 0
    col_lt_len = col < num_columns - 1
    if row_gt_0 and col_gt_0 and matrix[row - 1][col - 1] == BOMB:
        surrounding += 1
    if row_gt_0 and col_lt_len and matrix[row - 1][col + 1] == BOMB:
        surrounding += 1
    if row_gt_0 and matrix[row - 1][col] == BOMB:
        surrounding += 1
    if col_gt_0 and matrix[row][col - 1] == BOMB:
        surrounding += 1
    if col_lt_len and matrix[row][col + 1] == BOMB:
        surrounding += 1
    if row_lt_len and col_lt_len and matrix[row + 1][col + 1] == BOMB:
        surrounding += 1
    if row_lt_len and col_gt_0 and matrix[row + 1][col - 1] == BOMB:
        surrounding += 1
    if row_lt_len and matrix[row + 1][col] == BOMB:
        surrounding += 1

    return surrounding

# ------------------------------------------
# 3. FUNCTION solve
# ------------------------------------------
def solve(num_rows, num_columns, matrix):
    for row_i in range(num_rows):
        for col_i in range(num_columns):
            if matrix[row_i][col_i] == BOMB:
                continue
            matrix[row_i][col_i] = check_square(num_rows, num_columns, row_i, col_i, matrix)

    return matrix


# ------------------------------------------
# FUNCTION my_main
# ------------------------------------------
def my_main(input_file_name, output_file_name):
    # 1. We do the parseIn from the input file
    (num_rows, num_columns, matrix) = parse_in(input_file_name)

    # 2. We do the strategy to solve the problem
    sol_matrix = solve(num_rows, num_columns, matrix)

    # 3. We do the parse out to the output file
    parse_out(output_file_name, num_rows, num_columns, sol_matrix)


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now its time to apply this knowledge.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer finally processes this PYTHON PROGRAM EXECUTION section, which:
# (i) Specifies the function F to be executed.
# (ii) Define any input parameter such this function F has to be called with.
#
# --------------------------------------------------------
if __name__ == '__main__':
    # 1. We use as many input arguments as needed
    input_file_name = "../input_files/input_3.txt"
    output_file_name = "../results/output.txt"

    if (len(sys.argv) > 1):
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

    # 2. We solve the problem
    my_main(input_file_name, output_file_name)

