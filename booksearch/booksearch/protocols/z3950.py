from PyZ3950 import zoom


class Z3950():
    """ Fetches Z39.50 query's and returns the response """
    baseurl = False

    error = True

    def __init__(self, host, port, dbname):
        self.baseurl = (host, port, dbname)


