from os import name
from urllib.request import urlopen # module which allows to connect web-pages from python
from link_finder import LinkFinder
from initial_setup import *

class Spider:

    # Class variables so that it is shared among all the spider instances
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        # First spider has a few extra tasks- 1. Create empty project directory
        #                                     2. Create the data files- queue and crawled
        
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name,Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled: # check page_url is not already present in crawled set
            print(thread_name+' now crawling '+page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled '+ str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url)) # Add all the links on a page_url to waiting queue synchronous to all spiders
            Spider.queue.remove(page_url) # remove page_url from waiting queue once it is processed
            Spider.crawled.add(page_url)
            Spider.update_files()


# the urllib module doesn't return the result in human readable htm format instead it does it in binary

    @staticmethod
    def gather_links(page_url):
        html_string = '' # actual human readable string converted from binary
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read() 
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url,page_url)
            finder.feed(html_string)
        except:
            print('Error: Can Not Crawl Page')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            # check if url is not in waiting queue and are in crawled list so we don't crawl again
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            # check that any page my crawler crawls has same domain_name as my homepage else it might have to crawl complete internet.... 
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    # save the data from sets to actual file
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
         



