import logging

class Ramdrive(object):
    RAMDRIVE_PATH = '/var/shm'

    def __init__(self):
        pass



class Log(object):
    LOG_FILENAME = '/tmp/prutsgood.log'
    
    def __init__(self):
        logging.basicConfig(filename=self.LOG_FILENAME,level=logging.DEBUG,)

    def msg(self, st):
        logging.info(st)
