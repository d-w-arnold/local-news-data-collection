import os
import re
from bs4 import BeautifulSoup
from manage_dir import prepare_dir
from urllib.request import Request, urlopen


def read_list_of_links(path):
    print("** Reading in URLs from: {} **".format(path))
    file1 = open(path, 'r')
    links = file1.readlines()
    tmp = list()
    for x in links:
        # Use '#' at the beginning of a line for line comment in links.txt
        if re.search('^#', x) is None:
            tmp.append(x.rstrip("\n"))
    return tmp


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


def gen_dict_of_links(links, output_dir_name):
    print("** Generating dictionary of URLs from list of URLs **")
    dict_of_links = dict()
    total_links = 0
    for x in links:
        try:
            url_proto_domain = re.search('(http[s]?://)?([^/\\s]+)', x).group(0)
            req = Request(x)
            html_page = urlopen(req)
            links = []
            for link in get_soup(url_proto_domain, html_page):
                url_path = str(link.get('href'))
                if re.search('^(http|https)://', url_path) is not None:
                    links.append(url_path)
                if re.search('^/', url_path) is not None:
                    links.append(url_proto_domain + url_path)
            print("URL: {}".format(x))
            print(" -- Number of links found: {}".format(len(links)))
            dict_of_links[x] = links
            total_links += len(links)
        except Exception as e:
            print("** Exception ** : {0} - {1}".format(x, e))
    print()
    print("** Total number of links ** : {}".format(total_links))
    print()
    output_dict_of_links_to_txt(dict_of_links, output_dir_name)
    return dict_of_links


def output_dict_of_links_to_txt(dict_of_links, output_dir_name):
    print("** Generating TXTs using dictionary of URLs **")
    prepare_dir(output_dir_name)
    for key in dict_of_links:
        formatted_list = '\n'.join('{}: {}'.format(*k) for k in enumerate(dict_of_links[key]))
        list_of_strings = '{0} :\n\n{1}\n'.format(key, formatted_list)
        file_path = os.path.join(os.getcwd(), output_dir_name,
                                 str("<" + str(key).replace("://", "_").replace("/", "_") + ">.txt"))
        with open(file_path, 'w') as my_file:
            print("** Generating TXT for: {} **".format(key))
            my_file.write(list_of_strings)
    print()
