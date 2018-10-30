from django.conf import settings

try:
    from .mymeraki import *
except:
    import mymeraki 


import logging
logger = logging.getLogger(__name__)

class Meraki(object):
    
    apikey = settings.MERAKI_DASHBOARD_KEY
    
    def __init__(self):
        self.org_id = myorgaccess(self.apikey, True)[0]['id']
        self.net_list = [ net['id'] for net in getnetworklist(self.apikey, self.org_id, suppressprint=True) ]

    def getClientByMac(self, mac):
        for net in self.net_list:
            client = getclient(self.apikey, net, mac)
            if client is not None:
                return client
        return None

