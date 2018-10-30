import logging
import json
from django.conf import settings
from .models import WirelessClient
from .dashboard import *

logger = logging.getLogger(__name__)
secret = settings.MERAKI_SCANAPI_SECRET

class Observations(object):
    def __init__(self):
        self.dashboard = None
    
    def process(self, data):
        if data['secret'] != secret:
            logger.info('Invalid secret')
            return

        if data['data']['apMac'] is None:
            logger.info('No apMac')
            return
        
        tags = {t[0]:t[1] for t in [tag.split(':') for tag in data['data']['apTags'] if tag] if len(t) == 2}
        logger.info(tags)
        
        ap = {'mac': data['data']['apMac'], 'tags': tags }

        for one in data['data']['observations']:
            self._processOne(ap, one)
        
    def last(self, ip):
        return  WirelessClient.objects.filter(ip__exact=ip).order_by('-seen_time')[0]

    def _processOne(self, ap, one):
        logger.info(one)
        if one['ipv4'] is not None and one['ssid'] is not None:
            logger.info("Client:" + one['ipv4'] + " on ssid:" + one['ssid'])
            if self.dashboard is None:
                self.dashboard = Meraki()
            dashboard_info = self.dashboard.getClientByMac(one['clientMac'])
            client = WirelessClient(mac = one['clientMac'], seen_time = one['seenTime'],
                    ip = one['ipv4'][1:], ap_mac = ap['mac'], ssid = one['ssid'], 
                    location = json.dumps(one['location']), user = dashboard_info['user'], 
                    tags = json.dumps(ap['tags']))
            client.save()


