from pyspark.sql import SparkSession
from pathlib import Path

def main():
    # initialize SparkSession
    spark = SparkSession.builder.appName("BusAnalysis").getOrCreate()

    # read my_dataset_complete_31_files/siri.20130101.csv
    dataset_path = str(Path(__file__).parent.parent / "Lab02/my_dataset_complete_31_files/siri.20130101.csv")
    sc = spark.sparkContext
    sc.setLogLevel('WARN')

    # use 4 partitions for the RDD
    inputRDD = sc.textFile(dataset_path, minPartitions=4)

    # column headers: date, bus_line, bus_line_pattern, congestion, longitude, latitude, delay, vehicle_id, closer_stop, at_stop
    df = inputRDD.map(lambda line: line.split(',')).map(lambda fields: {
        'date': fields[0],
        'bus_line': fields[1],
        'bus_line_pattern': fields[2],
        'congestion': fields[3],
        'longitude': float(fields[4]),
        'latitude': float(fields[5]),
        'delay': float(fields[6]),
        'vehicle_id': fields[7],
        'closer_stop': fields[8],
        'at_stop': fields[9] == '1'
    })


    def get_secs_str_in_minute(seconds):
        return f"{seconds / 60:.1f} min"


    # count how many rows are in each partition
    partition_counts = df.glom().map(len).collect()
    print("Number of rows in each partition:", partition_counts)

    # print the first 5 rows of the RDD
    for row in df.take(5):
        print(row)

    # find the maximum and minimum delay in the dataset
    delay_stats = df.map(lambda r: r["delay"]).stats()
    print("Max delay:", f"{get_secs_str_in_minute(delay_stats.max())}")
    print("Min delay:", f"{get_secs_str_in_minute(delay_stats.min())}")
    print("Mean delay:", f"{get_secs_str_in_minute(delay_stats.mean())}")

    # check top 10 most delayed bus lines
    top_10_most_delayed_lines = df.map(lambda r: (r["bus_line"], r["delay"])).groupByKey().mapValues(lambda delays: sum(delays)/len(delays)).takeOrdered(10, key=lambda x: -x[1])
    print("Top 10 most delayed bus lines:")
    for line, avg_delay in top_10_most_delayed_lines:
        print(f"{line}: {get_secs_str_in_minute(avg_delay)}")

    # check top 10 least delayed bus lines
    top_10_least_delayed_lines = df.map(lambda r: (r["bus_line"], r["delay"])).groupByKey().mapValues(lambda delays: sum(delays)/len(delays)).takeOrdered(10, key=lambda x: x[1])
    print("Top 10 least delayed bus lines:")
    for line, avg_delay in top_10_least_delayed_lines:
        print(f"{line}: {get_secs_str_in_minute(avg_delay)}")

    # count buses by their closest stop, regardless of whether they are at the stop
    closest_stop_counts = df.map(lambda r: (r["closer_stop"], 1)).reduceByKey(lambda a, b: a + b)
    top_10_closer_stops = closest_stop_counts.takeOrdered(10, key=lambda x: -x[1])
    print("Top 10 closest stops with the most buses:")
    for stop, count in top_10_closer_stops:
        print(f"{stop}: {count} buses")

    # get the 10 closest stops with the fewest buses
    top_10_least_closer_stops = closest_stop_counts.takeOrdered(10, key=lambda x: x[1])
    print("Top 10 closest stops with the fewest buses:")
    for stop, count in top_10_least_closer_stops:
        print(f"{stop}: {count} buses")

    # correlate the delay with the congestion level
    congestion_delay_correlation = df.map(lambda r: (r["congestion"], r["delay"])).groupByKey().mapValues(lambda delays: sum(delays)/len(delays)).collect()
    print("Average delay by congestion level:")
    for congestion, avg_delay in sorted(congestion_delay_correlation):
        print(f"{congestion}: {get_secs_str_in_minute(avg_delay)}")

    # plot the average delay by congestion level
    import matplotlib.pyplot as plt

    congestion_levels = [congestion for congestion, _ in sorted(congestion_delay_correlation)]
    avg_delays = [avg_delay for _, avg_delay in sorted(congestion_delay_correlation)]

    plt.bar(congestion_levels, avg_delays)
    plt.xlabel("Congestion Level")
    plt.ylabel("Average Delay (minutes)")
    plt.title("Average Delay by Congestion Level")
    plt.show()

if __name__ == "__main__":
    main()