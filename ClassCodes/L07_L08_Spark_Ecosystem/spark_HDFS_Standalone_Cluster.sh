#!/bin/bash 
#
# ---------------------------------------
# 1. We use SSH to connect to localhost
# ---------------------------------------
#
ssh localhost
#
# ---------------------------------------
# 2. We start HDFS
# ---------------------------------------
#
hdfs namenode -format
start-dfs.sh
#
# ---------------------------------------
# 3. We create the folder where we are going to work at
# ---------------------------------------
#
hdfs dfs -mkdir /user/
hdfs dfs -mkdir /user/my_HDFS/
#
# --------------------------------------------------
# 4. We add our dataset to the HDFS working folder
# --------------------------------------------------
#
hdfs dfs -put ./my_dataset/ /user/my_HDFS/my_dataset
#
# --------------------------------------------------
# 5. We start the Spark Standalone Cluster Manager
# --------------------------------------------------
#
start-master.sh
start-worker.sh spark://CK-BTC-T2NNFN:7077
#
# --------------------------------------------------
# 6. We trigger the Spark Application
# --------------------------------------------------
#
# 6.1. We run the program, locally, using Python directly
#
python3.13 ./word_count.py ./my_dataset/ ./my_result/
#
# 6.2. We run the program, locally, using spark-submit
#
spark-submit --master "local[*]" ./word_count.py ./my_dataset/ ./my_result/
#
# 6.3. We run the program, on top of a HDFS in pseudo-distributed mode
#
spark-submit --master "local[*]" ./word_count.py /user/my_HDFS/my_dataset/ /user/my_HDFS/my_result/
#
# 6.4. We run the program, on top of a HDFS, and using the Spark Standalone cluster manager
#
spark-submit --master spark://CK-BTC-T2NNFN:7077 ./my_Spark_Core_Word_Count.py /user/my_HDFS/my_dataset/ /user/my_HDFS/my_result/
spark-submit --master spark://CK-BTC-T2NNFN:7077 --total-executor-cores 10 --executor-cores 5 ./my_Spark_Core_Word_Count.py /user/my_HDFS/my_dataset/ /user/my_HDFS/my_result/
spark-submit --master spark://CK-BTC-T2NNFN:7077 --deploy-mode client ./word_count.py /user/my_HDFS/my_dataset/ /user/my_HDFS/my_result/
#
spark-submit \
  --master spark://CK-BTC-T2NNFN:7077 \
  --total-executor-cores 8 \
  --executor-cores 4 \
  --executor-memory 12G \
  --driver-memory 2G \
  ./my_Spark_Core_Word_Count.py \
  hdfs://localhost:9000/user/my_HDFS/my_dataset/ \
  hdfs://localhost:9000/user/my_HDFS/my_result/
#
spark-submit \
  --master spark://CK-BTC-T2NNFN:7077 \
  --total-executor-cores 8 \
  --executor-cores 2 \
  --executor-memory 6G \
  --driver-memory 2G \
  ./my_Spark_Core_Word_Count.py \
  hdfs://localhost:9000/user/my_HDFS/my_dataset/ \
  hdfs://localhost:9000/user/my_HDFS/my_result/
#
spark-submit \
  --master spark://CK-BTC-T2NNFN:7077 \
  --total-executor-cores 8 \
  --executor-cores 2 \
  --executor-memory 2G \
  --driver-memory 2G \
  ./my_Spark_Core_Word_Count.py \
  hdfs://localhost:9000/user/my_HDFS/my_dataset/ \
  hdfs://localhost:9000/user/my_HDFS/my_result/
#
# ---------------------------------------------------------
# 7. We bring the result back to our local file system
# ---------------------------------------------------------
#
hdfs dfs -get /user/my_HDFS/my_result ./
#
# -------------------------------------------------------------------------------------
# 8. We remove the HDFS result folder, to try run the program with new configurations
# -------------------------------------------------------------------------------------
#
hdfs dfs -rm -r /user/my_HDFS/my_result/
#
# ------------------------------------------------------
# 9. We remove the HDFS folder we have been working at
# ------------------------------------------------------
#
hdfs dfs -rm -r /user
#
# ---------------------------------------------------
# 10. We stop the Spark Standalone Cluster Manager
# ---------------------------------------------------
#
stop-workers.sh
stop-master.sh
#
# ---------------------------------------
# 11. We stop HDFS
# ---------------------------------------
#
stop-dfs.sh
#
