"""Find structural (recurring) bus delays in the January 2013 Dublin data.

Four analyses:
  1. Consistency: line/hour/day-type combinations late (or early) on most days
  2. Expected delay map: the structural model's prediction for every
     line x hour x day of week, with congestion switched off
  3. Residuals: stops where buses run later than the model expects
  4. Delay gain: stops/hours where buses actually *gain* delay

Run spark_ml.py first so the structural model exists.
Results are written as CSV files under results/.
"""
from pyspark.sql import SparkSession, functions as F
from pyspark.ml import PipelineModel

from bus_features import (load_bus_data, add_features, add_lag_features,
                          STRUCTURAL_MODEL_PATH)

DATA_PATH = "../Lab02/my_dataset_complete_31_files/"
RESULTS_DIR = "/home/Lab03/results"

LATE_S = 300            # "late" = more than 5 minutes behind schedule
EARLY_S = -300          # "early" = more than 5 minutes ahead of schedule
MIN_DAYS = 10           # need at least this many days of evidence
MIN_SHARE = 0.7         # late/early on at least 70% of those days

spark = (SparkSession.builder
         .appName("StructuralDelays")
         .config("spark.driver.memory", "4g")
         .config("spark.sql.shuffle.partitions", "48")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")


def save(df, name, show=15):
    """Print the top rows and write the full result as a single CSV."""
    print(f"\n--- {name} ---")
    df.show(show, truncate=False)
    (df.coalesce(1).write.mode("overwrite")
       .option("header", True).csv(f"{RESULTS_DIR}/{name}"))


# ---------------------------------------------------------------------------
# Data: full month, no sampling (sampling weakens the consistency checks)
# ---------------------------------------------------------------------------
df = (add_features(load_bus_data(spark, DATA_PATH))
      .dropna(subset=["delay"])
      .withColumn("day_type",
                  F.when(F.col("dow").isin(1, 7), "weekend")
                   .otherwise("weekday"))
      .withColumn("date_only", F.to_date("date"))
      .cache())

model = PipelineModel.load(STRUCTURAL_MODEL_PATH)

# ---------------------------------------------------------------------------
# 1. Consistency: what is late (or early) on most days?
# ---------------------------------------------------------------------------
daily = (df.groupBy("bus_line", "hour", "day_type", "date_only")
           .agg(F.avg("delay").alias("daily_delay")))

consistency = (daily.groupBy("bus_line", "hour", "day_type")
    .agg(F.count("*").alias("n_days"),
         F.round(F.avg("daily_delay") / 60, 2).alias("avg_delay_min"),
         F.round(F.expr("percentile_approx(daily_delay, 0.5)") / 60, 2)
          .alias("median_delay_min"),
         F.round(F.avg((F.col("daily_delay") > LATE_S).cast("int")), 2)
          .alias("share_days_late"),
         F.round(F.avg((F.col("daily_delay") < EARLY_S).cast("int")), 2)
          .alias("share_days_early"))
    .filter(F.col("n_days") >= MIN_DAYS)
    .cache())

save(consistency.filter(F.col("share_days_late") >= MIN_SHARE)
                .orderBy(F.desc("avg_delay_min")),
     "structurally_late")

save(consistency.filter(F.col("share_days_early") >= MIN_SHARE)
                .orderBy("avg_delay_min"),
     "structurally_early")

# ---------------------------------------------------------------------------
# 2. Expected delay map from the structural model
#    Every line x hour x day of week, at the line's typical location,
#    with congestion off: isolates the effect of time and line.
# ---------------------------------------------------------------------------
line_loc = df.groupBy("bus_line").agg(F.avg("latitude").alias("latitude"),
                                      F.avg("longitude").alias("longitude"))
hours = spark.range(5, 24).select(F.col("id").cast("int").alias("hour"))
days = spark.range(1, 8).select(F.col("id").cast("int").alias("dow"))

grid = (line_loc.crossJoin(hours).crossJoin(days)
        .withColumn("congestion", F.lit(0))
        .withColumn("at_stop", F.lit(0)))

expected = (model.transform(grid)
    .select("bus_line", "hour", "dow",
            F.round(F.col("prediction") / 60, 2).alias("expected_delay_min")))

save(expected.orderBy(F.desc("expected_delay_min")), "expected_delay_map")

# ---------------------------------------------------------------------------
# 3. Residuals: where are buses later than the model expects?
# ---------------------------------------------------------------------------
resid = (model.transform(df)
    .withColumn("residual", F.col("delay") - F.col("prediction")))

residual_stops = (resid.groupBy("closer_stop")
    .agg(F.count("*").alias("n"),
         F.countDistinct("date_only").alias("n_days"),
         F.round(F.avg("residual") / 60, 2).alias("avg_residual_min"))
    .filter((F.col("n") >= 500) & (F.col("n_days") >= MIN_DAYS))
    .orderBy(F.desc("avg_residual_min")))

save(residual_stops, "residual_stops")

# ---------------------------------------------------------------------------
# 4. Delay gain: where do buses actually lose time?
#    Delay is cumulative, so a high delay at a stop may have built up
#    earlier on the route. The change between consecutive pings shows
#    where it is created.
# ---------------------------------------------------------------------------
gain = (add_lag_features(df)
        .withColumn("delay_gain", F.col("delay") - F.col("prev_delay")))

hotspots = (gain.groupBy("closer_stop", "hour", "day_type")
    .agg(F.count("*").alias("n"),
         F.countDistinct("date_only").alias("n_days"),
         F.round(F.avg("delay_gain"), 1).alias("avg_gain_s"),
         F.round(F.avg((F.col("delay_gain") > 0).cast("int")), 2)
          .alias("share_pings_gaining"))
    .filter((F.col("n") >= 200) & (F.col("n_days") >= MIN_DAYS))
    .orderBy(F.desc("avg_gain_s")))

save(hotspots, "delay_gain_hotspots")

print(f"\nAll results written under {RESULTS_DIR}/")
spark.stop()