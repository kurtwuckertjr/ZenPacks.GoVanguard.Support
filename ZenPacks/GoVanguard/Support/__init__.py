import logging
import os
from zope.component import getUtility
from transaction import commit
from Products.Five.viewlet import viewlet
from Products.CMFCore.DirectoryView import registerDirectory
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

##
packageNameData = "ZenPacks.GoVanguard.Support"
packageVersionData = "1.0.0"
packageLicenseData = "Not Licensed"

log = logging.getLogger("zen.GoVanguard.Support")

# Extend all ManagedEntity derivative classes to add supportId
ManagedEntity.supportId = -1

IComponentInfo._InterfaceClass__attrs['supportId'] = IDeviceInfo._InterfaceClass__attrs['supportId'] = Int(title=u'Customer Identifier', readonly=True, group='Details')
DeviceInfo.supportId = ComponentInfo.supportId = property(lambda self: self._object.supportId)

# Register skins directory
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# Register theme CSS
GvitCSS = viewlet.CSSViewlet('skinRes/gvit.css')


# Base ZP Class
class ZenPack(ZenPackBase):
    def install(self, app):
        super(ZenPack, self).install(app)
        log.info('Adding supportSettings in to DMD')
        if not hasattr(app.zport.dmd,'supportSettings'):
            manage_addSupportSettings(app.zport.dmd)
            commit()
        app.zport.dmd.supportSettings.packageNameData = packageNameData
        app.zport.dmd.supportSettings.packageVersionData = packageVersionData
        app.zport.dmd.supportSettings.packageLicenseData = packageLicenseData
        commit()


    def upgrade(self, app):
        super(ZenPack, self).install(app)
        log.info('Updating supportSettings in to DMD')
        if hasattr(app.zport.dmd,'supportSettings'):
            app.zport.dmd._delObject('supportSettings')
            commit()
        if not hasattr(app.zport.dmd,'supportSettings'):
            manage_addSupportSettings(app.zport.dmd)
            commit()
        app.zport.dmd.supportSettings.packageNameData = packageNameData
        app.zport.dmd.supportSettings.packageVersionData = packageVersionData
        app.zport.dmd.supportSettings.packageLicenseData = packageLicenseData
        commit()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            log.info('Removing supportSettings from DMD')
            if hasattr(app.zport.dmd,'supportSettings'):
                app.zport.dmd._delObject('supportSettings')
                commit()
                log.info('Removing menus')
                DataRoot.factory_type_information[0]['actions'] = tuple([entry for entry in (DataRoot.factory_type_information[0]['actions']) if entry['action'] != 'gvitSupport'])
                UserSettingsManager.factory_type_information[0]['actions'] = tuple([entry for entry in (UserSettingsManager.factory_type_information[0]['actions']) if entry['action'] != 'gvitSupport'])
                ZenPackManager.factory_type_information[0]['actions'] = tuple([entry for entry in (ZenPackManager.factory_type_information[0]['actions']) if entry['action'] != 'gvitSupport'])
                ZenossInfo.factory_type_information[0]['actions'] = tuple([entry for entry in (ZenossInfo.factory_type_information[0]['actions']) if entry['action'] != 'gvitSupport'])
                commit()

        super(ZenPack, self).remove(app, leaveObjects)

# Factory extension definitions
extAction = {
             'id': 'gvitSupport',
             'name':'Support',
             'action':'gvitSupport',
             'permissions':("Manage DMD",)
             }

extUserAction = {
                 'id':'gvitSupport',
                 'name':'Support',
                 'action':'../gvitSupport',
                 'permissions':("Manage DMD",)
                }

extZenossInfoAction = {
                       'id':'gvitSupport',
                       'name': 'Support',
                       'action': '../dmd/gvitSupport',
                       'permissions':("Manage DMD",)
                      }

# Extend factories
actions = list(DataRoot.factory_type_information[0]['actions'])
actions.append(extAction)
newActions = tuple(actions)
DataRoot.factory_type_information[0]['actions'] = newActions

actions = list(UserSettingsManager.factory_type_information[0]['actions'])
actions.append(extUserAction)
newActions = tuple(actions)
UserSettingsManager.factory_type_information[0]['actions'] = newActions

actions = list(ZenPackManager.factory_type_information[0]['actions'])
actions.append(extUserAction)
newActions = tuple(actions)
ZenPackManager.factory_type_information[0]['actions'] = newActions

actions = list(ZenossInfo.factory_type_information[0]['actions'])
actions.append(extZenossInfoAction)
newActions = tuple(actions)
ZenossInfo.factory_type_information[0]['actions'] = newActions
