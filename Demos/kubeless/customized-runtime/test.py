from lib.lib import CSVObject
import json
from ast import literal_eval


def counter(event, context):
    result = '{"error":"missing file name or incorrect json schema"}'
    if event['data']:
        data_dump = json.dumps(event['data'])
        data_dict = literal_eval(data_dump)
        if 'file' in data_dict.keys():
            fName = data_dict['file']
            delims = ',; '
            quotes = '"' + "'"
            CSVFile = CSVObject(fName, delims, quotes)
            num_lines = sum(1 for line in CSVFile)
            result = '{"score":"%s"}' % num_lines
    result = literal_eval(result)
    return result
