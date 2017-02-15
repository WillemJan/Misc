#!/usr/bin/env python

import sys

from booksearch.api import BookSearch


def main(query=False):
    if not query:
        query = " ".join(sys.argv[1:])

    bs = BookSearch()
    bs.query(query)



if __name__ == "__main__":
    if len(sys.argv) >= 1:
        main(" ".join(sys.argv[1:]))
    else:
        print "Usage: %s <query>" % __name__

