from django.db import models


# Create your models here.
class Scan(models.Model):
    ScanDate = models.DateTimeField()
    NetworkIPStart = models.GenericIPAddressField(protocol="IPv4")
    NetworkIPEnd = models.GenericIPAddressField(protocol="IPv4")
    PortStart = models.PositiveSmallIntegerField()
    PortEnd = models.PositiveSmallIntegerField()
    UserIP = models.GenericIPAddressField(protocol="IPv4")

    def __str__(self):
        return self.NetworkIPStart + "-" + self.NetworkIPEnd


class ScanResult(models.Model):
    Scan = models.ManyToManyField(Scan)
    IPAddress = models.GenericIPAddressField(protocol="IPv4")
    ResponseTime = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.IPAddress


class PortsScanned(models.Model):
    ScanResult = models.ManyToManyField(ScanResult)
    Port = models.PositiveSmallIntegerField()
    Status = models.BooleanField()

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
    HopIP = models.GenericIPAddressField(protocol="IPv4")
    HopReply = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.HopIP


