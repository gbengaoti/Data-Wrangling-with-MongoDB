#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
  ....
}
The type() function returns a type object describing the argument given to the 
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.

Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]
          
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def process_value(cell):
    if cell == "NULL" or cell == "":
        cell = None
        return type(None)
    elif cell.startswith("{"):
        try:
            cell = list(cell)
            return type([])
        except TypeError:
            print "cannot cast cell value to list"
    elif is_int(cell) == True:
        cell = int(cell)
        return type(1)
    elif is_float(cell) == True:
        cell = float(cell)
        return type(1.1)
    else:
        
        cell = str(cell)
        return type('a')
        
def audit_file(filename, fields):
    fieldtypes = {}
    # initialize with lists here
    for field in FIELDS:
        fieldtypes[field] = list()
    
    reader = csv.DictReader(open(filename))
    # skip header
    header = reader.fieldnames
    # skip three lines
    line1_after_header = next(reader)
    line2_after_header = next(reader)
    line3_after_header = next(reader)
    
    
    for entry in reader:
        for field in FIELDS:
            if field == "areaLand":
                pprint.pprint(entry[field])
            else:
                pass
            f_type = process_value(entry[field])
            fieldtypes[field].append(f_type)
    # turn data type lists into sets
    for key in fieldtypes.keys():
        fieldtypes[key] = set(fieldtypes[key])
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    #pprint.pprint(fieldtypes)
    pprint.pprint(fieldtypes["areaLand"])
    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
    
