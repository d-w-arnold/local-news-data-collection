import os
import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_webdriver(output_dir):
    driver = webdriver.Chrome(executable_path=chromedriver_binary.chromedriver_filename,
                              options=get_webdriver_options(output_dir))
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    return driver


def get_webdriver_options(output_dir):
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    prefs = {"profile.default_content_settings.popups": 0,
             'download.directory_upgrade': True,
             "download.default_directory": os.path.join(os.getcwd(), output_dir)}
    options.add_experimental_option("prefs", prefs)
    return options


def change_download_dir(driver, htmls_output_dir):
    path = os.path.join(os.getcwd(), htmls_output_dir)
    print("\n** Changed download path to: {} **\n".format(path))
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': path}}
    driver.execute("send_command", params)
    return driver
