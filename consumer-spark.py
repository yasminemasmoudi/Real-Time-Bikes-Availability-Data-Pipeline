from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import StringType
import time
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, BooleanType, IntegerType, MapType, FloatType
import pickle 
import json
from pyspark.sql.functions import *
from pyspark.sql.types import *
from elasticsearch import Elasticsearch
es = Elasticsearch()


sc = SparkContext.getOrCreate()

path = "/home/Documents/bikes/velo.csv"
check_path = "/home/Documents/bikes/"


spark = SparkSession.builder.appName('DataStreamingApp').getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

chema = StructType(
[StructField("number", IntegerType(), True),
 StructField("contract_name", StringType(), True),
 StructField("name", StringType(), True),
 StructField("address", StringType(), True),
 StructField("position",MapType(FloatType(), FloatType(), True)),
 StructField("banking", BooleanType(), True),
 StructField("bonus", BooleanType(), True),
 StructField("bike_stands", IntegerType(), True),
 StructField("available_bike_stands", IntegerType(), True),
 StructField("available_bikes", IntegerType(), True),
 StructField("status", StringType(), True),
 StructField("last_update", IntegerType(), True)])
 
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "velib-topic") \
  .load()
print(df.isStreaming)


parsed_df = df \
            .select(from_json(col('value').cast('string'),
                    chema).alias('parsed_value')) \
            .withColumn('timestamp', lit(current_timestamp()))
mdf = parsed_df.select('parsed_value.*', 'timestamp')
print(mdf)

    
#query.awaitTermination() 

split_col =  split(df.value, '\\,')

df = df.withColumn("number", split_col.getItem(0))\
    .withColumn("contract_name", split_col.getItem(1))\
    .withColumn("name", split_col.getItem(2))\
    .withColumn("address", split_col.getItem(3))\
    .withColumn("position", split_col.getItem(4))\
    .withColumn("banking", split_col.getItem(5))\
    .withColumn("bonus", split_col.getItem(6))\
    .withColumn("available_bike_stands", split_col.getItem(7))\
    .withColumn("available_bikes", split_col.getItem(8))\
    .withColumn("status", split_col.getItem(9))\
    .withColumn("last_update", split_col.getItem(10))\
    .drop("key")

print(df)

query = df \
    .selectExpr("number" , "contract_name" , "name" , "address" , "position" , "banking" , "bonus" , "available_bike_stands" , "available_bikes" , "status" , "last_update") \
    .writeStream \
    .format("console") \
    .option("header" , True) \
    .start()

query = df.writeStream.format('consol').option("es.port", "9200").option("es.nodes" , "localhost").option("es.resource", "yass").outputMode("append").start()
  
query.awaitTermination()
print("yes")





