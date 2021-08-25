#!/usr/bin/python3
# grep --color=auto -ER '\$_POST|\$_GET|\$_REQUEST' /var/www/html/blog/ (pipe output in)
# This script generates URLs to scan from source code 

import sys
import re
import argparse
import ipaddress
from lib.fileOp import FileOp
try:
	from ipaddress import ip_address
except ImportError:
	from ipaddr import IPAddress as ip_address

#Get list of Ips from a range
def findIPs(start, end):
    start = ip_address(start)
    end = ip_address(end)
    result = []
    while start <= end:
        result.append(str(start))
        start += 1
    return result

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-v', '--value', type=str, default='discobiscuits',
                        help='Specify a parameter value to use')
    parse.add_argument('-u', '--url', type=str, default='https://example.com',
                        help='Specify a base URL to use')
    parse.add_argument('-d', '--dir', type=str, default=None,
                        help='Specify the web directory')
    parse.add_argument('-a', '--all', action='store_true', default=False,
                        help='Use all params on all URLS')
    parse.add_argument('-p', '--onlypath', action='store_true', default=False,
                        help='Get path URLS without params')
    parse.add_argument('-s', '--smart', action='store_true', default=False,
                        help='Only generate URLS with params in the relative files')
    parse.add_argument('-std', '--standin', action='store_true', default=False,
						help='Use Standard input to parse GREPS!')
    parse.add_argument('-ip', '--fromIP', default=None, nargs='+',
						help='Translate network range into urls')
    parse.add_argument('-rip','--space', default=None, nargs='+',
                        help='Print all IPs between two [ip-a]...[ip-b]')
    parse.add_argument('-i', '--IPList', type=str, default=None,
                        help='Translate IPs from list into URLS')
        
    args = parse.parse_args()
    url_set = set()
    params = set()
    param_val = "="+args.value
    lines = []
     
    if len(sys.argv) <= 1:
           parse.print_help()
    
    if (args.standin):
        for line in sys.stdin:
            line = sys.stdin.readline()
            path = line.split(':')[0]
            strip_path = path.strip()
            if len(strip_path) > 0:
                url_set.add(strip_path)
            pattern = r'\'([A-Za-z0-9_\./\\-]*)\''
            pattern2 = r'"([A-Za-z0-9_\./\\-]*)"'
            words = re.findall(pattern,line)
            words2 = re.findall(pattern2, line)
            for i in words:
                params.add(i)
            for i in words2:
                params.add(i)
            lines.append(line)

    if args.space != None:
        try:
            ip_a = args.space[0]
            ip_b = args.space[1]
        except:
            print('provide 2 Ips (-rip 127.0.0.1 127.0.0.10)')
        data = findIPs(ip_a, ip_b)
        for i in data:
            print(i)

    elif args.all != False:
        if args.dir != None:
            new_url_set = set()
            for i in url_set:
                new_url = i.split(args.dir)[1]
                new_url_set.add(new_url)
            url_set = new_url_set

            for path in url_set:
                for param in params:
                    print(args.url+path+'?'+param+param_val)

    elif args.onlypath != False:
        if args.dir != None:
            new_url_set = set()
            for i in url_set:
                new_url = i.split(args.dir)[1]
                new_url_set.add(new_url)
            url_set = new_url_set

            for path in url_set:
                print(args.url+path)

    elif args.smart != False:
        smart_url_set = set()
        if args.dir != None:
            for line in lines:
                path = line.split(':')[0]
                strip_path = path.strip()
                if len(strip_path) > 0:
                    new_url = strip_path.split(args.dir)[1]
                    pattern = r'\'([A-Za-z0-9_\./\\-]*)\''
                    pattern2 = r'"([A-Za-z0-9_\./\\-]*)"'
                    words = re.findall(pattern,line)
                    words2 = re.findall(pattern2, line)
                    for param in words:
                        smart_url_set.add(args.url+new_url+"?"+param+param_val)
                    for param in words2:
                        smart_url_set.add(args.url+new_url+"?"+param+param_val)
        for i in smart_url_set:
            print(i)


    elif args.fromIP != None:
        iplist = []
        for i in args.fromIP:
            if '/' in i:
                try:
                    ip = ipaddress.ip_network(i,strict=False)
                    for host in ip.hosts():
                        iplist.append(str(host))
                except Exception as e:
                    print('Error: Bad IP network provided (127.0.0.1/24)')
                    print(e)
            elif '-' in i:
                try:
                    ipaddr = i.split('.')
                    iprange = ipaddr.pop()
                    ipaddr = '.'.join(ipaddr)
                    first = int(iprange.split('-').pop(0))
                    second = int(iprange.split('-').pop())+1
                    for x in range(first, second):
                        iplist.append(ipaddr+'.'+str(x))
                except Exception as e:
                    print(e)
                    print('Error: Bad IP range provided (127.0.0.20-30)')
            else:
                try:
                    ip = str(ipaddress.IPv4Address(i))
                    iplist.append(ip)
                except Exception as e:
                    print(e)
                    print('Error: Bad IP address provided (127.0.0.1)')
        for i in iplist:
            print('http://'+i+'/')
            print('https://'+i+'/')

    elif args.IPList != None:
        iplist = FileOp(args.IPList).reader()
        for i in iplist:
            print('http://'+i+'/')
            print('https://'+i+'/')

    else:
        print('Specify -a or -p')


