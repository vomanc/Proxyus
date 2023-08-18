""" Site and google search """
from random import choice
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector, ProxyConnectionError
from extension import standard_links
from crawler import MyBeautifulSoup


class MyUserAgents:
    """ Generation headers """
    __slots__ = ('common_fields',)

    def __init__(self):
        """ Generation of common fields """
        win_nt = "(Windows NT 10.0; "
        ubuntu = "(X11; Ubuntu; Linux x86_64; "
        chrome = "Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
        user_agents = (
            f"{win_nt}rv:115.0) Gecko/20100101 Firefox/115.0",
            f"{win_nt}rv:116.0) Gecko/20100101 Firefox/116.0",
            f"{win_nt}rv:107.0) Gecko/20100101 Firefox/107.0",
            f"{win_nt}rv:108.0) Gecko/20100101 Firefox/108.0",
            f"{win_nt}rv:109.0) Gecko/20100101 Firefox/109.0",
            f"{ubuntu}rv:115.0) Gecko/20100101 Firefox/115.0",
            f"{ubuntu}rv:116.0) Gecko/20100101 Firefox/116.0",
            f"{ubuntu}rv:112.0) Gecko/20100101 Firefox/112.0",
            f"{ubuntu}rv:114.0) Gecko/20100101 Firefox/114.0",
            f"{ubuntu}rv:109.0) Gecko/20100101 Firefox/109.0",
            f"{win_nt}{chrome}116 Safari/537.36",
            f"{win_nt}{chrome}111 Safari/537.36",
            f"{win_nt}{chrome}112 Safari/537.36",
            f"{win_nt}{chrome}113 Safari/537.36",
        )
        other = 'xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        self.common_fields = {
            "User-Agent": f'Mozilla/5.0 {choice(user_agents)}',
            "Accept": f"text/html,application/{other}",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1"
        }

    async def headers_brave(self):
        """ Headers for brave searcher """
        headers = {
            "Host": "search.brave.com",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://search.brave.com/search?q=free+proxy+list&source=web",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        headers.update(self.common_fields)
        return headers

    async def headers_standard(self, url):
        """ Headers for other sites """
        headers = {
            "Host": url.split('://')[-1].split('/')[0],
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "",
            "Cookie": "",
            "Sec-Fetch-User": "?1",
            "TE": "trailers"
        }
        headers.update(self.common_fields)
        return headers


class SearchProxies(MyUserAgents, MyBeautifulSoup):
    """ Main function for proxy search """
    __slots__ = ('tor_proxy', 'deep_count', 'proxy_lists')

    def __init__(self, *args):
        """ Receives two arguments <args.d, args.tor>.
         define is using a tor proxy us & scrapi method:
            search deep and standard links """
        super().__init__()
        if args[1]:
            try:
                self.tor_proxy = ProxyConnector.from_url('socks5://127.0.0.1:9050')
                print('[+] Tor Network is used !')
            except ProxyConnectionError:
                print('[!] Tor connection error')
        else:
            self.tor_proxy = None
        self.deep_count = args[0]
        self.proxy_lists = set()

    async def run_parser(self):
        """ Defines method scraping """
        if self.deep_count is None:
            async with aiohttp.ClientSession(connector=self.tor_proxy) as session:
                await self.tasks_runer(session, standard_links)
        if self.deep_count and self.deep_count in {1, 2}:
            # Deep search mode
            await self.deep_mode()
        return False

    async def get_site(self, session, url):
        """ Goes to the scraping site """
        try:
            async with session.get(
                    url, headers=await self.headers_standard(url), timeout=30, allow_redirects=True
            ) as response:
                if response.status == 200:
                    response = await response.text()
                    proxies = await self.page_results(response)
                    self.proxy_lists.update(proxies)
        except (
            UnicodeDecodeError,
            asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ServerDisconnectedError):
            print('[!] Bad Internet connection')


    async def deep_mode(self):
        """ Define deep mode """
        query = ('source=web',)
        if self.deep_count == 2:
            query = [*query, *[f'&offset={count}&spellcheck=0' for count in range(1, 5)]]

        await self.searching_sites(query)

    async def searching_sites(self, query):
        """ Performs a search in Google, returns the url of the address """
        async with aiohttp.ClientSession(connector=self.tor_proxy) as session:
            for url in query:
                url = f'https://search.brave.com/search?q=free proxy list&{url}'

                async with session.get(
                        url, headers=await self.headers_brave(), timeout=30, allow_redirects=True
                        ) as response:

                    if response.status == 200:
                        response = await response.text()
                        links = await self.get_links(response)
                        await self.tasks_runer(session, links)

    async def tasks_runer(self, session, links):
        """ Created and run tasks for requests site """
        tasks = []
        loop = asyncio.get_event_loop()
        for link in links:
            tasks.append(loop.create_task(self.get_site(session, link)))
        await asyncio.gather(*tasks)
