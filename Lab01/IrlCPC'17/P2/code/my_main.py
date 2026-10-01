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


# ------------------------------------------
# 1. FUNCTION parse_in
# ------------------------------------------
def parse_in(input_file_name):
    file = open(input_file_name, "r", encoding='utf-8', errors='ignore')
    number_count = int(file.readline().strip())
    numbers = []
    line = file.readline().strip().split(" ")
    assert(len(line) == number_count)
    for i in range(number_count):
        numbers.append(int(line[i]))
    return numbers


# ------------------------------------------
# 2. FUNCTION parse_out
# ------------------------------------------
def parse_out(res, output_file_name):
    file = open(output_file_name, "w", encoding='utf-8', errors='ignore')
    out_str = " ".join(map(str, res))
    file.write(out_str)
    file.close()


def solve_number(num):
    roman_equivalent = {
        3000: 'MMM',
        2000: 'MM',
        1000: 'M',
        900: 'CM',
        800: 'DCCC',
        700: 'DCC',
        600: 'DC',
        500: 'D',
        400: 'CD',
        300: 'CCC',
        200: 'CC',
        100: 'C',
        90: 'XC',
        80: 'LXXX',
        70: 'LXX',
        60: 'LX',
        50: 'L',
        40: 'XL',
        30: 'XXX',
        20: 'XX',
        10: 'X',
        9: 'IX',
        8: 'VIII',
        7: 'VII',
        6: 'IV',
        5: 'V',
        4: 'IV',
        3: 'III',
        2: 'II',
        1: 'I',
    }

    res = ''

    for val in roman_equivalent:
        if num >= val:
            res += roman_equivalent[val]
            num -= val

    return res

# ------------------------------------------
# 3. FUNCTION solve
# ------------------------------------------
def solve(numbers):
    res = []
    for num in numbers:
        res.append(solve_number(num))

    print(res)

    return res


# ------------------------------------------
# FUNCTION my_main
# ------------------------------------------
def my_main(input_file_name, output_file_name):
    numbers = parse_in(input_file_name)

    res = solve(numbers)

    parse_out(res, output_file_name)


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
    input_file_name = "../input_files/input_2.txt"
    output_file_name = "../results/output.txt"

    if (len(sys.argv) > 1):
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

    # 2. We solve the problem
    my_main(input_file_name, output_file_name)

