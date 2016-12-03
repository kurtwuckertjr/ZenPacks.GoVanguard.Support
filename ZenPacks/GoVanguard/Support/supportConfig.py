from zope.interface import implements

from Products.ZenRelations.RelSchema import ToOne, ToManyCont
from Products.ZenModel.ZenModelRM import ZenModelRM
from Products.ZenUtils.guid.interfaces import IGloballyIdentifiable


class supportConfig(ZenModelRM):
    implements(IGloballyIdentifiable)

    meta_type = portal_type = "supportConfig"

    content = {}
    integration_name = ""

    def __init__(self, *args, **kwargs):
        super(supportConfig, self).__init__(*args, **kwargs)
        self.content = {}

