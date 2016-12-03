from subprocess import Popen, PIPE
from Products.Five.browser import BrowserView
from Products.ZenUtils.Utils import zenPath
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import logging

class authCertificateUpload(BrowserView):
    """
    Handeler for certificate data upload. Only PEM format.
    """

    log = logging.getLogger("zen.ZenPacks.GoVanguard.Support.Authentication")
    redirect = ViewPageTemplateFile('../templates/portalTemplates/authentication.pt')

    def __call__(self, *args, **kwargs):
        if self.request.get('fileData'):
            destination = zenPath("etc", "authenticationCertificate.pem")
            fileData = self.request.get('fileData').read()
            with open(destination, "w") as w:
                w.write(fileData)
        return self.redirect()


class brandingUpload(BrowserView):
    """
    Handeler for branding image upload. Restarts Zope after writing uploaded file.
    """

    log = logging.getLogger("zen.ZenPacks.GoVanguard.Support.Branding")
    redirect = ViewPageTemplateFile('../templates/portalTemplates/branding.pt')

    def __call__(self, *args, **kwargs):
        if self.request.get('fileData'):
            destination = zenPath("ZenPacks", "ZenPacks.GoVanguard.Support-1.0.0.egg/ZenPacks/GoVanguard/Support/skins/Support/company-logo.png")
            fileData = self.request.get('fileData').read()
            with open(destination, "w") as w:
                w.write(fileData)
                command = "zopectl restart" 
                try:
                    systemCall = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
                    stdout, stderr = systemCall.communicate()
                    if systemCall.returncode != 0:
                        log.warn("Unable to complete. Why?: %s Error: %s", stdout, stderr)
                except Exception:
                    log.exception("Unable to complete.")
        return self.redirect()


class licenseUpload(BrowserView):
    """
    Handeler for license data upload. Only x509 format.
    """

    log = logging.getLogger("zen.ZenPacks.GoVanguard.Support.Licensing")
    redirect = ViewPageTemplateFile('../templates/portalTemplates/licensing.pt')

    def __call__(self, *args, **kwargs):
        if self.request.get('fileData'):
            destination = zenPath("etc", "gvitSupportLicense.pem")
            fileData = self.request.get('fileData').read()
            with open(destination, "w") as w:
                w.write(fileData)
        return self.redirect()
