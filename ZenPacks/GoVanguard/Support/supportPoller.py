import logging
import Globals
import datetime
import time
from zope.component import getUtility
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.ZenUtils.CyclingDaemon import CyclingDaemon
from Products.ZenUtils.Utils import unused
from zenoss.protocols.services import ServiceResponseError
from Products.Zuul import getFacade
from ZODB.transact import transact

unused(Globals)

DAEMON = "supportPoller"

class supportPoller(CyclingDaemon):
    name = DAEMON

    def __init__(self, *args, **kwargs):
        super(supportPoller, self).__init__(*args, **kwargs)
        self.deviceFacade = getFacade('device', self.dmd)
        self.zport = self.dmd.zport
        self.sync = self.zport._p_jar.sync
        self.log = logging.getLogger("zen.GoVanguard.Support.Poller")
        self.cycleNumber = 0

    def main_loop(self):
        """
        Cycle through the devices and add or update as neccesarry.
        """
        ts = time.time()
        self.log.info("Syncing with ZODB...")
        self.sync()
        self.sync() 
        self.log.info("Processing results...")
        te = time.time()
        tf = te-ts
        self.cycleNumber = self.cycleNumber + 1
        self.log.info('Cycle #%s took %2.2f sec!' % (str(self.cycleNumber), tf))        
        self.log.info("Waiting for next cycle...")

    def buildOptions(self):
        super(supportPoller, self).buildOptions()
        self.parser.set_defaults(cycletime=1)


if __name__ == "__main__":
    daemon = supportPoller()
    daemon.run()

