#!/usr/bin/env python3

from urllib import request
import urllib
import json, sys, time, re

if len(sys.argv) != 3 and not (len(sys.argv) == 2 and sys.argv[1] == '--logout') :
    print('BJUT network - Gateway Auto Login v0.1')
    print('This script will auto login bjut\'s wired network both ipv4 and ipv6\n')
    print('Usage: \t' + sys.argv[0] + ' <user> <password>')
    print('\t' + sys.argv[0] + ' --logout')
    sys.exit()

LGN_LOGIN_URL = 'https://lgn.bjut.edu.cn'
LGN_LOGOUT_URL = 'https://lgn.bjut.edu.cn/F.htm'
LGN6_JUMPING_URL = 'https://lgn6.bjut.edu.cn/V6?https://lgn.bjut.edu.cn'

# logout
if len(sys.argv) == 2 and sys.argv[1] == '--logout':
    req = request.Request(LGN_LOGOUT_URL)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0')
    f = request.urlopen(req)
    data = f.read().decode('gb2312')
    if data.find('Msg=14') != -1:
        print('Logout successed')
    else:
        print('Logout failed, have you already logged out?')

    sys.exit()

# Get lgn login page's content
req = request.Request(LGN_LOGIN_URL)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0')
f = request.urlopen(req)
data = f.read().decode('gb2312')

# Get ipv4_server_ip from login page
result = re.match(r'.*v4serip=\'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\'', data, re.DOTALL)
if not result:
    print('Error: re.match get ipv4_server_ip failed, have you already logged in?')
    print('Please use the following command to logout:')
    print('\t', sys.argv[0], '--logout')
    sys.exit(1)

ipv4_server_ip = result.groups()[0]
print('ipv4_server_ip =', ipv4_server_ip)


# POST data to lgn6 jumping page
req = request.Request(LGN6_JUMPING_URL)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0')
post_data = {'DDDDD': sys.argv[1], 'upass': sys.argv[2], 'v46s': '0', 'v6ip': '', 'f4serip': ipv4_server_ip, '0MKKey': ''}
post_data = urllib.parse.urlencode(post_data).encode()
f = request.urlopen(req, post_data)
data = f.read().decode('gb2312')

# Get ipv6_server_ip from lgn6 jumping page
result = re.match(r'.*name=\'v6ip\' value=\'(.+)\'', data, re.DOTALL)
if not result:
    print('Error: re.match get ipv6_server_ip failed, abort')
    sys.exit(1)

ipv6_server_ip = result.groups()[0]
print('ipv6_server_ip =', ipv6_server_ip)


# POST data to final lgn login page
req = request.Request(LGN_LOGIN_URL)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0')
post_data = {'DDDDD': sys.argv[1], 'upass': sys.argv[2], '0MKKey': 'Login', 'v6ip': ipv6_server_ip}
post_data = urllib.parse.urlencode(post_data).encode()
f = request.urlopen(req, post_data)
data = f.read().decode('gb2312')

if data.find('successfully logged') != -1:
    print('Login successed')
elif data.find('Msg=01') != -1:
    print('Error: wrong password')
    sys.exit(1)
else:
    print('--- final lgn login page content dump - START')
    print(data)
    print('--- final lgn login page content dump - END')
    print('\nError: unknown error, page content dumped')
    sys.exit(1)
