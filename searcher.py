# Site and google search
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector, ProxyConnectionError
import extension
import crawler


headers_1, headers_2 = extension.my_headers()


async def request(session, url):
    # Makes a request to get links from a search engine
    async with session.get(url, headers=headers_1, timeout=30, allow_redirects=True) as response:
        if response.status == 200:
            raw_links = await response.text()
            craw = crawler.MyBeautifulSoup(raw_links)
            response = await craw.get_links()
        else:
            response = '0'
        return response


async def searching_site(deep_mode, tor_proxy=None):
    # Performs a search in Google, returns the url of the address
    url = 'https://www.google.com/search?q=free+proxy+list'
    async with aiohttp.ClientSession(connector=tor_proxy) as session:
        sites_for_proxy = await request(session, url)
        if deep_mode == 2:
            for page in range(10, 60, 10):
                url = f'{url}&start={page}&sa=N'
                site_proxy = await request(session, url)
                sites_for_proxy += site_proxy
                if site_proxy == '0':
                    return False
    return set(sites_for_proxy)


async def collector(session, url, proxy_lists):
    # makes a request to collect the proxy
    async with session.get(url, headers=headers_2, timeout=30, allow_redirects=True) as response:
        if response.status == 200:
            response = await response.text()
            craw = crawler.MyBeautifulSoup(response)
            proxy_lists += await craw.page_results()


async def standard_mode(tor_proxy, links_list):
    # Follows certain links to collect proxy addresses
    async with aiohttp.ClientSession(connector=tor_proxy) as session:
        tasks = []
        loop = asyncio.get_event_loop()
        proxy_lists = []
        for url in links_list:
            tasks.append(loop.create_task(collector(session, url, proxy_lists)))
        await asyncio.gather(*tasks)
    return set(proxy_lists)


async def search(args):
    # Main function for proxy search
    if args.tor is True:
        try:
            tor_proxy = ProxyConnector.from_url('socks5://127.0.0.1:9050')
            print('[+] Tor Network is used !')
        except ProxyConnectionError:
            return '[!] Tor connection error'
    else:
        tor_proxy = None

    if args.d is None:
        return await standard_mode(tor_proxy, extension.standard_links)
    if args.d in (1, 2):
        # Deep search mode
        found_links = await searching_site(args.d, tor_proxy)
        if found_links is not False:
            return await standard_mode(tor_proxy, found_links)
        return '[*] Perhaps the search engine is blocking your address !'
    print('[!] -d 1 or 2')
    return False
