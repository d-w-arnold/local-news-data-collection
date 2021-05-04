import os
import re
from manage_dir import prepare_dir
from pywebcopy import save_webpage


def save_webpage_from_URL(link, output_dir_name):
    save_path = os.path.join(os.getcwd(), output_dir_name)
    formatted_link = str("<" + link.replace("://", "_").replace("/", "_") + ">")
    kwargs = {'project_name': formatted_link}
    save_webpage(
        url=link,
        project_folder=save_path,
        **kwargs
    )
    print("** Saved webpage for the following URL: {} **".format(link))


# TODO: Solve HTTP 403 errors
def gen_mhtmls(lol, dol, output_dir_name):
    print("** Generating MHTMLs using list of URLs and dictionary of URLs **")
    prepare_dir(output_dir_name)
    for lnk in lol:
        print("** Generating MHTMLs for: {} **".format(lnk))
        save_webpage_from_URL(lnk, output_dir_name)
        url_domain = re.search('https?://([A-Za-z_0-9.-]+).*', lnk).group(1)
        path_for_lnk_mhtml = os.path.join(os.getcwd(), output_dir_name, "<" + url_domain + ">")
        if not (os.path.isdir(path_for_lnk_mhtml)):
            os.mkdir(path_for_lnk_mhtml)
            print("** Created directory: {} **".format(path_for_lnk_mhtml))
        for link in dol[lnk]:
            save_webpage_from_URL(path_for_lnk_mhtml, link)
    print()


def gen_only_home_mhtmls(lol, output_dir_name):
    print("** Generating home MTHMLs using list of URLs **")
    prepare_dir(output_dir_name)
    for lnk in lol:
        print("** Generating MHTML for: {} **".format(lnk))
        save_webpage_from_URL(lnk, output_dir_name)
    print()
