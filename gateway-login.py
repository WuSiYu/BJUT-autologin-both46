#!/usr/bin/env python3

# === Settings BEGIN ===
# Change it according to your school's network environment
LGN_LOGIN_URL = 'https://lgn.bjut.edu.cn/'
LGN_LOGOUT_URL = 'https://lgn.bjut.edu.cn/F.htm'
LGN6_JUMPING_URL = 'https://lgn6.bjut.edu.cn/V6?https://lgn.bjut.edu.cn'

SIMULATED_UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
# === Settings END

from urllib import request
import urllib, sys, re


# Logout current account
def gateway_logout():
    req = request.Request(LGN_LOGOUT_URL)
    req.add_header('User-Agent', SIMULATED_UA)
    f = request.urlopen(req)
    data = f.read().decode('gb2312')
    if data.find('Msg=14') != -1:
        print('Logout successed')
    else:
        print('Logout failed, have you already logged out?')


# Get account status
def gateway_account_status():
    req = request.Request(LGN_LOGIN_URL)
    req.add_header('User-Agent', SIMULATED_UA)
    f = request.urlopen(req)
    data = f.read().decode('gb2312')
    # print(data)
    result = re.match(r'.*time=\'(.+?)\s*\';', data, re.DOTALL)
    if not result:
        print('Error: re.match get account info failed, abort')
        sys.exit(1)
    used_time = int(result.groups()[0])
    used_traffic = int(re.match(r'.*flow=\'(.+?)\s*\';', data, re.DOTALL).groups()[0]) / 1024
    account_ballance = int(re.match(r'.*fee=\'(.+?)\s*\';', data, re.DOTALL).groups()[0]) / 10000

    print("=== Account status =========================================")
    print(" Connnected time:       %d mins (%d hours and %d mins)" % (used_time, used_time // 60, used_time % 60) )
    print(" Traffic used:          %.2f GiB (%d GiB and %d MiB)" % (used_traffic / 1024, used_traffic // 1024, used_traffic % 1024) )
    print(" Account ballance:      %d Yuan" % account_ballance)
    print("=============================================================")


# Login the bjut gateway
def gateway_login(username, password):
    # Get lgn login page's content
    req = request.Request(LGN_LOGIN_URL)
    req.add_header('User-Agent', SIMULATED_UA)
    f = request.urlopen(req)
    data = f.read().decode('gb2312')

    # Get ipv4_server_ip from login page
    result = re.match(r'.*v4serip=\'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\'', data, re.DOTALL)
    if not result:
        if data.find('DispTFM') != -1:
            print('Error: re.match get ipv4_server_ip failed, have you already logged in?\n'
                  'Please use the following command to logout if you want:\n'
                  '\t', sys.argv[0], '--logout\n')
            print('Tring to get current logged in account status ...')
            gateway_account_status()
        else:
            print('Error: re.match get ipv4_server_ip failed')
        return -1

    ipv4_server_ip = result.groups()[0]
    print('ipv4_server_ip =', ipv4_server_ip)

    # POST data to lgn6 jumping page
    req = request.Request(LGN6_JUMPING_URL)
    req.add_header('User-Agent', SIMULATED_UA)
    post_data = {'DDDDD': username, 'upass': password, 'v46s': '0', 'v6ip': '', 'f4serip': ipv4_server_ip, '0MKKey': ''}
    post_data = urllib.parse.urlencode(post_data).encode()
    f = request.urlopen(req, post_data)
    data = f.read().decode('gb2312')

    # Get ipv6_server_ip from lgn6 jumping page
    result = re.match(r'.*name=\'v6ip\' value=\'(.+?)\'', data, re.DOTALL)
    if not result:
        print('Error: re.match get ipv6_server_ip failed, abort')
        sys.exit(1)

    ipv6_server_ip = result.groups()[0]
    print('ipv6_server_ip =', ipv6_server_ip)

    # POST data to final lgn login page
    req = request.Request(LGN_LOGIN_URL)
    req.add_header('User-Agent', SIMULATED_UA)
    post_data = {'DDDDD': username, 'upass': password, '0MKKey': 'Login', 'v6ip': ipv6_server_ip}
    post_data = urllib.parse.urlencode(post_data).encode()
    f = request.urlopen(req, post_data)
    data = f.read().decode('gb2312')

    if data.find('successfully logged') != -1:
        print('Login successed, Welcome to the Internet!\n')
        gateway_account_status()
    elif data.find('Msg=01') != -1:
        print('Error: wrong password')
        return 1
    elif data.find('Msg=04') != -1:
        print('Error: server says: Insufficient account balance')
        return 4
    else:
        print('--- final LGN login page content dump - START')
        print(data)
        print('--- final LGN login page content dump - END')
        print('\nError: unknown error, page content dumped')
        return -2


def main():

    if len(sys.argv) == 3:
        gateway_login(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] in ('-l', '--logout'):
        gateway_logout()
    elif len(sys.argv) == 2 and sys.argv[1] in ('-s', '--status'):
        gateway_account_status()
    else:
        print('BJUT network - Gateway Auto Login v0.2\n'
              'This script can log in to BJUT\'s wired network both ipv4 and ipv6\n'
              'It may also works in other school\'s which using the same system\n\n'
              'Usage: \t' + sys.argv[0] + ' <user> <password>\n'
              '\t' + sys.argv[0] + ' -l, --logout\n'
              '\t' + sys.argv[0] + ' -s, --status\n')
        sys.exit()


if __name__ == '__main__':
    main()
