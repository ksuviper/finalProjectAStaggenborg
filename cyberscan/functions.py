import requests
from scapy.all import *
from scapy.layers.inet import traceroute
from constants import *
from .models import Scan, ScanResult, Trace, TraceResult
import ipaddress
import nmapthon2 as nm2


def is_ipv4(ip_addr):
    try:
        ipaddress.IPv4Network(ip_addr)
        return True
    except ValueError:
        return False


def get_my_ip():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify=True)

    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
        exit()

    data = response.json()

    return data['ip']


def get_isp(ip_addr):
    api_url = 'https://api.api-ninjas.com/v1/iplookup?address={}'.format(ip_addr)
    response = requests.get(api_url, headers={'X-Api-Key': API_NINJA_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()['isp']
    else:
        return "Error:", response.status_code, response.text


def get_ip_geodata(ip_addr):
    # """get ip if domain"""
    # if not is_ipv4(ip_addr):
    #     print("not valid IPv4 address")
    #     api_url = 'https://api.api-ninjas.com/v1/dnslookup?domain={}'.format(ip_addr)
    #     response = requests.get(api_url, headers={'X-Api-Key': API_NINJA_KEY})
    #     if response.status_code == requests.codes.ok:
    #         dnsdata = dict(requests.json())
    #         for key, value in dnsdata.items():
    #             print(key, value)
    #     else:
    #         print("Error:", response.status_code, response.text)

    # api_url = 'https://api.api-ninjas.com/v1/iplookup?address={}'.format(ip_addr)
    # response = requests.get(api_url, headers={'X-Api-Key': API_NINJA_KEY})
    api_url = 'https://ipinfo.io/{}/json'.format(ip_addr)
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        geodata = response.json()
        try:
            city = geodata['city']
            region = geodata['region']
            country = geodata['country']
            isp = get_isp(ip_addr)
            geo_loc = isp+" ("+city+", "+region+", "+country+")"
        except KeyError as ke:
            geo_loc = "Private IP"

        return geo_loc
    else:
        return "Error:", response.status_code, response.text


def get_ip_geocoords(ip_addr):
    # api_url = 'https://api.api-ninjas.com/v1/iplookup?address={}'.format(ip_addr)
    # response = requests.get(api_url, headers={'X-Api-Key': API_NINJA_KEY})
    api_url = 'https://ipinfo.io/{}/json'.format(ip_addr)
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        try:
            loc = response.json()['loc']
        except KeyError as ke:
            loc = "No Location Data Available"

        return loc
    else:
        return "Error:", response.status_code, response.text


def run_traceroute(ip_addr, save_result):
    """run traceroute"""
    trace, packets = traceroute(ip_addr, verbose=0)

    tr = trace.get_trace()
    tr_keys = tr.get(list(tr.keys())[0])
    hops = dict(sorted(tr_keys.items()))

    if save_result == "on":
        """save trace results"""
        t = Trace(TraceDate=datetime.now(), IPAddress=ip_addr, UserIP=get_my_ip())
        t.save()

        for h in hops:
            hop_ip = hops[h][0]
            hop_reply = hops[h][1]
            t.traceresult_set.create(Hop=h, HopIP=hop_ip, HopReply=hop_reply)

    return hops


def run_network_scan(network, ports="1-1024", scanner_args="-sS -T4", save_result=""):
    sc = nm2.NmapScanner()
    result = sc.scan(network, ports=ports, arguments=scanner_args)
    # print(result)
    if save_result == "on":
        """save scan results"""
        s = Scan(NetworkIPs=network, Ports=ports, ScanDate=datetime.now(), UserIP=get_my_ip())
        s.save()

        for host in result:
            # Get state, reason and hostnames
            hname = ""
            for hostname in host.hostnames():
                hname = hostname
            print(host.ip, hname)
            p = s.scanresult_set.create(IPAddress=host.ip, Hostname=hname, Status=host.state)

            # Get scanned protocols
            for port in host:
                # Get scanned ports
                print(port.number, port.state)
                p.portsscanned_set.create(Port=port.number, Status=port.state)

    return result
