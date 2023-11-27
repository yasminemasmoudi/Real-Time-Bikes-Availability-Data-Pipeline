# Creating a Real-Time Flight-info Data Pipeline with Kafka, Apache Spark, Elasticsearch and Kibana

In this project, we will use a real-time bikes stations info API, Apache Kafka, ElastichSearch and Kibana to create a real-time Flight-info data pipeline and track the flights in real-time. We will use a high-level architecture and
corresponding configurations that will allow us to create this data pipeline. The end result will be a Kibana dashboard fetching real-time data from ElasticSearch.


## Pipeline
The project pipeline is as follows:

![2] (https://github.com/yasminemasmoudi/Real-Time-Bikes-Availability-Data-Pipeline/blob/master/archi.png)

## Prerequisites
The following software should be installed on your machine in order to reproduice our work:

- Spark (spark-3.3.3-bin-hadoop3)
- Kafka (kafka_2.13-2.7.0)
- ElasticSearch (elasticsearch-7.14.2)
- Kibana (kibana-7.14.2)
- Python 3.10.12

## How to run
1. Start Elasticsearch

`sudo systemctl start elasticsearch ` 

2. Start Kibana

`sudo systemctl start kibana ` 

3. Start Zookeeper server by moving into the bin folder of Zookeeper installed directory by using:

`./bin/zookeeper-server-start.sh ./config/zookeeper.properties`

4. Start Kafka server by moving into the bin folder of Kafka installed directory by using:

`./bin/kafka-server-start.sh ./config/server.properties`

5. Run Kafka producer:

`python producer-kafka.py`

6. Run PySpark consumer with spark-submit:

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:2.7.0,,org.elasticsearch:elasticsearch-spark-30_2.12:7.14.2 consumer-spark.py`

## How to launch kibana dashboard

- Open http://localhost:5601/ in your browser.
- Go to Management>Kibana>Saved Objects
- Import .ndjson file
- Open dashboard










