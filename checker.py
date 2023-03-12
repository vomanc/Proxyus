# To check and determine the proxy country
from concurrent.futures import ThreadPoolExecutor
import requests
from extension import IPINFO_TOKEN


def request(proxy):
    # Checking proxy addr
    headers = {
        'Accept': 'application/json',
        'Connection': 'close'
    }
    if IPINFO_TOKEN is not None:
        token = {'Authorization': f'Bearer {IPINFO_TOKEN}'}
        headers.update(token)
    req = requests.get('https://ipinfo.io', headers=headers, proxies=proxy, timeout=10)
    if req.status_code == 200:
        return ['OK', req.json()['country']]
    if req.status_code == 429:
        return ['OK', 'Limit']
    return False


def check_response(proxy):
    # Sends requests in turn to determine the type of proxy: http, socks4, socks5
    type_proxy = [
        {'http': f'{proxy}', 'https': f'{proxy}'},
        {'http': f'socks4://{proxy}', 'https': f'socks4://{proxy}'},
        {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
    ]
    for i in type_proxy:
        try:
            type_ip = i['http'].split('://')
        except ValueError:
            type_ip = ['http', i['http']]
        if 'socks' not in type_ip[0]:
            type_ip.append('http')
            type_ip.reverse()
        try:
            response = request(i)
            if response is False:
                continue
            return request(i) + type_ip
        except (
                requests.exceptions.ProxyError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout):
            continue
    return False


def checker_results(proxy_list):
    # Main function launching in multi-threaded mode
    pool = ThreadPoolExecutor(max_workers=30)
    for proxy_res in pool.map(check_response, proxy_list):
        if proxy_res is not False:
            print(proxy_res)
