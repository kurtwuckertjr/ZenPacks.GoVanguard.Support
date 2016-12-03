from Products.ZenModel.ZenModelRM import ZenModelRM
from Products.Zuul.utils import ZuulMessageFactory as _t
from copy import deepcopy

def manage_addSupportSettings(context, id="supportSettings"):
    settings = supportSettings(id)
    context._setObject(id, settings)
    return getattr(context, id)

class supportSettings(ZenModelRM):
    _relations = ()

    _supportProperties = (
        {'id': 'CompanyName', 'type': 'string', 'mode': 'w'},
        {'id': 'SupportKey', 'type': 'string', 'mode': 'w'},
        {'id': 'SupportType', 'type': 'string', 'mode': 'w'}
        )

    _supportPropertyMetaData = {
        'CompanyName': {'xtype': 'textfield', 'name': _t('Company name'), 'defaultValue':'Unregistered Company', 'allowBlank': False},
        'SupportKey': {'xtype': 'textfield', 'name': _t('Support Key'), 'defaultValue':'', 'allowBlank': True},
        'SupportType': {'xtype': 'textfield', 'name': _t('Support Type'), 'defaultValue':'Unsupported', 'allowBlank': False}
        }


    def getSupportSettingsData(self):
        """
        @rtype: Dictionary
        @return: The value of the settings along with some meta information
        for display
        """
        settings = deepcopy(self._supportProperties)
        for prop in settings:
            prop.update(self._supportPropertyMetaData[prop['id']])
            prop['value'] = getattr(self, prop['id'], prop['defaultValue'])
        return settings
