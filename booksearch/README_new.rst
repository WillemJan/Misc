BookSearch - Search for book metadata
=====================================

What is this?
-------------

BookSearch is a collection of protocols, formats and endpoints
for book metadata search via libraries, research institutes
and commercial
`available endpoints <https://booksearch.fe2.nl/available_endpoints.html>`_,
implemented in Python.

BookSearch is able to search your local national library,
if they expose an endpoint, many of them do,
without the need for keys, and they provide rich info.
The aim of this project is to provide easy access to
different sources of metadata, in a parallel fashion.

There are a couple of standards required to search the
metadata providers, some well known, others more obscure.
To get a sense of the search protocols, see
`search protocol overview <https://booksearch.fe2.nl/search_protocol_overview.html>`_.
Metadata in the library world can take on many forms, for
an overview of the implemented metadata formats see
`metadata formats overview <https://booksearch.fe2.nl/metadata_format_overview.html>`_.

Booksearch launches queries to it's endpoints in parallel mode,
results are collected as they come in, user is free to design
result merge strategies.

TL;DR code 
----------

From shell
----------
::

  Build // Install // Test // Patch ccl.py

  $ git clone git clone http://booksearch.fe2.nl/booksearch/.git
  $ cd booksearch
  $ sudo make
  $ sudo make install # or python setup.py install from a virtenv
  $ bs appel  # test it, ccl.py might be broken
  # sudo ./patch_ccl.sh # apply path ;)
  $ bs appel
  ...
  ...
  ...
  
From Python
-----------
::

  >>> from booksearch import BookSearch
  >>> booksearch = BookSearch()
  >>> result = booksearch.query("Scheveningen")
  >>> result.done
  False
  >>> result.todo
  'BL'

  >>> result
  <Result {"kb" : { "hits": 1329, "records" : [ "Record0" : { 'publisher' : '', 'creator' : '' }}

  # So this result is quite arbitrary, since we did not wait for all queries to finish.
  >>> result.getrecord(0)
  {"publisher" : "A",
   "creator" : "b"} 

Z39.50 legacy 
---------------

Since not a lot of humans use Z39.50, the Python library is a bit rusty.
In order to get it up and running again, apply the patch:

::

  $ ./patch_ccl.sh

If you don't you will probaly get an error like this:

::
    from PyZ3950 import ccl 
  File "/usr/local/lib/python2.7/dist-packages/PyZ3950-2.04-py2.7-linux-armv6l.egg/PyZ3950/ccl.py", line 141
    ImportError: No module named lex
    ImportError: No module named yacc


For now the only endpoint that uses this ancient gateway is the British
library. There is another thing to note about the Z39.50 library,
it has a habit of writing out a file called 'PyZ3950_parsetab.py',
the file is removed in the '__del__' method of the class BL. So
now you know, there is a call to os.remove in the code.


This document online:
`BookSearch website <http://booksearch.fe2.nl/>`_.
