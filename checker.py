# To check and determine the proxy country
from concurrent.futures import ThreadPoolExecutor
import requests
from extension import IPINFO_TOKEN


class ProxyChecker:
    """ Multithreads status checks, determines country and proxy type """
    __slots__ = ('__headers',)

    def __init__(self):
        """ The init """
        self.__headers = {
            'Accept': 'application/json',
            'Connection': 'close'
        }
        if IPINFO_TOKEN:
            self.__headers.update({'Authorization': f'Bearer {IPINFO_TOKEN}'})

    def request(self, proxy):
        """ Checking proxy addr """
        req = requests.get('https://ipinfo.io', headers=self.__headers, proxies=proxy, timeout=10)
        if req.status_code == 200:
            return 'OK', req.json()['country']
        if req.status_code == 429:
            return 'OK', 'Limit'
        return None

    def check_response(self, proxy):
        """ Sends requests in turn to determine the type of proxy: http, socks4, socks5 """
        type_proxy = (
            {'http': f'{proxy}', 'https': f'{proxy}'},
            {'http': f'socks4://{proxy}', 'https': f'socks4://{proxy}'},
            {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
        )

        for i in type_proxy:
            try:
                if response := self.request(i):
                    return ', '.join(response), self.check_proxy_type(i), proxy
            except (
                    requests.exceptions.ProxyError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout):
                continue
        return None

    @staticmethod
    def check_proxy_type(i):
        """ Define proxy type """
        if "socks4" in i['http']:
            return 'socks4'
        if "socks5" in i['http']:
            return 'socks5'
        return 'http  '

    def results(self, proxy_list):
        """ Main function launching in multi-threaded mode """
        pool = ThreadPoolExecutor(max_workers=30)
        index, rate = 0, 100 / len(proxy_list)

        for proxy_res in pool.map(self.check_response, proxy_list):
            if proxy_res:
                print('\r', proxy_res)
            index += 1
            print('\r', round(index * rate, 2), '% executed ...', end='',)
