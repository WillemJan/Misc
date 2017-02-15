========================================
BookSearch: Python based book search API
========================================


What is it
----------

A simple python based API to search across different sources of book-metadata providers.


Installation
------------

To install BookSearch to your system, follow these three steps:
(Tested with Raspbian, Debian GNU/Linux 7)

::
    
    cd booksearch; make

Create a virutalenv in the directory one level higher (../virtualenv), and check dependencies.

::

    source virtualenv/bin/activate

Activate the virtualenv.

:: 

    python booksearch/setup.py install

Install the BookSearch package within the virtualenv.


Features
--------

Some of the highlights:

    * Easy search across mutiple National Library Systems.

    * Supports mutiple search protocols, SRU, Z3950, OpenSearch.

    * Uses doctests.


Usefull resources
-----------------

SRU
~~~

- `SRU Standard overview`_

.. _`SRU Standard overview`: http://www.loc.gov/standards/sru/

- `SRU Server implementation test`_

.. _`SRU Server implementation test`: http://alcme.oclc.org/srw/test/SRUServerTester?url=

SRU endpoints
~~~~~~~~~~~~~

- `CH`_, Projekt swissbib, UB Basel, Switzerland, `Terms of service (CH)`_

::

  http://sru.swissbib.ch/sru/explain?operation=explain&version=1.1

.. _`CH`: http://sru.swissbib.ch/sru/explain?operation=explain&version=1.1

.. _`Terms of service (CH)`: http://www.swissbib.org/wiki/index.php?title=SRU

- `DE`_, Deutsche Nationalbibliothek `Terms of service (DE)`_

::

  http://services.dnb.de/sru/dnb?operation=explain&version=1.1       

.. _`DE`: http://services.dnb.de/sru/dnb?operation=explain&version=1.1

.. _`Terms of service (DE)`: http://www.dnb.de/EN/Service/DigitaleDienste/SRU/sru_node.html

- `NL`_, GGC - National Library of the Netherlands, `Terms of service (NL)`_

::

  http://jsru.kb.nl/sru/sru?operation=explain&version=1.1  

.. _`NL`: http://jsru.kb.nl/sru/sru?operation=explain&version=1.1

.. _`Terms of service (NL)`: http://www.kb.nl/en/data-services-apis

- `US`_, Library of Congress `Terms of service (US)`_

::

  http://lx2.loc.gov:210/LCDB?operation=explain&version=1.1

.. _`US`: http://lx2.loc.gov:210/LCDB?operation=explain&version=1.1

.. _`Terms of service (US)`: http://www.loc.gov/z3950/lcserver.html

Z3950
~~~~~

- `Z39.50 Standard overview`_

.. _`Z39.50 Standard overview`: https://en.wikipedia.org/wiki/Z39.50

- `Practicle example python Z39.50 library`_

.. _`Practicle example python Z39.50 library`: https://lawlesst.github.io/notebook/z3950-scan.html

Z3950 endpoints
~~~~~~~~~~~~~~~
  
- `GB`_, British Library

.. _`GB`: http://www.bl.uk/bibliographic/z3950configuration.html

::

  Hostname: z3950cat.bl.uk
  Portname: 9909
  DatabaseName: ZBLACU or BNB03U

JSON
~~~~

- `JSON Standard overview`_

.. _`JSON Standard overview`: https://en.wikipedia.org/wiki/Json

JSON endpoints
~~~~~~~~~~~~~~

- `OpenLibrary`_

.. _`OpenLibrary`: https://openlibrary.org/dev/docs/api/

- `SE`_ LIBRIS - National Library of Sweden `Terms of service (SE)`_

.. _`SE`: http://libris.kb.se/xsearch?query=W.V.+Quine&format=json

.. _`Terms of service (SE)`: http://librishelp.libris.kb.se/help/tech_eng.jsp?open=tech


Dependencies
------------

- `isbnlib`_

.. _`isbnlib`: https://pypi.python.org/pypi/isbnlib

- `pycountry`_ 

.. _`pycountry`: https://pypi.python.org/pypi/pycountry

- `pymarc`_

.. _`pymarc`: https://pypi.python.org/pypi/pymarc

- `PyZ3950`_

.. _`PyZ3950`: https://pypi.python.org/pypi/PyZ3950

- `requests`_

.. _`requests`: https://pypi.python.org/pypi/requests

- `ujson`_

.. _`ujson`: https://pypi.python.org/pypi/ujson


Example usage and output
------------------------

Default invocation
~~~~~~~~~~~~~~~~~~

::

  $ booksearch
  Usage: booksearch <options(s)> query
    Searches for query in miscellaneous sources.
    The options are:

     -i --isbntrack     Get ISBN from first record/result,
                        query remaining endpoints with this ISBN
     -l --list          Show list of available endpoints, and default route
     -n --nostop        Continue untill all sources are queried
     -r --route         List of endpoints to query
     -s --stop          Stop if a record is returned (Default)
     -v --verbose       Verbose output

Simple search example
~~~~~~~~~~~~~~~~~~~~~

::

  $ booksearch 9789046703434
  dc_creator:
  dc_date:
  dc_description:
  dc_identifier:
  dc_language:
  dc_publisher:
  dc_terms:
  dc_title:
  dc_type:
  dcterms_abstract:
  dcterms_extent:

Simple search with verbosing example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

::

  $ booksearch 9789046703434 -v

Search example with routing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ booksearch 9789046703434 --nostop --route=NL,DE,UK,US,openlibrary,googlebooks


Using as library/embed
~~~~~~~~~~~~~~~~~~~~~~

::

  >>> from booksearch.api import API
  >>> from pprint import pprint

  >>> api = API()
  >>> api.query("9789046703434")
  >>> api.run()
  >>> pprint(api.results)
  {'endpoints': {'NL': {'found': 2,
                        'results': ['<result NL record 0>',
                                    '<result NL record 1>'],
                        'status_code': 200,
                        'time' : 10,
                        'done' : True,
                        'failed' : False},
                 'UK': {'found': 1,
                        'results': ['<result UK record 0>'],
                        'status_code': 200,
                        'time' : 100,
                        'done' : True,
                        'failed' : False}
                },
   'resultset': ['<result NL record 0>',
                 '<result NL record 1>',
                 '<result UK record 0>'],
   'query': '9789046703434',
   'query_time_total': 110}
