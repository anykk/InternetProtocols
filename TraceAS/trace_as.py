import argparse
import ipwhois
import prettytable
import re
import shlex
import sys
import subprocess
from warnings import filterwarnings

filterwarnings('ignore')


IP_PATTERN = re.compile('\d+\.\d+\.\d+\.\d+')


def parse_args():
    parser = argparse.ArgumentParser(description='util for AS trace and get info about it')
    parser.add_argument('domain', type=str, help='domain to trace')
    return parser.parse_args()


def trace_to(domain):
    try:
        return subprocess.check_output(shlex.split(f'tracert -w 350 {domain}')).decode('cp866')
    except subprocess.CalledProcessError:
        sys.exit('Failed to trace.')


def get_addrs_from(trace_output):
    return tuple(enumerate(re.findall(IP_PATTERN, trace_output)[1:], start=1))


def get_info_by(ip):
    try:
        obj = ipwhois.IPWhois(ip[1])
        info = obj.lookup_whois()
        asn = info["asn"].split()[0]
        country = info['nets'][0]['country']
        provider = info['nets'][0]['description']
    except ipwhois.exceptions.IPDefinedError:
        asn = 'NA'
        country = 'Unknown'
        provider = 'None'
    return ip[0], ip[1], asn, country, provider


if __name__ == '__main__':
    args = parse_args()
    print(f'Trace to {args.domain}...')
    table = prettytable.PrettyTable(['№', 'IP', 'AS', 'COUNTRY', 'PROVIDER'])
    for element in map(get_info_by, get_addrs_from(trace_to(args.domain))):
        table.add_row(element)
    print(table)
