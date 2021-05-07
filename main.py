import sys
import chromedriver_binary

from links import read_list_of_links, gen_dict_of_links
from mhtmls import gen_mhtmls, gen_only_home_mhtmls
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def print_finished():
    print("\n** Finished **\n")


def get_webdriver_options():
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    return options


def main():
    if len(sys.argv) > 1:
        # Read in URLS from links files.
        list_of_links = read_list_of_links(links_path='links.txt')
        # Generate a dictionary of links, and write TXT files to list_of_links dir
        dict_of_links, failed_links = gen_dict_of_links(list_of_links, output_dir_name="list_of_links")
        last_arg = sys.argv[len(sys.argv) - 1]
        # Start-up a Google Chrome browser to be controlled by selenium.webdriver
        driver = webdriver.Chrome(executable_path=chromedriver_binary.chromedriver_filename,
                                  options=get_webdriver_options())
        if last_arg == "simple":
            # Run 'simple' version of Python 3 program
            gen_only_home_mhtmls(driver, list_of_links, failed_links, output_dir_name="htmls")
        elif last_arg == "all":
            # Run 'all' version of Python 3 program
            gen_mhtmls(driver, list_of_links, dict_of_links, failed_links, output_dir_name="mhtmls")
        print_finished()
    else:
        print("ERROR: No argument provided. Please provide one of the following options:\n" +
              "simple - to get list_of_links and mhtmls of only URLs in links.txt file\n" +
              "all - to get list_of_links and mhtmls of URLs in links.txt file and URLs found on each webpage" +
              "(e.g. $ python3 main.py simple)")
        exit(1)


if __name__ == '__main__':
    main()
