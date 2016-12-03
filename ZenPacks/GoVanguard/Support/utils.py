import logging
import time

def timeIt(method):
    def timed(*args, **kw):
        log = logging.getLogger("zen.GoVanguard.Support.Stats")
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        tf = te-ts
        if tf > 10:
            log.warn('%r took over %2.2f sec! Too long!' % (method.__name__, tf))
        else:
            log.info('%r took %2.2f sec!' % (method.__name__, tf))
        return result
    return timed
