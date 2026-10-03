"""Train two random forests to predict Dublin bus delays with Spark ML.

- Structural model: time, place and line only. Used by structural_delays.py.
- Live model: also uses the vehicle's previous delay. Used for live prediction.
"""
from pyspark.sql import SparkSession, functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

from bus_features import (load_bus_data, add_features, add_lag_features,
                          STRUCTURAL_FEATURE_COLS, LIVE_FEATURE_COLS,
                          STRUCTURAL_MODEL_PATH, LIVE_MODEL_PATH)

DATA_PATH = "../Lab02/my_dataset_complete_31_files/"
SAMPLE_FRACTION = 0.1   # set to None for the final run on the full month

spark = (SparkSession.builder
         .appName("BusDelayML")
         .config("spark.driver.memory", "4g")
         .config("spark.sql.shuffle.partitions", "48")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

evaluator = RegressionEvaluator(labelCol="delay", predictionCol="prediction")


def rmse_of(df):
    return evaluator.evaluate(df, {evaluator.metricName: "rmse"})


def build_pipeline(feature_cols):
    indexer = StringIndexer(inputCol="bus_line", outputCol="line_idx",
                            handleInvalid="keep")
    encoder = OneHotEncoder(inputCols=["line_idx"], outputCols=["line_vec"])
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    rf = RandomForestRegressor(featuresCol="features", labelCol="delay",
                               numTrees=20, maxDepth=8, seed=42)
    return Pipeline(stages=[indexer, encoder, assembler, rf])


def train_and_evaluate(name, data, feature_cols, model_path):
    print(f"\n=== {name} model ===")
    if SAMPLE_FRACTION:
        data = data.sample(fraction=SAMPLE_FRACTION, seed=42)

    # Time-based split: train on Jan 1-24, test on Jan 25-31 (a full week)
    train = data.filter(F.col("day") <= 24).cache()
    test = data.filter(F.col("day") > 24)

    model = build_pipeline(feature_cols).fit(train)
    preds = model.transform(test)

    mae = evaluator.evaluate(preds, {evaluator.metricName: "mae"})
    print(f"Model RMSE:                  {rmse_of(preds)/60:.2f} min")
    print(f"Model MAE:                   {mae/60:.2f} min")

    mean_delay = train.agg(F.avg("delay")).first()[0]
    base_mean = test.withColumn("prediction", F.lit(mean_delay))
    print(f"Baseline RMSE (mean delay):  {rmse_of(base_mean)/60:.2f} min")

    if "prev_delay" in feature_cols:
        base_prev = test.withColumn("prediction",
                                    F.col("prev_delay").cast("double"))
        print(f"Baseline RMSE (prev delay):  {rmse_of(base_prev)/60:.2f} min")

    # line_vec is the last feature and expands to one slot per bus line,
    # so its slots are summed into a single bus_line figure
    importances = model.stages[-1].featureImportances.toArray()
    n_scalar = len(feature_cols) - 1
    print("Feature importances:")
    for col, value in zip(feature_cols[:n_scalar], importances[:n_scalar]):
        print(f"  {col:12s} {value:.3f}")
    print(f"  {'bus_line':12s} {importances[n_scalar:].sum():.3f}")

    model.write().overwrite().save(model_path)
    print(f"Saved to {model_path}")
    train.unpersist()


base = add_features(load_bus_data(spark, DATA_PATH)).dropna(subset=["delay"])

# Structural model: no lag, so every ping with a known delay is usable
train_and_evaluate("Structural", base, STRUCTURAL_FEATURE_COLS,
                   STRUCTURAL_MODEL_PATH)

# Live model: lag computed on the full data, before any sampling
train_and_evaluate("Live", add_lag_features(base), LIVE_FEATURE_COLS,
                   LIVE_MODEL_PATH)

spark.stop()