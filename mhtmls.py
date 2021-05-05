import os
import re
from manage_dir import prepare_dir


def save_webpage_from_URL(link, output_dir_name):
    # TODO: Replace logic to actually produce MHTML archive
    save_dir = os.path.join(os.getcwd(), output_dir_name)
    formatted_link = str("<" + link.replace("://", "_").replace("/", "_") + ">")
    full_file_path = save_dir + "/" + formatted_link + ".txt"
    file = open(full_file_path, mode='w')
    file.write("Test")
    file.close()
    print("** Saved webpage for the following URL: {} in the location: {} **".format(link, output_dir_name))


def gen_mhtmls(list_of_links, dict_of_links, failed_links, output_dir_name):
    print("\n** Generating MHTMLs using list of URLs and dictionary of URLs **\n")
    prepare_dir(output_dir_name)
    for link in list_of_links:
        if link not in failed_links:
            print("\n** Generating MHTMLs for: {} **\n".format(link))
            save_webpage_from_URL(link, output_dir_name)
            url_domain = re.search('https?://([A-Za-z_0-9.-]+).*', link).group(1)
            path_for_link_mhtml = os.path.join(os.getcwd(), output_dir_name, "<" + url_domain + ">")
            if not (os.path.isdir(path_for_link_mhtml)):
                print("\n** Making directory: {} **\n".format(path_for_link_mhtml))
                os.mkdir(path_for_link_mhtml)
            for lnk in dict_of_links[link]:
                save_webpage_from_URL(link=lnk, output_dir_name=path_for_link_mhtml)
    print()


def gen_only_home_mhtmls(list_of_links, failed_links, output_dir_name):
    print("\n** Generating home MTHMLs using list of URLs **\n")
    prepare_dir(output_dir_name)
    for link in list_of_links:
        if link not in failed_links:
            print("\n** Generating MHTML for: {} **\n".format(link))
            save_webpage_from_URL(link, output_dir_name)
    print()
