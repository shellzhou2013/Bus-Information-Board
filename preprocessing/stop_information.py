'''
stop information
    @function: this function is to process the stop information 
        such as GPS positions and stop names
'''
from confidential_preprocessing import get_confidential
import pandas as pd
import psycopg2

def save_stop_information_to_database():
    df = pd.read_csv('../input/stops.txt')
    df = df[['stop_id', 'stop_name', 'stop_lat', 'stop_lon']]

    # connect to database
    database_password = get_confidential('database_password')
    database_host = get_confidential('database_host')
    conn = psycopg2.connect(database = "test", 
                            user = "postgres", 
                            password = database_password, 
                            host = database_host, 
                            port = "5432")
    cur = conn.cursor()

    # drop the stop_information table if it exists
    cur.execute("DROP TABLE IF EXISTS STOP_INFORMATION;")

    # create the stop_information table
    cur.execute('''CREATE TABLE STOP_INFORMATION
          (STOP_ID      VARCHAR(10),
          STOP_NAME           VARCHAR(50),
          STOP_LAT            FLOAT,
          STOP_LON        FLOAT);''')

    # put the stop information to the table
    for row in df.index:
        # track the job
        print(str(row) + '/' + str(len(df)))
        cur.execute("INSERT INTO STOP_INFORMATION (STOP_ID, STOP_NAME, STOP_LAT, STOP_LON) VALUES (%s, %s, %s, %s)",
                  (str(df['stop_id'][row]), df['stop_name'][row], str(df['stop_lat'][row]), str(df['stop_lon'][row])))
        conn.commit()
    conn.close()

save_stop_information_to_database()
