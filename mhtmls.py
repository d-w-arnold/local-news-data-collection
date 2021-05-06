import os
import re
import pyautogui

from manage_dir import prepare_dir
from selenium.webdriver.common.keys import Keys
from time import sleep


def save_as_on_webpage(driver, formatted_link):
    # TODO: Improve this to save in specific dir and change 'Format' to 'Web page, Single File'
    # Full screen and wait
    driver.fullscreen_window()
    sleep(2)
    # Right-click webpage
    pyautogui.rightClick(x=100, y=100)
    # Navigate down right-click option to 'Save As' and wait for pop-up window
    pyautogui.press(['down', 'down', 'down', 'down', 'enter'])
    sleep(2)
    # Rename and save file to Downloads and wait
    pyautogui.typewrite(formatted_link)
    pyautogui.press('enter')
    sleep(10)


def save_webpage_from_URL(driver, link, output_dir_name):
    # TODO: Replace logic to actually produce MHTML archive, instead of HTML file
    save_dir = os.path.join(os.getcwd(), output_dir_name)
    formatted_link = link.replace("://", "_").replace("/", "_")
    # Limit filename length
    max_filename_len = 240
    if len(formatted_link) > max_filename_len:
        formatted_link = formatted_link[0:max_filename_len]
    # Set absolute path for HTML file
    full_file_path = save_dir + "/<" + formatted_link + ">.html"
    # Open tab
    # (Keys.CONTROL + 'w') on other OSs.
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    # Open webpage link and wait to load
    driver.get(link)
    sleep(1)
    # TODO: Add step to close/accept privacy/cookie settings DOM pop-ups
    # Write webpage source to HTML file
    with open(full_file_path, 'w+') as f:
        f.write(driver.page_source)
        f.close()
    # Save as webpage using pyautogui
    # save_as_on_webpage(driver, formatted_link)
    # Close the tab
    # (Keys.CONTROL + 'w') on other OSs.
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
    print("** Saved webpage for the following URL: {}\n\t\tat the path: {} **".format(link, full_file_path))


def gen_mhtmls(driver, list_of_links, dict_of_links, failed_links, output_dir_name):
    print("\n** Generating MHTMLs using list of URLs and dictionary of URLs **\n")
    prepare_dir(output_dir_name)
    for link in list_of_links:
        if link not in failed_links:
            print("\n** Generating MHTMLs for: {} **\n".format(link))
            save_webpage_from_URL(driver, link, output_dir_name)
            url_domain = re.search('https?://([A-Za-z_0-9.-]+).*', link).group(1)
            path_for_link_mhtml = os.path.join(os.getcwd(), output_dir_name, "<" + url_domain + ">")
            if not (os.path.isdir(path_for_link_mhtml)):
                print("\n** Making directory: {} **\n".format(path_for_link_mhtml))
                os.mkdir(path_for_link_mhtml)
            for lnk in dict_of_links[link]:
                save_webpage_from_URL(driver, link=lnk, output_dir_name=path_for_link_mhtml)
    driver.close()
    print()


def gen_only_home_mhtmls(driver, list_of_links, failed_links, output_dir_name):
    print("\n** Generating home MTHMLs using list of URLs **\n")
    prepare_dir(output_dir_name)
    for link in list_of_links:
        if link not in failed_links:
            print("\n** Generating MHTML for: {} **\n".format(link))
            save_webpage_from_URL(driver, link, output_dir_name)
    driver.close()
    print()
