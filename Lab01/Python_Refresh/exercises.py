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

# --------------
# IMPORTS
# --------------


#----------------------------------------------
# ex1
#----------------------------------------------
#
# The function prints your name by the screen.
# Example: In my case it will print Nacho Castineiras
#
def ex1():
	print("Felipe Flores")

#----------------------------------------------
# ex2
#----------------------------------------------
#
# The function declares a new variable res, assigns it to the sum of 'a' and 'b' and returns res.
# Example: If a = 3 and b = 5 then it returns 8 (which is 3 + 5)
# @param a: First Integer
# @param b: Second Integer
# @return Sum of a and b
#
def ex2(a, b):
	print("Input - a:", a, "-b:", b)
	res = a + b
	return res

# ----------------------------------------------
# ex3
# ----------------------------------------------
#
# The function receives 3 numbers and prints by screen the biggest of them.
# Example: If a = 3, b = 7 and c = 5, then it prints 7 (which is the biggest of the 3 numbers).
# @param a: First number
# @param b: Second number
# @param c: Third number
#
def ex3(a, b, c):
	print("Input - a:", a, "-b:", b, "-c:", c)
	m = max(a, b, c)
	print("Max:", m, "\n")

# ----------------------------------------------
# ex4
# ----------------------------------------------
#
# The function returns the sum of all numbers from 1 to n.
# Example: If n = 5, the function returns 15 (which is 1 + 2 + 3 + 4 + 5).
# @param n: Number we want to stop adding at
# @return Sum of all integers in [1..n]
#
def ex4(n):
	print("Input - n:", n)
	seq_arr = sum([i for i in range(1, n + 1)])
	return seq_arr

# ----------------------------------------------
# ex5
# ----------------------------------------------
#
# The function prints a pattern by screen.
# Example1: If n = 3, then it prints
# *
# **
# ***
# Example2: If n = 5, then it prints<
# *
# **
# ***
# ****
# *****
#
# @param n: Number of lines to be printed
#
def ex5(n):
	print("Input - n:", n)
	for i in range(1, n + 1):
		print('*' * i)
	print()

# ----------------------------------------------
# ex6
# ----------------------------------------------
#
# The function reverses a String and returns the String reversed.
# Example: If the String "Hello" is received, then it returns "olleH"
#
# @param s: String to be scanned.
# @return The reversed String.
#
def ex6(s):
	print("Input - s:", s)
	rev = s[::-1]
	return rev

# ----------------------------------------------
# ex7
# ----------------------------------------------
#
# NOTE: This exercise has been taken from CodeWars
# https://www.codewars.com/kata/sum-of-digits-slash-digital-root
# Description:
# A digital root is the recursive sum of all the digits in a number.
# Given n, take the sum of the digits of n.
# If that value has still more than one digit, continue reducing in this way until a single-digit number is produced.
# Example 1:
# ex7(16)
# 1 + 6
# 7
#
# Example 2:
# ex7(942)
# 9 + 4 + 2
# 15
# However, as 15 still contains more than one digit, we iterate again
# 1 + 5
# 6
#
# @param n: Number to apply its digital root to.
# @return res: Digital result of the number.
#
def ex7(n):
	print("Input - n:", n)
	while n > 9:
		ns = str(n)
		print("Adding:", ns)
		n = 0
		for i in ns:
			n += int(i)

	return n

# ---------------------------
# FUNCTON my_main
# ---------------------------
def my_main():
	# 1. We create extra variables for the results
	res1 = 0
	res2 = ""
		
	#---------------------
	# TESTS
	#---------------------
		
	#ex1
	print("----------- ex1 -----------")
	ex1()
		
	#ex2
	print("----------- ex2 -----------")
	res1 = ex2(2, 3)
	print(res1)
		
	res1 = ex2(5, 7)
	print(res1)
		
	#ex3
	print("----------- ex3 -----------")
	ex3(3, 7, 5)
	ex3(1, 2, 3)
		
	#ex4
	print("----------- ex4 -----------")
	res1 = ex4(5)
	print(res1)

	res1 = ex4(10)
	print(res1)
		
	#ex5
	print("----------- ex5 -----------")
	ex5(3)
		
	ex5(5)
		
	#ex6
	print("----------- ex6 -----------")
	res2 = ex6("Hello")
	print(res2)
		
	res2 = ex6("Goodbye")
	print(res2)
		
	#ex7
	print("----------- ex7 -----------")
	res1 = ex7(16)
	print(res1)
		
	res2 = ex7(942)
	print(res2)

	res3 = ex7(48654684656548651384684)
	print(res3)

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
	my_main()


