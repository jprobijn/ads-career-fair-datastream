import json
import numpy as np

class DataframeToJsonConverter():

    def __init__(self, time_column_name):
        self.time_column_name = time_column_name


    def convert_data_to_stream_format(self, inmotio_dataframe,
                                      columns_to_stream = ['X', 'Y', 'PlrID', 'TeamName']):
        """
        This function converts the specified Inmotio data to the format required for streaming

        :param inmotio_dataframe: Pandas dataframe with the data to be streamed
        :param columns_to_stream: list with the names of the columns to stream
        :return: list of dictionaries (i.e. json objects) with the data in the required format
        """
        json_data_list = []

        # Subset to necessary columns
        inmotio_dataframe = inmotio_dataframe[columns_to_stream + [self.time_column_name]]

        # Subset to required columns and convert to json
        pos_json_per_timestamp = inmotio_dataframe.groupby(self.time_column_name).apply(lambda x:
                                                                        x.to_json(orient='records'))

        # Loop over all timestamps and create a list of dictionaries
        for timestamp in pos_json_per_timestamp.index.values:
            # Construct dictionary
            json_data = {self.time_column_name: timestamp,
                         "pos": [{i:dict[i] for i in dict if i != self.time_column_name} for dict in
                                 json.loads(pos_json_per_timestamp[timestamp])]}
            json_data_list.append(json_data)

        return json_data_list
