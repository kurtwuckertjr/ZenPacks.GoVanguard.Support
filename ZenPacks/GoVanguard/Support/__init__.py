import logging
import os
from zope.component import getUtility
from transaction import commit
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.Zuul.interfaces import IDeviceInfo, IComponentInfo
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.form.schema import Int
from ZenPacks.GoVanguard.Support.settings import manage_addSupportSettings
from Products.ZenModel.DataRoot import DataRoot
from Products.ZenModel.UserSettings import UserSettingsManager
from Products.ZenModel.ZenPackManager import ZenPackManager
from Products.ZenModel.ZenossInfo import ZenossInfo
from Products.ZenModel.ZenossSecurity import *

log = logging.getLogger("zen.GoVanguard.Support")

# Extend all ManagedEntity derivative classes to add supportId
ManagedEntity.supportId = -1

IComponentInfo._InterfaceClass__attrs['supportId'] = IDeviceInfo._InterfaceClass__attrs['supportId'] = Int(title=u'Customer Identifier', readonly=True, group='Details')
DeviceInfo.supportId = ComponentInfo.supportId = property(lambda self: self._object.supportId)

# Base ZP Class
class ZenPack(ZenPackBase):
    def install(self, app):
        super(ZenPack, self).install(app)
        os.system('easy_install -U setuptools')
        os.system('easy_install suds-jurko')
        log.info('Adding supportSettings in to DMD')
        if not hasattr(app.zport.dmd,'supportSettings'):
            manage_addSupportSettings(app.zport.dmd)
            commit()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            log.info('Removing supportSettings from DMD')
            if hasattr(app.zport.dmd,'supportSettings'):
                app.zport.dmd._delObject('supportSettings')
                commit()
                log.info('Removing menus')
                DataRoot.factory_type_information[0]['actions'] = tuple([entry for entry in (DataRoot.factory_type_information[0]['actions']) if entry['action'] != 'support'])
                UserSettingsManager.factory_type_information[0]['actions'] = tuple([entry for entry in (UserSettingsManager.factory_type_information[0]['actions']) if entry['action'] != 'support'])
                ZenPackManager.factory_type_information[0]['actions'] = tuple([entry for entry in (ZenPackManager.factory_type_information[0]['actions']) if entry['action'] != 'support'])
                ZenossInfo.factory_type_information[0]['actions'] = tuple([entry for entry in (ZenossInfo.factory_type_information[0]['actions']) if entry['action'] != 'support'])
                commit()
        super(ZenPack, self).remove(app, leaveObjects)

# Factory extension definitions
extAction = {
             'id': 'support',
             'name':'Support',
             'action':'support',
             'permissions':("Manage DMD",)
             }

extUserAction = {
                 'id':'support',
                 'name':'Support',
                 'action':'../support',
                 'permissions':("Manage DMD",)
                }

extZenossInfoAction = {
                       'id':'support',
                       'name': 'Support',
                       'action': '../dmd/support',
                       'permissions':("Manage DMD",)
                      }

# Extend factories
actions = list(DataRoot.factory_type_information[0]['actions'])
actions.append(extAction)
newActions = tuple(actions)
DataRoot.factory_type_information[0]['actions'] = newActions
# DataRoot.factory_type_information[0]['actions'] = tuple([entry for entry in (DataRoot.factory_type_information[0]['actions']) if entry['action'] != 'support'])

actions = list(UserSettingsManager.factory_type_information[0]['actions'])
actions.append(extUserAction)
newActions = tuple(actions)
UserSettingsManager.factory_type_information[0]['actions'] = newActions
# UserSettingsManager.factory_type_information[0]['actions'] = tuple([entry for entry in (UserSettingsManager.factory_type_information[0]['actions']) if entry['action'] != 'support'])

actions = list(ZenPackManager.factory_type_information[0]['actions'])
actions.append(extUserAction)
newActions = tuple(actions)
ZenPackManager.factory_type_information[0]['actions'] = newActions
# ZenPackManager.factory_type_information[0]['actions'] = tuple([entry for entry in (ZenPackManager.factory_type_information[0]['actions']) if entry['action'] != 'support'])

actions = list(ZenossInfo.factory_type_information[0]['actions'])
actions.append(extZenossInfoAction)
newActions = tuple(actions)
ZenossInfo.factory_type_information[0]['actions'] = newActions
# ZenossInfo.factory_type_information[0]['actions'] = tuple([entry for entry in (ZenossInfo.factory_type_information[0]['actions']) if entry['action'] != 'support'])
