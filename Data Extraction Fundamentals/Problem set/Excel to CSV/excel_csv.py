# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile
import numpy as np

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

def handle_station(station_index, station_name,sheet):
    start_index = 1
    station_column = sheet.col_values(station_index, start_index)
    station_index_max = np.argmax(station_column)
    station_max_value = station_column[station_index_max]
    year, month, day, hour, _, _ = xlrd.xldate_as_tuple(sheet.cell_value(station_index_max + 1, 0), 0)
    station_data = [station_name, year, month, day, hour, station_max_value]
    return station_data

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    # YOUR CODE HERE
    # handle header
    data.append(["Station","Year","Month","Day","Hour","Max Load"])
    # handle coast
    coast_data = handle_station(1, "COAST", sheet)
    data.append(coast_data)
    # handle east
    east_data = handle_station(2, "EAST", sheet)
    data.append(east_data)
    # handle far-west
    far_west_data = handle_station(3, "FAR_WEST", sheet)
    data.append(far_west_data)
    # handle north
    north_data = handle_station(4, "NORTH", sheet)
    data.append(north_data)
    # handle north_c
    north_c_data = handle_station(5, "NORTH_C", sheet)
    data.append(north_c_data)
    # handle southern
    southern_data = handle_station(6, "SOUTHERN", sheet)
    data.append(southern_data)
    # handle south_c
    south_c_data = handle_station(7, "SOUTH_C", sheet)
    data.append(south_c_data)
    # handle west
    west_data = handle_station(8, "WEST", sheet)
    data.append(west_data)
    return data


def save_file(data, filename):
    with open(filename, 'wt') as csvfile:
        stationwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(data)):
            stationwriter.writerow(data[i])

def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
