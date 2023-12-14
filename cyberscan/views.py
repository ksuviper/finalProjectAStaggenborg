from django.shortcuts import render, get_object_or_404, redirect
from cyberscan.functions import *


# Create your views here.
def index(request):
    """index page"""
    user_ip = get_my_ip()
    isp = get_isp(user_ip)

    return render(request, "cyberscan/index.html", {"user_ip": user_ip, "isp": isp})


def trace(request):
    """trace page"""
    if request.GET.get("id") is not None:
        """pull up saved trace results"""
        pk_id = request.GET.get("id")
        tr = get_object_or_404(Trace, pk=pk_id)

        tr_hops = tr.traceresult_set.values_list()
        ipaddr = tr.IPAddress
        hops = {}
        for i, hop, ip, reply in tr_hops:
            """add geolocation data to trace data dictionary and format for viewing to match non-saved data"""
            hops.update({hop: [ip, reply, get_ip_geodata(ip)]})

        return render(request, "cyberscan/traceresult.html", {"ipaddr": ipaddr, "hops": hops})
    elif request.GET.get("ipaddr") is not None:
        """start new trace"""
        ipaddr = request.GET.get("ipaddr")
        saveresult = request.GET.get("save_results")

        conf.geoip_city = "GeoLite2-City.mmdb"

        tr = run_traceroute(ipaddr, saveresult)

        hops = {}
        for h in tr:
            """add location data to trace data dictionary"""
            ip = tr.get(h)[0]
            reply = tr.get(h)[1]
            hops.update({h: [ip, reply, get_ip_geodata(ip)]})

        return render(request, "cyberscan/traceresult.html", {"ipaddr": ipaddr, "hops": hops})
    else:
        """trace page"""
        """list traces that have been saved from the current user's IP"""
        traces = Trace.objects.filter(UserIP__exact=get_my_ip()).values_list()
        userip = get_my_ip()

        return render(request, "cyberscan/trace.html", {"tr_list": traces, "userip": userip})


def scan(request):
    """scan page"""
    if request.GET.get("id") is not None:
        """pull up saved trace results"""
        pk_id = request.GET.get("id")
        sc = get_object_or_404(Scan, pk=pk_id)
        network = sc.NetworkIPs
        ports = sc.Ports
        loadedscan = sc.scanresult_set.all()

        return render(request, "cyberscan/scanresult2.html", {"network": network, "ports": ports, "loadedscan": loadedscan})
    elif request.GET.get("network") is not None:
        """start new scan"""
        network = request.GET.get("network")
        ports = request.GET.get("ports")
        saveresult = request.GET.get("save_results")

        scan_results = run_network_scan(network, ports=ports, save_result=saveresult)
        return render(request, "cyberscan/scanresult.html", {"network": network, "ports": ports, "scan_results": scan_results})
    else:
        """scan page"""
        """list scans that have been saved from the current user's IP"""
        scans = Scan.objects.filter(UserIP__exact=get_my_ip()).values_list()
        userip = get_my_ip()

    return render(request, "cyberscan/scan.html", {"userip": userip, "scans": scans})

