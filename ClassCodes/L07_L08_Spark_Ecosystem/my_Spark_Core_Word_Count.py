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


# ------------------------------------------
# IMPORTS
# ------------------------------------------
import sys
import pyspark
import re


# ------------------------------------------
# FUNCTION process_line
# ------------------------------------------
def process_line(line):
    # 1. We create the output variable
    res = []

    # 2. We get the words from line
    words = line.strip().split(" ")

    # 3. We clean the characters from each word
    clean_words = [ re.sub(r"[^a-zA-Z]", "", w).lower() for w in words ]

    # 4. We get only the non-empty words
    res = [ x for x in clean_words if x != "" ]

    # 5. We return res
    return res


# ------------------------------------------
# FUNCTION my_main
# ------------------------------------------
def my_main(sc,
            my_dataset_dir,
            my_result_dir
           ):

    # 1. Operation C1: 'textFile'
    inputRDD = sc.textFile( my_dataset_dir )

    # 2. Operation T1: 'map'
    wordsRDD = inputRDD.flatMap( process_line )

    # 3. Operation T2: 'map'
    pairsRDD = wordsRDD.map( lambda x: (x, 1) )

    # 4. Operation T3: 'reduceByKey'
    appearancesRDD = pairsRDD.reduceByKey( lambda x, y: x + y )

    # 5. Operation T4: 'sortBy'
    solutionRDD = appearancesRDD.sortBy( lambda x : (-1) * x[1] )

    # 6. Operation A1: 'saveAsTextFile'
    solutionRDD.saveAsTextFile( my_result_dir )

    # DEBUG. Operation A1: 'collect'
    # resVAL = solutionRDD.collect()
    # for item in resVAL:
    #     print(item)


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now it's time to apply this knowledge.
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
    my_dataset_dir = "./my_dataset/"
    my_result_dir = "./my_result/"

    if (len(sys.argv) > 1):
       my_dataset_dir = sys.argv[1]
       my_result_dir = sys.argv[2]

    # 2. We configure the Spark Context
    sc = pyspark.SparkContext.getOrCreate()
    sc.setLogLevel('WARN')

    # 3. We call our main function
    my_main(sc,
            my_dataset_dir,
            my_result_dir
           )


