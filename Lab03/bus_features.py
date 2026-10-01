"""Shared data loading and feature engineering for the bus delay model.

Imported by both spark_ml.py (training) and use_model.py (scoring), so the
features are always built the same way.
"""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

COLUMNS = ["date", "bus_line", "bus_line_pattern", "congestion",
           "longitude", "latitude", "delay", "vehicle_id",
           "closer_stop", "at_stop"]

# Columns fed into the VectorAssembler (line_vec is produced by the pipeline)
FEATURE_COLS = ["hour", "dow", "latitude", "longitude",
                "congestion", "at_stop", "prev_delay", "line_vec"]


def load_bus_data(spark, path):
    """Read the headerless SIRI CSV files and name the columns."""
    return (spark.read.csv(path, header=False, inferSchema=True)
            .toDF(*COLUMNS))


def add_features(df):
    """Time features, plus dropping rows missing any feature column."""
    return (df
        .withColumn("hour", F.hour("date"))
        .withColumn("dow", F.dayofweek("date"))
        .withColumn("day", F.dayofmonth("date"))
        .dropna(subset=["date", "bus_line", "vehicle_id", "latitude",
                        "longitude", "congestion", "at_stop"]))


def add_lag_features(df, max_gap_s=120):
    """Add the same vehicle's delay at its previous ping.

    Only keeps rows where the previous ping is at most max_gap_s seconds
    earlier, so the lag never crosses from one trip or day to the next.
    """
    w = Window.partitionBy("vehicle_id").orderBy("date")
    return (df
        .withColumn("prev_delay", F.lag("delay").over(w))
        .withColumn("prev_date", F.lag("date").over(w))
        .withColumn("gap_s",
                    F.col("date").cast("long") - F.col("prev_date").cast("long"))
        .filter(F.col("gap_s").between(1, max_gap_s))
        .dropna(subset=["prev_delay"]))