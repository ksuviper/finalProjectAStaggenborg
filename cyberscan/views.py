from django.shortcuts import render, get_object_or_404
from .models import Scan, ScanResult, Trace, TraceResult
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

    elif request.GET.get("ipaddr") is not None:
        """start new trace"""
        ipaddr = request.GET.get("ipaddr")
        saveresult = request.GET.get("swSave")

        tresults = run_traceroute(ipaddr, saveresult)

        if saveresult == "on":
            """load saved results from returned id"""
            trace_id = tresults


        return render(request, "cyberscan/traceresult.html", {"ipaddr": ipaddr, "saveresults": saveresult, "traceresults": tresults})
    else:
        return render(request, "cyberscan/trace.html")


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


