import requests
import json
from scapy.layers.inet import traceroute
from constants import *
from scapy import all


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


def run_traceroute(ip_addr, save_result):
    """run traceroute"""
    tr = traceroute(ip_addr)
    if save_result == "on":
        """save trace results"""



    return tr

