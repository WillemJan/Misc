# -*- coding: utf-8 -*-
"""
    The basic sql functionality, using sqlite.

    :class:`~Fe2.tools.sql`
"""

import os
from sqlalchemy.engine import create_engine

import Fe2.tools.log


def Sql():
    def __init__(sefl):
        """
            Fe2.tools.Sql
            ~~~~~~~~~~~~~

            Implements basic Sql wrapper object for sqlite.
        """
        pass

    @staticmethod
    def _test_sqlite():
        """
            >>> test_sqlite()
            username: foo

        """
        engine = create_engine('sqlite:///:memory:', echo=False)
        connection = engine.connect()
        connection.execute("""
            CREATE TABLE users (
                username VARCHAR PRIMARY KEY,
                password VARCHAR NOT NULL
            );
            """)
        connection.execute("""
            INSERT INTO users (username, password) VALUES (?, ?);
            """,
            "foo", "bar")
        result = connection.execute("SELECT username FROM users")
        for row in result:
            print "username:", row['username']
        connection.close()
