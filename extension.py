''' Banner, links for free proxy, user-agents used in the script '''
from random import choice

IPINFO_TOKEN = None
BANNER = 'PROXYUS, version 3.0\n' + '_'*20

user_agent_list = [
    "(Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0",
    "(Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0",
    "(Windows NT 10.0; rv:107.0) Gecko/20100101 Firefox/107.0",
    "(Windows NT 10.0; rv:108.0) Gecko/20100101 Firefox/108.0",
    "(Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0",
    "(X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "(X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "(X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "(X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "(X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106 Safari/537.36",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108 Safari/537.36",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109 Safari/537.36",
    ]


def my_headers():
    ''' Generation headers '''
    user_agent = "Mozilla/5.0 " + choice(user_agent_list)
    acpt = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers_1 = {
        "Host": "www.google.com",
        "User-Agent": user_agent,
        "Accept": acpt,
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Cookie": "",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "TE": "trailers"
        }

    headers_2 = {
        "User-Agent": user_agent,
        'Accept': '*/*',
        'Accept-Encoding': 'deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        }

    return headers_1, headers_2


standard_links = [
    "https://premproxy.com/socks-list/",
    "https://www.socks-proxy.net/",
    "https://spys.one/en/socks-proxy-list/",
    "https://www.freeproxy.world/?type=socks5",
    "https://www.proxy-list.download/SOCKS5",
    "https://www.sslproxies.org/",
    "https://hidemy.name/en/proxy-list/",
    "https://www.proxyscan.io/",
    "https://www.socks-proxy.net",
    "https://freeproxy.pro/",
    "https://free-proxy-list.net",
    "https://us-proxy.org/",
    "http://proxydb.net/?protocol=http&protocol=https&protocol=socks4&protocol=socks5&country=",
    "https://free-proxy-list.net/uk-proxy.html"
]
