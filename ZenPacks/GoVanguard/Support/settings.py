from Products.ZenModel.ZenModelRM import ZenModelRM
from Products.Zuul.utils import ZuulMessageFactory as _t
from copy import deepcopy

def manage_addSupportSettings(context, id="supportSettings"):
    settings = supportSettings(id)
    context._setObject(id, settings)
    return getattr(context, id)

class supportSettings(ZenModelRM):
    _relations = ()

    _exProperties = (
        {'id': 'packageNameData', 'type': 'string', 'mode': 'r'},
        {'id': 'packageVersionData', 'type': 'string', 'mode': 'r'},
        {'id': 'packageLicenseData', 'type': 'string', 'mode': 'r'},
        {'id': 'companyName', 'type': 'string', 'mode': 'w'},
        {'id': 'companyMotto', 'type': 'string', 'mode': 'w'},
        {'id': 'companyLink', 'type': 'string', 'mode': 'w'},
        {'id': 'companyBanner', 'type': 'string', 'mode': 'w'},
        {'id': 'supportKey', 'type': 'string', 'mode': 'w'},
        {'id': 'supportType', 'type': 'string', 'mode': 'w'},
        {'id': 'supportedPacks', 'type': 'list', 'mode': 'w'}
        )

    _exPropertyMetaData = {
        'packageNameData': {'xtype': 'textfield', 'name': _t('Package name'), 'defaultValue':'Unknown', 'allowBlank': False},
        'packageVersionData': {'xtype': 'textfield', 'name': _t('Package version'), 'defaultValue':'Unknown', 'allowBlank': False},
        'packageLicenseData': {'xtype': 'textfield', 'name': _t('Package license'), 'defaultValue':'Unlicensed', 'allowBlank': False},
        'companyName': {'xtype': 'textfield', 'name': _t('Company name'), 'defaultValue':'Unregistered Company', 'allowBlank': False},
        'companyMotto': {'xtype': 'textfield', 'name': _t('Company motto'), 'defaultValue':'', 'allowBlank': True},
        'companyLink': {'xtype': 'textfield', 'name': _t('Company link'), 'defaultValue':'http://gvit.com', 'allowBlank': True},
        'companyBanner': {'xtype': 'textfield', 'name': _t('Company banner'), 'defaultValue':'', 'allowBlank': True},
        'supportKey': {'xtype': 'textfield', 'name': _t('Support Key'), 'defaultValue':'', 'allowBlank': True},
        'supportType': {'xtype': 'textfield', 'name': _t('Support Type'), 'defaultValue':'Unsupported', 'allowBlank': False},
        'supportedPacks': {'xtype': 'textfield', 'name': _t('Supported Packages'), 'defaultValue':'None', 'allowBlank': False}
        }

    def getSupportSettingsData(self):
        """
        @rtype: Dictionary
        @return: The value of the settings along with some meta information
        for display
        """
        settings = deepcopy(self._exProperties)
        for prop in settings:
            prop.update(self._exPropertyMetaData[prop['id']])
            prop['value'] = getattr(self, prop['id'], prop['defaultValue'])
        return settings

    def getPackageVersion(self):
        try:
            result = self.packageVersionData
        except:
            result = ''
        return result

    def getPackageName(self):
        try:
            result = self.packageNameData
        except:
            result = ''
        return result

    def getPackageLicense(self):
        try:
            result = self.packageLicenseData
        except:
            result = ''
        return result

    def getCompanyName(self):
        try:
            result = self.companyName
        except:
            result = ''
        return result

    def getCompanyMotto(self):
        try:
            result = self.companyMotto
        except:
            result = ''
        return result

    def getCompanyLink(self):
        try:
            result = self.companyLink
        except:
            result = ''
        return result

    def getCompanyBanner(self):
        try:
            result = self.companyBanner
        except:
            result = ''
        return result
