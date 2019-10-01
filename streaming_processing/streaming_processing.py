# version 4

import psycopg2
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.context import SQLContext
from pyspark.sql import SparkSession



def initialize_database():
    '''
        @input: None
        @output: None
        @function: this function is to initialize the table called "RECORD" so that
        everytime we can create a new "RECORD" table to store qualified data
        '''
    conn = psycopg2.connect(database = "test",
                            user = "postgres",
                            password = "test",
                            host = "ec2-35-165-109-193.us-west-2.compute.amazonaws.com",
                            port = "5432")
                            cur = conn.cursor()
                            cur.execute("DROP TABLE IF EXISTS RECORD;")
                            
                            # create a new "record" table
                            cur.execute('''CREATE TABLE RECORD
                                (TIME_STAMP      TIMESTAMP     NOT NULL,
                                ROUTE_ID           VARCHAR(30)    NOT NULL,
                                TRIP_ID            VARCHAR(50)     NOT NULL,
                                DISTANCE        FLOAT,
                                NEXT_STOP         VARCHAR(30));''')
                            
                            # commit the change and close the connection
                            conn.commit()
                            conn.close()


def sendPartition(iterater):
    '''
        @input:
        iterater (rdd): an RDD
        @ouput:
        None
        @function:
        this function is used as the function in foreachRDD method.
        it helps writing all the rdds at a micro batch in a partition to the database
        '''
    conn = psycopg2.connect(database = "test",
                            user = "postgres",
                            password = "test",
                            host = "ec2-35-165-109-193.us-west-2.compute.amazonaws.com",
                            port = "5432")
                            cur = conn.cursor()
                            for record in iterater:
                                cur.execute("INSERT INTO RECORD (TIME_STAMP,ROUTE_ID,TRIP_ID,DISTANCE,NEXT_STOP) VALUES (%s, %s, %s, %s, %s)",
                                            (record[0], record[1], record[2], record[3], record[4]))
                            conn.commit()
    conn.close()

def process_trip_id(trip_id):
    '''
        @input (string): trip_id before processing
        @output (string): trip_id after processing
        @function: because the trip_ids from the historical data have some strange stuffs,
        need to clean it before save it into database
        '''
    trip_id_list = trip_id.split('-')
    if len(trip_id_list) == 3:
        trip_id_list[0] = '_'.join(trip_id_list[0].split('_')[1:])
    elif len(trip_id_list) == 4:
        trip_id_list[0] = '_'.join(trip_id_list[0].split('_')[1:])
        trip_id_list = [trip_id_list[0], trip_id_list[1], trip_id_list[3]]
    elif len(trip_id_list) == 6:
        trip_id_list = trip_id_list[:-1]
    return "-".join(trip_id_list)



def spark_streaming_processing(batch_size, zookeeper_port, topic):
    '''
        @input:
        batch_size (int): define the batch_size in second for spark streaming
        zookeeper_port (string): the port of zookeeper, such as "localhost:2181"
        topic (string): the topic that data is ingested
        @output:
        None
        @function:
        start a spark streaming job to:
        receive signals from kafka topic
        process data
        write data to database
        '''
    
    # create spark context and spark streaming context
    sc = SparkContext(appName="ConsumeFromKafkaSendToDatabase")
    ssc = StreamingContext(sc, batch_size)
    
    # ingest data from kafka, in spark streaming, lines is a Dstream
    kvs = KafkaUtils.createStream(ssc, zookeeper_port, "spark-streaming-consumer", {topic: 1})
    lines =  kvs.map(lambda x: x[1])
    lines = lines.map(lambda line: line.split("\t"))
    
    # filter records that is not regular or show that the bus is not functioning
    lines = lines.filter(lambda line: len(line) == 11)
    lines = lines.filter(lambda line: line[6] != "LAYOVER_DURING")
    
    # we only need: time stamp/route id/trip_id/distance/next stop
    lines = lines.map(lambda line: [line[2], line[7], process_trip_id(line[8]),
                                    line[9], line[10].split('_')[1].split('\n')[0]])
        
                                    
                                    # after filtering, we want to write each rdd to the database
                                    lines.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))
                                    
                                    # start spark streaming job
                                    ssc.start()
                                    ssc.awaitTermination()

def main():
    initialize_database()
    spark_streaming_processing(1, "localhost:2181", "hello_topic")
main()
