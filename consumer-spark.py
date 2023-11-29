
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

spark = SparkSession.builder.appName("consumer").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("numbers", IntegerType(), True),
    StructField("contract_name", StringType(), True),
    StructField("banking", StringType(), True),
    StructField("bike_stands", IntegerType(), True),
    StructField("available_bike_stands", IntegerType(), True),
    StructField("available_bikes", IntegerType(), True),
    StructField("address", StringType(), True),
    StructField("status", StringType(), True),
    StructField("position", StructType([
        StructField("lat", DoubleType(), True),
        StructField("lng", DoubleType(), True)
    ]), True),
    StructField("timestamps", StringType(), True),
])

kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bike") \
    .option("startingOffsets", "latest")\
    .load()

json_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")
json_df = json_df.withColumn("position", col("position").alias("position").cast("struct<lat:double, lon:double>"))

zero_bikes_df = json_df.filter(col("available_bikes") == 0)


query = zero_bikes_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()


data = json_df.writeStream \
        .format("org.elasticsearch.spark.sql") \
        .outputMode("append")\
        .option("es.nodes", "127.0.0.1")\
        .option("es.port", "9200")\
        .option("es.index.auto.create", "true") \
        .option("es.resource", "bike")\
        .option("es.nodes.wan.only", "true") \
        .option("checkpointLocation", "/home/osboxes/Documents/projects/bikes/checkpoints/new") \
        .start()
data.awaitTermination()
