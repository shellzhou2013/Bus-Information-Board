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
6. Check your kafka topics: `/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181`
7. 
