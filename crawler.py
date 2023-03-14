""" Search IP, and URL """
import re
from bs4 import BeautifulSoup


class MyBeautifulSoup:
    """ Crawler for any page """

    def __init__(self, html_doc):
        # Auto crawler for any page
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    async def page_results(self):
        """ Search IP """
        all_proxy = re.findall(r"[0-9]+(?:\.[0-9]+){3}:\d*", str(self.soup))
        return all_proxy

    async def get_links(self):
        """ Collects links from search """
        links = []
        for url in self.soup.findAll('a'):
            url = url.get('href')
            if url is None:
                continue
            if 'google' not in url and 'wikipedia.org' not in url and 'gstatic' not in url \
                    and 'https://' in url:
                links.append(url)
        return links
