from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag: str, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    # if we find a full url place it in my file else convert it in full url
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass

# finder = LinkFinder()
# finder.feed('<html><head><title>Test</title></head>'
# '<body><h1>Parse me</h1></body></html>')