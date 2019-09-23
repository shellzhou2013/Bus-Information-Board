# Bus-Information-Board
## 1. Environment setup
### 1. Set up AWS account (VPC, security groups, IAM) and apply the 1000 credit. (See insight internal material)
When you set up the inbound rule and outbound rule for your security group, for outbound rule, you can set it allow all traffic to all ips. For inbound rule, you need to allow all traffics from your ip, and allow all traffic from itselt (put the same group_id)
### 2. Use Pegasus to intall a spark-cluster with 1 master node and 3 worker nodes.
See [https://docs.google.com/document/d/1InLxbu-FH2nyd0NuJ3ewdvAt0Ttk_bNUwlQop38lq0Q/edit#](https://docs.google.com/document/d/1InLxbu-FH2nyd0NuJ3ewdvAt0Ttk_bNUwlQop38lq0Q/edit#) or [https://github.com/InsightDataScience/pegasus](https://github.com/InsightDataScience/pegasus). After doing step, you have already installed ssh, aws, hadoop, spark, zookeeper, kafka. You can also use this command to install extra apps like java: `peg install spark-cluster environment`
### 3. Kafka
0. Every time you want to use pegasus, remember to do: `peg fetch spark-cluster`
1. Start all the instance in spark-cluster: `peg start spark-cluster`
2. Start zookeeper: `peg service spark-cluster zookeeper start`
3. Start kafka: `peg service spark-cluster kafka start`. Sometimes it won't allow you to start kafka. I have no idea what the problem is. The only way I figured out to solve this problem is to reinstall zookeeper and kafka: 
`peg uninstall zookeeper`
`peg uninstall kafka`
`peg install zookeeper`
`peg install kafka`
4. ssh to your master node: go to your .ssh folder directory, and run: `ssh -i "Xuhui-IAM-keypair.pem" ubuntu@ec2-34-215-118-65.us-west-2.compute.amazonaws.com`
5. In your ec2 instance, if you run: `jps`, you can see a QuorumPeerMain job. It is related to zookeeper. Sometimes it show a job of kafka but sometimes it doesn't. 
6. Check your kafka topics: `/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181`. I have created a topic called hello_topic, if kafka has started, it will output "hello_topic"
7. Create a topic: `/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic your_topic`. You can create more relications and partitions by changing the two factors.
8. Start a producer: `/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic hello_topic`. Your tab is now pinned to wait anything you want to produce. (Act as a producer)
9. In another terminal that is ssh to the master node, start a consumer: `/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic hello_topic`. Now your tab is pinned to consume anything you produce through the producer.
10. Steps 5-9 just give you some sense of how kafka works. Now if you type anything with a return, say `hello` + return, you can see hello on both producer and consumer tabs.
### 4. Kafka-python
0. Install kafka-python package: `pip install kafka-python`
1. Python code directly act as a producer: 
```
import kafka
cluster = kafka.KafkaClient("localhost:9092")
prod = kafka.SimpleProducer(cluster, async=False)
topic = "hello_topic"
prod.send_messages(topic, message_you_want_send)
```
For more information, see [https://github.com/dpkp/kafka-python](https://github.com/dpkp/kafka-python)
### 5. PySpark
0. Install PySpark: `pip install pyspark`. For more tutorial about spark, see [https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/spark-intro](https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/spark-intro)
### 6. Kafka + Spark Streaming in python:
1. The package to import:
```
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.context import SQLContext
```
2. Before run your python file, you need to start your producer so that spark-streaming has something to ingest and process
3. Run the spark job locally:
```
/usr/local/spark/bin/spark-submit --jars /usr/local/spark/jars/spark-streaming_2.11-2.4.0.jar --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 /home/ubuntu/code/test.py
```
You need to check if the jar file is in your `/usr/local/spark/jars` folder and if the package is able to get. This package works for me now.
4. To be able to run it on the master nodes, you need to start spark for all node:
```
peg service spark-cluster hadoop start
peg service spark-cluster spark start
```
5. Run the job in a distributed way:
```
/usr/local/spark/bin/spark-submit --master spark://ec2-34-215-118-65.us-west-2.compute.amazonaws.com:7077 --jars /usr/local/spark/jars/spark-streaming_2.11-2.4.0.jar --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 /home/ubuntu/code/test.py
```
### 7. PostgreSQL
1. Create a database cluster with only one master. I will just use EC2 ubuntu instance
2. SSH to your node
3. Peg install the environment: `peg install database-cluster environment`
4. Install postgresql: 
```
sudo apt update
sudo apt upgrade
sudo apt install build-essential
sudo apt install postgresql postgresql-contrib
```
5. Install psycopg2 so that python can connect to database. For some reason, I need to install binary version: `pip install psycopg2-binary`
6. 



## 2. Project Idea
