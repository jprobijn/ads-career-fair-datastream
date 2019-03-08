import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import json
from dateutil import parser
from modules.DataframeToJsonConverter import DataframeToJsonConverter


class DataStreamer:
    def __init__(self, input_file, time_column_name, no_delay=False, verbose=False):
        """
        :param input_file: Path to a CSV file containing inmotio position data
        :param time_column_name: string with the name of the column containing time values
        :param no_delay: Should the datastreamer not simulate the actual event times in
                         the data by delaying each datapoint as needed?
        :param verbose: Should the datastreamer print its' progress?
        """

        self.time_column_name = time_column_name
        self.no_delay = no_delay
        self.verbose = verbose

        # Get a dataframe containing the CSV's position data
        input_data = pd.read_csv(input_file)

        # Convert to stream format
        DataConverter = DataframeToJsonConverter(self.time_column_name)
        stream_data = DataConverter.convert_data_to_stream_format(input_data)

        # Convert the timestamps to datetime strings
        # Calculate the start time of the match (used as offset for event time)
        self.match_start_datetime = datetime.now()
        for data in stream_data:
            data[self.time_column_name] = self.gametime_to_datetime(data[self.time_column_name])

        self.stream_data = stream_data


    def gametime_to_datetime(self, gametime):
        """
        This function converts gametime (in seconds) to a matching datetime relative to some
        provided datetime offset marking gametime=0.0

        :param gametime: gametime describing how many seconds have passed since the start of the match
        :return: datetime matching the given gametime
        """

        # Calculate how many milliseconds we're into the match
        ms_progress = round(gametime*1000)

        # Calculate the event datetime based on that progress
        event_datetime = self.match_start_datetime + timedelta(milliseconds=ms_progress)

        return event_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


    def get_streamable_data(self):
        """
        This function converts the input data into a streamable list of dictionaries and saves
        said list into the stream_data member variable. It also saves the datetime associated
        with the start of the data in a separate member variable called match_start_datetime
        """


    def local_stream(self):
        """
        :param sink: producer object implementing a push_message() function which we'll use to
                     push a message for every timestamp
        """

        if self.verbose:
            print('Streaming timestamps ' + str(min(self.stream_data, key=lambda m: m[self.time_column_name])[self.time_column_name]) +
                  ' to ' + str(max(self.stream_data, key=lambda m: m[self.time_column_name])[self.time_column_name]))
            print('-'*35)
       
        # # Loop over all data and stream
        for i, stream_data_point in enumerate(self.stream_data):

            # Save the start time of the data point processing period
            previous_stream_time = time.time()

            if self.verbose:
                curr_datetime = parser.parse(stream_data_point[self.time_column_name])
                if (curr_datetime - self.match_start_datetime).total_seconds() % 5 == 0.0:
                    print(datetime.now().strftime("%H:%M:%S") + ' || Timestamp ' +
                          str(stream_data_point[self.time_column_name]))

            # Stream the data
            yield(stream_data_point)

            # Compute the required time to wait to stream the next data point

            if not self.no_delay and i < len(self.stream_data)-1:

                delta_t = parser.parse(self.stream_data[i + 1][self.time_column_name]) - parser.parse(stream_data_point[self.time_column_name])
                time_to_wait = delta_t.total_seconds() - (time.time() - previous_stream_time)

                if time_to_wait > 0:
                    time.sleep(time_to_wait)

    def get_data_sample(self):

        return self.stream_data[7]

