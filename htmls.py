import os
import re
import pyautogui

from manage_dir import prepare_dir
from manage_webdriver import change_download_dir
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from time import sleep


def download_wait(directory, timeout):
    seconds = 0
    start_dir_size = len(os.listdir(directory))
    while seconds < timeout:
        sleep(1)
        if start_dir_size < len(os.listdir(directory)):
            break
        seconds += 1


def save_as_on_webpage(formatted_link):
    # TODO: Improve this to save in specific dir and change 'Format' to 'Web page, Single File'
    download_timeout = 10
    # Save As
    # ('ctrl', 's') on other OSs.
    pyautogui.hotkey('command', 's')
    sleep(2)
    # Rename and save file to default downloads folder and for download to finish
    pyautogui.typewrite("<" + formatted_link + ">")
    pyautogui.press('enter')
    download_wait(directory=os.path.join(os.path.expanduser('~'), 'Downloads'), timeout=download_timeout)


def write_to_HTML_file(driver, full_file_path):
    with open(full_file_path, 'w+') as f:
        f.write(driver.page_source)
        f.close()


def accept_alert(driver, link):
    try:
        if driver.switch_to.alert is not None:
            print("\n** Closing pop-up on: {} **\n".format(link))
            alert = driver.switch_to.alert
            alert.dismiss()  # alert.accept()
            return True
    except NoAlertPresentException:
        return False


def close_pop_ups(driver, link):
    while True:
        if not accept_alert(driver, link):
            break


def close_privacy_cookie_panes_helper(driver, word, link):
    try:
        element = driver.find_element_by_xpath("//*[contains(., '{}')]".format(word))
        print("\n** Closing privacy/cookies pane on: {} **\n".format(link))
        element.click()
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass
    except ElementClickInterceptedException:
        pass


def close_privacy_cookie_panes(driver, link):
    accept_words = ["Agree", "Accept"]
    for word in accept_words:
        close_privacy_cookie_panes_helper(driver, word, link)
        close_privacy_cookie_panes_helper(driver, word.upper(), link)


def save_webpage_from_URL(driver, link, output_dir_name, child_webpage=False):
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
    # (Keys.CONTROL + 't') on other OSs.
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    # Open webpage link
    driver.get(link)
    # Close any pop-ups
    close_pop_ups(driver, link)
    # Close privacy/cookie pop-up panes
    close_privacy_cookie_panes(driver, link)
    # Write webpage source to HTML file
    write_to_HTML_file(driver, full_file_path)
    # Save as webpage using pyautogui
    # save_as_on_webpage(formatted_link)
    # Close the tab
    # (Keys.CONTROL + 'w') on other OSs.
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
    if child_webpage:
        print("** Saved child webpage **")
        print("\t-- URL: {}".format(link))
        print("\t-- Saved path: {}".format(full_file_path))
    else:
        print("\n** Saved home webpage **")
        print("\t-- URL: {}".format(link))
        print("\t-- Saved path: {}\n".format(full_file_path))


def gen_htmls(driver, list_of_links, dict_of_links, failed_links, output_dir_name):
    print("\n** Generating HTMLs using list of URLs and dictionary of URLs **\n")
    prepare_dir(output_dir_name)
    for link in list_of_links:
        if link not in failed_links:
            print("\n** Generating HTMLs for: {} **\n".format(link))
            save_webpage_from_URL(driver, link, output_dir_name)
            url_domain = re.search('https?://([A-Za-z_0-9.-]+).*', link).group(1)
            relative_path = os.path.join(output_dir_name, "<" + url_domain + ">")
            path_for_link_html = os.path.join(os.getcwd(), relative_path)
            if not (os.path.isdir(path_for_link_html)):
                print("\n** Making directory: {} **\n".format(path_for_link_html))
                os.mkdir(path_for_link_html)
            driver = change_download_dir(driver, relative_path)
            for lnk in dict_of_links[link]:
                save_webpage_from_URL(driver, link=lnk, output_dir_name=path_for_link_html, child_webpage=True)
            driver = change_download_dir(driver, output_dir_name)
    driver.close()
    print()


def gen_only_home_htmls(driver, list_of_links, failed_links, output_dir_name):
    print("\n** Generating home HTMLs using list of URLs **\n")
    prepare_dir(output_dir_name)
    for link in list_of_links:
        if link not in failed_links:
            print("\n** Generating HTML for: {} **\n".format(link))
            save_webpage_from_URL(driver, link, output_dir_name)
    driver.close()
    print()
