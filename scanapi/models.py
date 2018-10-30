from django.db import models

# Create your models here.

class WirelessClient(models.Model):
    mac = models.CharField(max_length=30)
    seen_time = models.DateTimeField()
    ip = models.GenericIPAddressField()
    ap_mac = models.CharField(max_length=30)
    ssid = models.CharField(max_length=100)
    location = models.TextField()
    user = models.CharField(max_length=100,null=True)
    tags = models.TextField(null=True)


class News(models.Model):
    timestamp = models.DateTimeField()
    site = models.CharField(max_length=100)
    news = models.TextField()
