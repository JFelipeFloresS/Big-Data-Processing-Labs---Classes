"""Train a random forest to predict Dublin bus delays with Spark ML."""
from pyspark.sql import SparkSession, functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

from bus_features import (load_bus_data, add_features, add_lag_features,
                          FEATURE_COLS)

DATA_PATH = "../Lab02/my_dataset_complete_31_files/"
MODEL_PATH = "/home/Lab03/bus_delay_model"
SAMPLE_FRACTION = 0.1   # set to None for the final run on the full month

spark = (SparkSession.builder
         .appName("BusDelayML")
         .config("spark.driver.memory", "4g")
         .config("spark.sql.shuffle.partitions", "48")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

# ---------------------------------------------------------------------------
# Data and features
# ---------------------------------------------------------------------------
df = load_bus_data(spark, DATA_PATH)

# Label must be present for training; lag is computed before sampling so
# each vehicle's consecutive pings are still together.
df2 = add_lag_features(add_features(df).dropna(subset=["delay"]))

if SAMPLE_FRACTION:
    df2 = df2.sample(fraction=SAMPLE_FRACTION, seed=42)

# Time-based split: train on Jan 1-24, test on Jan 25-31 (a full week)
train = df2.filter(F.col("day") <= 24).cache()
test = df2.filter(F.col("day") > 24)

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
indexer = StringIndexer(inputCol="bus_line", outputCol="line_idx",
                        handleInvalid="keep")
encoder = OneHotEncoder(inputCols=["line_idx"], outputCols=["line_vec"])
assembler = VectorAssembler(inputCols=FEATURE_COLS, outputCol="features")
rf = RandomForestRegressor(featuresCol="features", labelCol="delay",
                           numTrees=20, maxDepth=8, seed=42)

pipeline = Pipeline(stages=[indexer, encoder, assembler, rf])
model = pipeline.fit(train)

# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
preds = model.transform(test)
evaluator = RegressionEvaluator(labelCol="delay", predictionCol="prediction")

rmse = evaluator.evaluate(preds, {evaluator.metricName: "rmse"})
mae = evaluator.evaluate(preds, {evaluator.metricName: "mae"})

# Baseline 1: always predict the training mean
mean_delay = train.agg(F.avg("delay")).first()[0]
base_mean = test.withColumn("prediction", F.lit(mean_delay))
mean_rmse = evaluator.evaluate(base_mean, {evaluator.metricName: "rmse"})

# Baseline 2: predict that the delay stays what it was at the last ping
base_prev = test.withColumn("prediction", F.col("prev_delay").cast("double"))
prev_rmse = evaluator.evaluate(base_prev, {evaluator.metricName: "rmse"})

print(f"Model RMSE:                  {rmse/60:.2f} min")
print(f"Model MAE:                   {mae/60:.2f} min")
print(f"Baseline RMSE (mean delay):  {mean_rmse/60:.2f} min")
print(f"Baseline RMSE (prev delay):  {prev_rmse/60:.2f} min")

# Which features the forest relied on most (line_vec is expanded into one
# slot per bus line, so it's summed into a single figure here)
importances = model.stages[-1].featureImportances.toArray()
n_scalar = len(FEATURE_COLS) - 1
print("\nFeature importances:")
for name, value in zip(FEATURE_COLS[:n_scalar], importances[:n_scalar]):
    print(f"  {name:12s} {value:.3f}")
print(f"  {'bus_line':12s} {importances[n_scalar:].sum():.3f}")

model.write().overwrite().save(MODEL_PATH)
print(f"\nModel saved to {MODEL_PATH}")

spark.stop()