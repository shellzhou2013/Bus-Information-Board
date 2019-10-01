'''
    schedule information
    @function: this function is to save the schedule information to the database
    '''

import pandas as pd
import psycopg2
def save_schedule_to_database():
    df = pd.read_csv('../output/schedule_information_new.csv')
    
    # connect to database
    conn = psycopg2.connect(database = "test",
                            user = "postgres",
                            password = "test",
                            host = "ec2-35-165-109-193.us-west-2.compute.amazonaws.com",
                            port = "5432")
                            cur = conn.cursor()
                            
                            # drop the stop_information table if it exists
                            cur.execute("DROP TABLE IF EXISTS SCHEDULE_INFORMATION;")
                            
                            # create the stop_information table
                            cur.execute('''CREATE TABLE SCHEDULE_INFORMATION
                                (TRIP_ID      VARCHAR(50),
                                SCHEDULED_TIME           FLOAT,
                                STOP_ID            VARCHAR(20));''')
                            
                            # put the stop information to the table
                            for row in df.index:
                                # track the job
                                print(str(row) + '/' + str(len(df)))
                                cur.execute("INSERT INTO SCHEDULE_INFORMATION (TRIP_ID, SCHEDULED_TIME, STOP_ID) VALUES (%s, %s, %s)",
                                            (str(df['trip_id'][row]), str(df['scheduled_time'][row]), str(df['stop_id'][row])))
                                conn.commit()
                            conn.close()


save_schedule_to_database()
