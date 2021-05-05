import os
import re
from bs4 import BeautifulSoup
from manage_dir import prepare_dir
from urllib.request import Request, urlopen


def read_list_of_links(links_path):
    print("\n** Reading in URLs from: {} **\n".format(links_path))
    file1 = open(links_path, 'r')
    links = file1.readlines()
    list_of_links = list()
    for link in links:
        # Use '#' at the beginning of a line for line comment in links.txt
        if re.search('^#', link) is None:
            list_of_links.append(link.rstrip("\n"))
    return list_of_links


def gen_dict_of_links(list_of_links, output_dir_name):
    print("\n** Generating dictionary of URLs from list of URLs **\n")
    dict_of_links = dict()
    failed_links = set()
    total_links = 0
    for x in list_of_links:
        try:
            url_proto_domain = re.search('(http[s]?://)?([^/\\s]+)', x).group(0)
            req = Request(x)
            html_page = urlopen(req)
            links = set()
            for link in get_soup(url_proto_domain, html_page):
                url_path = str(link.get('href'))
                if re.search('^(http|https)://', url_path) is not None:
                    links.add(url_path)
                if re.search('^/', url_path) is not None:
                    links.add(url_proto_domain + url_path)
            print("URL: {}".format(x))
            print("\n -- Number of links found: {}\n".format(len(links)))
            dict_of_links[x] = links
            total_links += len(links)
        except Exception as e:
            print("\n** Exception ** : {0} - {1}\n".format(x, e))
            failed_links.add(x)
    print("\n** Total number of links ** : {}\n".format(total_links))
    output_dict_of_links_to_txt(dict_of_links, output_dir_name)
    return dict_of_links, failed_links


def output_dict_of_links_to_txt(dict_of_links, output_dir_name):
    print("\n** Generating TXTs using dictionary of URLs **\n")
    prepare_dir(output_dir_name)
    for x in dict_of_links:
        formatted_list = '\n'.join('{}: {}'.format(*k) for k in enumerate(dict_of_links[x]))
        list_of_strings = '{0} :\n\n{1}\n'.format(x, formatted_list)
        file_path = os.path.join(os.getcwd(), output_dir_name,
                                 str("<" + str(x).replace("://", "_").replace("/", "_") + ">.txt"))
        with open(file_path, 'w') as my_file:
            print("\n** Generating TXT for: {} **\n".format(x))
            my_file.write(list_of_strings)
    print()


# TODO: Make it so site container info can be specified in links.txt along with URL for crawling
def get_soup(url_proto_domain, html_page):
    if url_proto_domain == 'https://www.bbc.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("div", {"id": "site-container"}).findAll('a')
    elif url_proto_domain == 'https://www.kentonline.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("div", {"class": "MainSite"}).findAll('a')
    elif url_proto_domain == 'https://www.cambridgeindependent.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("div", {"id": "EWrap"}).findAll('a')
    elif url_proto_domain == 'https://www.bristolpost.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("main").findAll('a')
    elif url_proto_domain == 'https://www.nottinghampost.com':
        return BeautifulSoup(html_page, "html.parser").find("main").findAll('a')
    elif url_proto_domain == 'https://www.thestar.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("div", {"id": "frameInner"}).findAll('a')
    elif url_proto_domain == 'https://www.miltonkeynes.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("div", {"id": "frameInner"}).findAll('a')
    elif url_proto_domain == 'http://altrincham.today':
        return BeautifulSoup(html_page, "html.parser").find("main").findAll('a')
    elif url_proto_domain == 'https://onthewight.com':
        return BeautifulSoup(html_page, "html.parser").find("div", {"id": "content"}).findAll('a')
    elif url_proto_domain == 'https://thelincolnite.co.uk':
        return BeautifulSoup(html_page, "html.parser").find("main").findAll('a')
    elif url_proto_domain == 'https://theisleofthanetnews.com':
        return BeautifulSoup(html_page, "html.parser").find("div", {"class": "mh-wrapper"}).findAll('a')
    elif url_proto_domain == 'https://westbridgfordwire.com':
        return BeautifulSoup(html_page, "html.parser").find("div", {"class": "td-main-content-wrap"}).findAll('a')
    elif url_proto_domain == 'https://www.yourthurrock.com':
        return BeautifulSoup(html_page, "html.parser").find("div", {"class", "container"}).findAll("a")
    else:
        return BeautifulSoup(html_page, "html.parser").findAll('a')
