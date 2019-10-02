## Ingestion
### Simulation the data as if it's real-time
To simulate the historical data to look like streaming data. My data is sorted with timestamp. First, I record the historical start time and the current time. Then I quickly release all the signals within a second. After that, I wait a small period of time (0.1 sec) each time until the current time passes the end time for that second. By doing all of these, I enter another loop to do job for the signals in the next second.

### Kafka basics
0. Every time you want to use pegasus, remember to do: `peg fetch spark-cluster`
1. Start all the instance in spark-cluster: `peg start spark-cluster`
2. Start zookeeper: `peg service spark-cluster zookeeper start`
3. Start kafka: `peg service spark-cluster kafka start`. 
4. ssh to your master node: go to your .ssh folder directory, and run: `ssh -i "Xuhui-IAM-keypair.pem" ubuntu@ec2-34-215-118-65.us-west-2.compute.amazonaws.com`
5. In your ec2 instance, if you run: `jps`, you can see a QuorumPeerMain job. It is related to zookeeper. Sometimes it show a job of kafka but sometimes it doesn't. 
6. Check your kafka topics: `/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181`. I have created a topic called hello_topic, if kafka has started, it will output "hello_topic"
7. Create a topic: `/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic your_topic`. You can create more relications and partitions by changing the two factors.
8. Start a producer: `/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic hello_topic`. Your tab is now pinned to wait anything you want to produce. (Act as a producer)
9. In another terminal that is ssh to the master node, start a consumer: `/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic hello_topic`. Now your tab is pinned to consume anything you produce through the producer.
10. Steps 5-9 just give you some sense of how kafka works. Now if you type anything with a return, say `hello` + return, you can see hello on both producer and consumer tabs.

### Kafka-python
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

### How to run ingestion:
In the main directory, run: `./run.sh`. You can modify the time you want to run. It's in seconds. Also you may want to run it on another topic, just change the "hello_topic" to any topic(s) you want to use. 

### Will launch more about how to run kafka in a distributed way...


### Kafka-cluster
1. Follow [https://github.com/InsightDataScience/pegasus](https://github.com/InsightDataScience/pegasus) to create your kafka-cluster.
2. Also: `peg install kafka-cluster environment` and `pip install kafka-python`
3. Create a topic: `/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 3 --topic bus_topic`


