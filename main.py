import sys

from htmls import gen_htmls, gen_only_home_htmls
from links import read_list_of_links, gen_dict_of_links
from manage_webdriver import setup_webdriver


def print_finished():
    print("\n** Finished **\n")


def main():
    if len(sys.argv) > 1:
        # Read in URLS from links files.
        list_of_links = read_list_of_links(links_path='links.txt')
        # Generate a dictionary of links, and write TXT files to list_of_links dir
        dict_of_links, failed_links = gen_dict_of_links(list_of_links, output_dir_name="list_of_links")
        last_arg = sys.argv[len(sys.argv) - 1]
        # Start-up a Google Chrome browser to be controlled by selenium.webdriver
        htmls_output_dir = "htmls"
        driver = setup_webdriver(output_dir=htmls_output_dir)
        if last_arg == "simple":
            # Run 'simple' version of Python 3 program
            gen_only_home_htmls(driver, list_of_links, failed_links, output_dir_name=htmls_output_dir)
        elif last_arg == "all":
            # Run 'all' version of Python 3 program
            gen_htmls(driver, list_of_links, dict_of_links, failed_links, output_dir_name=htmls_output_dir)
        print_finished()
    else:
        print("ERROR: No argument provided. Please provide one of the following options:\n" +
              "simple - to get list_of_links and HMTL files of only URLs in links.txt file\n" +
              "all - to get list_of_links and HTML files of URLs in links.txt file and URLs found on each webpage" +
              "(e.g. $ python3 main.py simple)")
        exit(1)


if __name__ == '__main__':
    main()
