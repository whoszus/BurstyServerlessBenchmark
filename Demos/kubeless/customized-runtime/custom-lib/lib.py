class CSVObject(object):
    """
    This class instantiates a file object as an interable. It means that
    CSV files can be read more efficiently than reading the entire data
    into memory.
    """

    def __init__(self, fileName, delimiters, quotes):
        self.fileName = fileName
        self.delimiters = delimiters
        self.quotes = quotes
        self.fin = open(fileName, 'r')

    def __iter__(self):
        return self

    def next(self):
        line = self.fin.next()
        return self.parseLine(line)

    def parseLine(self, line):
        """
        Parses a line of CSV text into components. This attempts to
        be a proper parser that can cope with multiple delimiters.
        """
        inQuote = False  # flag for being 'within' quotes
        token = ''  # current token
        tokens = []  # list of tokens
        for char in line:
            if inQuote:  # so if we're in the middle of a quote...
                if char == inQuoteChar:  # ...and have a matching quote character...
                    tokens.append(token)  # add the token to list (ignore quote character)
                    token = ''  # and begin new token
                    inQuote = False  # flag that we're not in a quote any more
                else:  # But if char is a non-matching quote...
                    token += char  # ...just add to token
            elif char in self.delimiters:  # or if char is a delimiter...
                if len(token) > 0:  # ...and token is worth recording...
                    tokens.append(token)  # add token to list
                    token = ''  # and begin new token
                else:  # if token has 0 length and no content...
                    pass  # ...adjacent delimiters so do nothing
            elif char in self.quotes:  # But if char is a quote...
                inQuoteChar = char  # record it to check for matching quote later
                inQuote = True  # and flag that we're in a quotation
            else:  # And if char is anything else...
                token += char  # add to token
        if len(token) > 0:  # Check if last item is worth recording (len > 0)
            tokens.append(token)  # add to list of tokens
        return tokens  # return list of tokens


if __name__ == '__main__':
    fName = './test.csv'
    delimiters = ',; '
    quotes = '"' + "'"
    CSVFile = CSVObject(fName, delimiters, quotes)
    for line in CSVFile:
        print(line)
