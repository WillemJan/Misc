import logging

__all__ = ['logger',
          ]

DEFAULT_LOGLEVEL = logging.WARNING
LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

def logger(name, loglevel='warning'):

    try:
        loglevel = getattr(logging,
                [l for l in dir(logging) if l.isupper() and l.lower() == loglevel].pop())
    except:
        loglevel = DEFAULT_LOGLEVEL

    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loglevel)
    return logger

logger('test')
