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
        traces = Trace.objects.filter(UserIP__exact=get_my_ip()).values()
        userip = get_my_ip()

        return render(request, "cyberscan/trace.html", {"tr_list": traces, "userip": userip})


def scan(request):
    """scan page"""

    return render(request, "cyberscan/scan.html")


def traceresult(request, trace_id):
    """trace result page"""
    tr = get_object_or_404(Trace, pk=trace_id)

    return render(request, "cyberscan/traceresult.html", {"traceresult": tr})


def scanresult(request, scan_id):
    """scan result page"""
    s = get_object_or_404(Scan, pk=scan_id)
    return render(request, "cyberscan/scanresult.html", {"scanresult": s})


