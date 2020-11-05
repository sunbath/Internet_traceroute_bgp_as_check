import requests
from requests.exceptions import HTTPError
from prettytable import PrettyTable
from ipaddress import IPv4Address
import re

# Functions

# Read Juniper Traceroute File and return a list of hop ips
def read_juniper_traceroute_file(file):
    textfile = open(file, 'r')
    matches = []
    reg = re.compile(
        r"\d{1,2}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]|\d{1,2}\s\*\s\*\s\*")
    for line in textfile:
        matches += reg.findall(line)
    textfile.close()
    traceroute_hops = []

    for hop in matches:
        traceroute_hops.append(hop.split(' ')[1])

    return traceroute_hops

def check_invalid_ip(ip):
    # Check if IPv4 address is private
    if ip == "*":
        return False
    elif IPv4Address(ip).is_private:
        return False
    else:
        return True

# Variables
# traceroute_hops = ["121.244.40.162", "180.87.36.9", "180.87.36.41", "180.87.96.130","202.84.224.189", "202.84.143.177", "202.84.249.14", "42.99.163.9"]


traceroute_hops = read_juniper_traceroute_file("juniper_traceroute.txt")

# Output Display Configuration
PTable = PrettyTable()
PTable.field_names = ["Hop", "IP Address", "Country", "AS Number - Telco Info"]
PTable.align["Hop"] = 'm'
PTable.align["IP Address"] = 'l'
PTable.align["Country"] = 'm'
PTable.align["AS Number - Telco Info"] = 'l'

hop_count = 1
for hop_ip in traceroute_hops:
    if check_invalid_ip(hop_ip):
        try:
            url = "http://ip-api.com/json/{}?fields=status,country,region,regionName,city,isp,org,as,query".format(
                hop_ip)
            response = requests.get(url)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print('HTTP error occurred: {http_err} on hop #{}'.format(hop_count))
        except Exception as err:
            print('Other error occurred: {err} on hop #{}'.format(hop_count))
        else:
            # print('Success!')
            result = response.json()
            # print(result)
            IP_Address = result['query']
            Country = result['country']
            ASN = result['as']
            PTable.add_row([hop_count, IP_Address, Country, ASN])
            hop_count += 1
    else:
        PTable.add_row([hop_count, hop_ip, "N/A", "N/A"])
        hop_count += 1

print(PTable)
