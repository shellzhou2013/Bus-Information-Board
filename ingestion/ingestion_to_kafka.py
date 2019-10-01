import datetime
import time
import sys
import kafka

def simulate_real_time_data(total_running_time, file_dir, kafka_url, kafka_topic):
    '''
        @input:
        total_running_time (integer): time that you want to run your data ingestion in seconds
        file_dir (string): folder directory where historical data saved
        @output:
        Nothing
        @function:
        This fucntion first simulate historical bus GPS data as if they are real-time signals
        and then send the real-time signals to kafka message queue.
        
        How:
        1. build kafka connection
        2. get the time program starts as the real_start_time
        3. get the start time of historical data as the historical_start_time
        4. for loop to simulate data in a certain second
        1. real_end_time = real_start_time + seconds passed
        2. historical_end_time = historical_start_time + seconds passed
        3. quickly send all the rows before the historical_end_time to kafka, the timestamp
        needs to be modified by the real_end_time - 1
        4. wait a small gap every time until the current time > real_end_time
        '''
    
    
    # build kafka connection
    cluster = kafka.KafkaClient(kafka_url)
    producer = kafka.SimpleProducer(cluster, async=False)
    topic = kafka_topic
    
    # open the data file and skip the first line which is the header
    f = open(file_dir, 'r')
    f.readline()
    
    # set up historical and real start times
    first_line_string = f.readline()
    first_line_list = first_line_string.split('\t')
    historical_start_time = datetime.datetime.strptime(first_line_list[2], '%Y-%m-%d %H:%M:%S')
    real_start_time = datetime.datetime.now()
    
    # assign the unsent line with first row
    # we need to open a new row so that we know it doesn't belong to current second
    unexecuted_line = first_line_string
    
    # send signals to kafka for each second
    for i in range(1, int(total_running_time) + 1):
        # get the end time for historical and real time
        real_end_time = real_start_time + datetime.timedelta(0, i, 0)
        historical_end_time = historical_start_time + datetime.timedelta(0, i, 0)
        
        while True:
            # if there is unexecuted line, execute this line first
            if unexecuted_line:
                line = unexecuted_line
                unexecuted_line = None
            else:
                line = f.readline()
            row = line.split('\t')
            
            # modified the time stamp and send to kafka when the timestamp < historical_end_time
            # break otherwise
            if datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S') < historical_end_time:
                row[2] = (datetime.datetime.now() - datetime.timedelta(0, 1, 0)).strftime("%Y-%m-%d %H:%M:%S")
                producer.send_messages(topic, '\t'.join(row))
            else:
                unexecuted_line = line
                break
        
        # wait 0.1 every time until the current time > real_end_time
        while True:
            curr_time = datetime.datetime.now()
            if curr_time < real_end_time:
                time.sleep(0.1)
            else:
                break

# close the file
f.close()
def main():
    simulate_real_time_data('2000', '../input/MTA-Bus-Time_.2014-08-01.txt', 'localhost:9092', 'hello_topic')

main()
