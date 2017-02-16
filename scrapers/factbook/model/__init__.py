"""The application's model objects"""
import sqlalchemy as sa
import os
from couchdb import Server
from couchdb import schema

def init_model(engine):
    dir(schema)
    pass

def get_db():
    try:
        server=Server("http://127.0.0.1:5984/")
        if 'test' not in server:
            server.create('test')
        db = server['test']
    except:
        print ("DB_ERROR")
        os._exit(-1)
    return(db)

class Factsheet(schema.Document):
    id = schema.TextField()
    name = schema.TextField()
    factsheet = schema.TextField()
    
#def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #

#    meta.Session.configure(bind=engine)
#    meta.engine = engine


## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)

## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
