from ipaddress import IPv4Address
from re import compile, findall

import requests
from prettytable import PrettyTable
from requests.exceptions import HTTPError

# Variables

# Specify the traceroute file
traceroute_file = "juniper_traceroute.txt"

# Base URL to get IP info
# Here I use ip-api.com to gather the necessary ip information for each hop ip
# String output from ip-api.com from this API call:
# {"status": "success", "country": "India", "region": "TN", "regionName": "Tamil Nadu", "city": "Chennai", "isp": "Tata Communications Limited","org": "VSNL", "as": "AS4755 TATA Communications formerly VSNL is Leading ISP", "query": "121.244.40.162"}
# The output is a string with JSON format, it needs to further transform to JSON.
base_url = "http://ip-api.com/json/{}?fields=status,country,region,regionName,city,isp,org,as,query"

# Functions

# Read Juniper Traceroute File and return a list of hop ips


def read_juniper_traceroute_file(file):

    reg = compile(
        r"\d{1,2}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]|\d{1,2}\s\*\s\*\s\*")

    # find matching pattern for hop and IPs
    matches = [reg.findall(line) for line in open(file)]

    # Filter out empty entries ([]) and unpack each hop (match) as a string (match[0])
    matches = [match[0] for match in matches if match != []]

    return [hop.split(' ')[1] for hop in matches]


# Check if each hop ip is private or *


def check_invalid_ip(ip):
    # Check if IPv4 address is private
    if ip == "*":
        return False
    elif IPv4Address(ip).is_private:
        return False
    else:
        return True

# check each hop ip info


def check_ip_info(traceroute_hops):

    hop_count = 1
    hop_info_list = []
    for hop_ip in traceroute_hops:
        if check_invalid_ip(hop_ip):
            try:
                url = base_url.format(hop_ip)
                response = requests.get(url)

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                print(
                    'HTTP error occurred: {http_err} on hop #{}'.format(hop_count))
            except Exception as err:
                print(
                    'Other error occurred: {err} on hop #{}'.format(hop_count))
            else:
                result = response.json()
                IP_Address = result['query']
                Country = result['country']
                ASN = result['as']
                hop_info_list.append([hop_count, IP_Address, Country, ASN])
                hop_count += 1
        else:
            hop_info_list.append(
                [hop_count, hop_ip, "N/A", "N/A (Non-Public IP)"])
            hop_count += 1
    return hop_info_list

# Print Result


def print_result(hop_info_list):
    # Output Display Configuration
    PTable = PrettyTable()
    PTable.field_names = ["Hop", "IP Address",
                          "Country", "AS Number - Telco Info"]
    PTable.align["Hop"] = 'm'
    PTable.align["IP Address"] = 'l'
    PTable.align["Country"] = 'm'
    PTable.align["AS Number - Telco Info"] = 'l'

    for hop_info in hop_info_list:
        PTable.add_row(hop_info)
    print(PTable)


def main():
    traceroute_hops = read_juniper_traceroute_file(traceroute_file)
    hop_info_list = check_ip_info(traceroute_hops)
    print_result(hop_info_list)


if __name__ == "__main__":
    main()
