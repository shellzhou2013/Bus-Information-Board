## Streaming processing
### Spark
1. Start spark: on your local machine, run: `peg service spark-cluster hadoop start` and `peg service spark-cluster spark start`. By doing these, you can see your spark UI at: http://ec2-***-***-***-**.us-west-2.compute.amazonaws.com:8080/
2. Install pyspark: `pip install pyspark`. For more tutorial about spark, see [https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/spark-intro](https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/spark-intro)
3. Before running the spark streaming job: you need to check if the jar file is in your `/usr/local/spark/jars` folder and if the spark streaming kafka package is able to get. This package works for me now.
4. Run the spark job locally:
```
/usr/local/spark/bin/spark-submit --jars /usr/local/spark/jars/spark-streaming_2.11-2.4.0.jar --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 your_file.py
```
5. Run the job in a distributed way:
```
/usr/local/spark/bin/spark-submit --master spark://ec2-***-***-***-***.us-west-2.compute.amazonaws.com:7077 --jars /usr/local/spark/jars/spark-streaming_2.11-2.4.0.jar --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 your_file.py
```
### Kafka ingestion
1. run the ingestion, then the spark streaming job is going to process the signals.

### PostgreSQL
1. I put the database on another EC2 instance. To make life simplifier, I use pegasus to create a database-cluster using the same VPC and security group. 
2. After that, just install the environment:  `peg install database-cluster environment`.
3. Installation of Postgre database. 
4. Install postgresql: 
```
sudo apt update
sudo apt upgrade
sudo apt install build-essential
sudo apt install postgresql postgresql-contrib
```
Generally just follow this: [https://docs.google.com/presentation/d/1cQ_G2DWvpW4qGhd9oiQV7xnWmYV7aLFGZGwK5GQPWgo/present?slide=id.p](https://docs.google.com/presentation/d/1cQ_G2DWvpW4qGhd9oiQV7xnWmYV7aLFGZGwK5GQPWgo/present?slide=id.p). 
5. Install psycopg2 so that python can connect to database. For some reason, I need to install binary version: `pip install psycopg2-binary`. However to use it: [https://www.tutorialspoint.com/postgresql/postgresql_python.htm](https://www.tutorialspoint.com/postgresql/postgresql_python.htm)
6. An important thing is to allow external reading and writing to your database from other instances. Follow this blog to modify .conf files: [https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252](https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252)
### How to run
In your main function, you can change the micro-batch-size (currently 1 second), the zookeeper host (currently local) and topic name. To run it, under the streaming_processing folder, run `./run_streaming.sh`

Before running it, don't forget to install the required packages on your workers such as **psycopg2!!!**
