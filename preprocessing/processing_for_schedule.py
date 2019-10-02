# version 4: hide the confidential
import pandas as pd

def str_to_min(time_str):
    '''
    @imput (string): the time in string in format of hh:mm:ss
    @output (float): the time of float with unit of minute
    '''
    hour, minute, second = time_str.split(':')
    return int(hour) * 60.0 + int(minute) * 1.0 + int(second) / 60.0



def get_schedule_time(file_directory):
    '''
    @input (string): the file directory where the schedule information is
    @output: None
    @function: this function is to calculate the schedule time for each trip_id.
        for each stop_id in each trip_id, the scheduled time from beginning to
        this stop is calculated and saved in a temporary output file.
        the reason to calculate this is, the streaming signal only has the next
        stop the bus will arrive. So we need this information to get the time
        period from that next stop to any stop in this trip id
    '''
    df = pd.read_csv(file_directory)
    df = df[['trip_id', 'departure_time', 'stop_id']]
    df['scheduled_time'] = df['departure_time'].apply(str_to_min)
    
    # for each trip id, calculate the scheduled time
    trip_list = df['trip_id'].unique()
    total_job = len(trip_list)
    df_schedule = None
    
    for i, trip_id in enumerate(trip_list):
        # first find all the sequence in each trip, then:
        # scheduled time for this stop = scheduled arrival time - scheduled start time for this trip
        df_slice_for_this_trip = df[df['trip_id'] == trip_id]
        start_index = df_slice_for_this_trip.index[0]
        start_time_for_this_trip = df_slice_for_this_trip['scheduled_time'][start_index]
        df_slice_for_this_trip['scheduled_time'] -= start_time_for_this_trip
        # connect the processed data to df_schedule
        df_schedule = pd.concat([df_schedule, df_slice_for_this_trip], axis=0, join='outer', ignore_index=True)
        # track the job processing
        print("Job processing: " + str(i) + '/' + str(total_job))
    df_schedule = df_schedule[['trip_id', 'scheduled_time', 'stop_id']]
    # save it to a temporary output file
    df_schedule.to_csv('../output/schedule_information_new.csv')


    
file_directory = '../input/stop_times.txt'
get_schedule_time(file_directory)  
