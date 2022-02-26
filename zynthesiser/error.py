import logging


class ZynthesiserException(Exception):
    def __init__(self, value):
        super().__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

    
def get_zynthesiser_logger():    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(style='{')
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    return logger
