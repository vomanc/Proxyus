# Search IP, and URL from HTML
import re
from bs4 import BeautifulSoup


class MyBeautifulSoup:
    """ Crawler for any page """
    async def page_results(self, html_doc):
        """ Auto crawler for any page and search IP """
        if all_proxy := re.findall(r"[0-9]+(?:\.[0-9]+){3}:[0-9]\d*", str(html_doc)):
            return all_proxy

        soup = BeautifulSoup(html_doc, 'html.parser')
        text = soup(text=re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"))
        all_proxy = []
        for ip in text:
            _ip = re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)[0]

            for port in range(0, 5):
                try:
                    port = ip.find_next().get_text().strip()
                except AttributeError:
                    break
                if port and port.isdigit():
                    all_proxy.append(f'{_ip}:{port}')
                    break

                ip = ip.find_next()

        return all_proxy

    async def get_links(self, html_doc):
        """ Collects links from search """
        soup = BeautifulSoup(html_doc, 'html.parser')
        links = set()
        for url in soup.findAll('a'):
            url = url.get('href')
            if 'google' in url or 'wikipedia.org' in url or 'gstatic' in url \
                or 'brave.com' in url or 'youtube.com' in url:
                continue
            if 'https://' in url:
                links.add(url)
        return links
