# -*- coding: utf-8 -*-
"""
    The basic config functionality.

    >>> config = Config()
    >>> if config.get_section('Fe2'):
    >>>     print(config.get('Fe2', 'debug'))
    True

    :class:`~Fe2.tools.config`
"""

import os
import ConfigParser
import codecs
import Fe2.tools.log

__version__ = "1.0"


class Config(dict):
    """
        Config parser, reads the default config defined
        by PATH + ``'os.sep'`` + EXTENTION.

        defaults to $HOME/.fe2.ini.
    """

    PATH = os.environ["HOME"]
    EXTENTION = ".fe2.ini"
    config = {u"Fe2": [u"debug", u"true"]}

    log = Fe2.tools.log.create_logger(__name__)
    log.info("Running %s version %s" % (__name__, __version__))

    @staticmethod
    def _test_config():
        """
            Simple method for testing.

            >>> c = Config
            >>> c.test_config()
            [('test1', '1'), ('test2', '2')]
        """
        config = ConfigParser.ConfigParser()
        from StringIO import StringIO
        fh = StringIO("[test_config]\ntest1: 1\ntest2: 2\n")
        config.readfp(fh)
        print config.items('test_config')

    def __path__(self):
        return(self.PATH + os.sep + self.EXTENTION)

    def read(self, path=None, extention=None):
        """
            Read config file from path.

            :param extention: optional extention to the configfile, defaults
                          to: .fe2.ini.
            :param path: optional path to the configfile, defaults
                         to: $HOME/.fe2.ini.
        """
        if extention:
            self.EXTENTION = extention
        if path:
            self.PATH = path
        parser = ConfigParser.SafeConfigParser()
        self.log.info("Reading config file %s" % self.__path__())
        if os.path.isfile(self.__path__()):
            with codecs.open(self.__path__(), 'r', encoding='utf-8') as fh:
                parser.readfp(fh)
        else:
            self.log.warn("No config file to read at %s" % self.__path__())
            return(None)
        return(parser)

    def write(self, path=None, extention=None):
        """
            Write config file to path.

            :param path: optional path to write configfile to.
                         defaults to $HOME.
            :param extention: optional extention for configfile.
                              defaults to .fe2.ini
        """

        if path:
            self.PATH = path
        if extention:
            self.EXTENTION = extention
        parser = ConfigParser.SafeConfigParser()
        fh = codecs.open(self.__path__(), 'w', encoding='utf-8')
        for item in self.config:
            parser.add_section(item)
            for row in self.config[item]:
                parser.set(item,
                            self.config[item][row.numerator - 1],
                            self.config[item][row.numerator])
        parser.write(fh)

    def __init__(self):
        c = self.read()
        if not c:
            self.write()
