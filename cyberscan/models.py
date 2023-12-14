from django.db import models


# Create your models here.
class Scan(models.Model):
    ScanDate = models.DateTimeField()
    NetworkIPs = models.CharField(max_length=100)
    Ports = models.CharField(max_length=20)
    UserIP = models.GenericIPAddressField(protocol="IPv4")

    def __str__(self):
        return self.NetworkIPs


class ScanResult(models.Model):
    Scan = models.ManyToManyField(Scan)
    IPAddress = models.GenericIPAddressField(protocol="IPv4")
    Hostname = models.CharField(max_length=100)
    Status = models.CharField(max_length=20)

    def __str__(self):
        return self.IPAddress


class PortsScanned(models.Model):
    ScanResult = models.ManyToManyField(ScanResult)
    Port = models.PositiveSmallIntegerField()
    Status = models.CharField(max_length=20)

    def __str__(self):
        return self.Port


class Trace(models.Model):
    TraceDate = models.DateTimeField()
    IPAddress = models.GenericIPAddressField(protocol="IPv4")
    UserIP = models.GenericIPAddressField(protocol="IPv4")

    def __str__(self):
        return self.IPAddress


class TraceResult(models.Model):
    Trace = models.ManyToManyField(Trace)
    Hop = models.PositiveSmallIntegerField()
    HopIP = models.GenericIPAddressField(protocol="IPv4")
    HopReply = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.HopIP
