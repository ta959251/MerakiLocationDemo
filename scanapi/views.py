from django.shortcuts import render
import logging
from django.http import HttpResponse, HttpResponseRedirect
import json
from .observations import *
from .dashboard import *
from django.template import loader
import after_response
from .models import WirelessClient, News
from django.conf import settings

logger = logging.getLogger(__name__)

def index(request):
    logger.info(request.META)
    return HttpResponse("Hello, Scan API.")

def event(request):
    if request.method == 'GET':
        return HttpResponse(settings.MERAKI_SCANAPI_VALIDATION)
    elif request.method == 'POST':
        logger.info("Got post")
        data = json.loads(request.body)

        @after_response.enable
        def do_it_after(_data):
            Observations().process(_data)

        do_it_after.after_response(data) 
        return HttpResponse(status=204)


def info(request):
    client = request.META['REMOTE_ADDR']
    return infoImpl(request, client)

def info_client(request,client):
    return infoImpl(request, client)

def infoImpl(request, client):
    logger.info(str(request.META))
    wclient = None
    news = None
    try:
        wclient = Observations().last(client)
        wclient.location = json.loads(wclient.location)
        wclient.tags = json.loads(wclient.tags)
        office = wclient.tags['office']
        logger.info('Office=' + office)
        news = News.objects.filter(site__exact=office).order_by('-timestamp')
        logger.info('News=' + str(news))
    except: 
        pass
    
    template = loader.get_template('scanapi/info.html')
    context = {
        'client': wclient,
        'news' : news,
        'apikey' : settings.WRLD3D_APIKEY
    }
    return HttpResponse(template.render(context, request))
