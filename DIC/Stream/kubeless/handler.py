from collections import Counter

def handler(event, context):
    string = 'hello world'
    if string:
        Counter(string.strip().split())
        return {'token': 'warming done'}
    else:
        return {'token': 'warming done'}
