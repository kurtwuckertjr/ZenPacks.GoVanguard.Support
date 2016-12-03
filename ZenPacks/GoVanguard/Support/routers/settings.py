from Products.ZenUtils.Ext import DirectRouter
from Products.ZenUtils.extdirect.router import DirectResponse
from Products.Zuul.decorators import require
from Products import Zuul
from Products.ZenMessaging.audit import audit


class supportSettingsRouter(DirectRouter):
    """
    A JSON/ExtDirect interface to operations on settings
    """

    def _getSupportSettings(self):
        return self.context.zport.dmd.supportSettings

    def getSupportSettings(self):
        """
        Retrieves the collection of settings
        """
        settings = self._getSupportSettings()
        return DirectResponse.succeed(data=Zuul.marshal(settings.getSupportSettingsData()))

    @require('Manage DMD')
    def setSupportSettings(self, **kwargs):
        """
        Accepts key value pair of settings
        """
        settings = self._getSupportSettings()
        oldValues = {}
        newValues = {}
        for key, value in kwargs.iteritems():
            oldValues[key] = str(getattr(settings, key, None))
            newValues[key] = str(value)
            setattr(settings, key, value)
        return DirectResponse.succeed()

    def getSupportedPacks(self):
        """
        Retrieves the collection of supported ZenPacks
        """
        settings = self._getSupportSettings()
        return DirectResponse.succeed(data=Zuul.marshal(settings.getSupportedPacksData()))

    def getPackageVersion(self):
        return self.packageVersionData

    def getPackageName(self):
        return self.packageNameData

    def getPackageLicense(self):
        return self.packageLicenseData
