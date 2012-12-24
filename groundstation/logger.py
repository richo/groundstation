import logging

LEVEL = logging.DEBUG # TODO hang this off an environment variable.

def _get_formatter():
    return logging.Formatter('%(name)s - %(levelname)s - %(message)s')

CONSOLE_FORMATTER = _get_formatter()

def _get_console_handler():
    ch = logging.StreamHandler()
    ch.setLevel(LEVEL)
    ch.setFormatter(CONSOLE_FORMATTER)
    return ch

CONSOLE_HANDLER = _get_console_handler()

LOGGERS = {} # Cache for instanciated loggers

def getLogger(name): # Not threadsafe
    if name in LOGGERS:
        return LOGGERS[name]
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    logger.addHandler(CONSOLE_HANDLER)

    LOGGERS[name] = logger
    return logger
