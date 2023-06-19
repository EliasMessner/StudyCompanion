import os

from langchain.document_loaders import SeleniumURLLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
from typing import Literal
from dotenv import load_dotenv
import logging
load_dotenv()


class Scraper:
    def __init__(self, browser: Literal["firefox", "chrome"] = "firefox"):
        if browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.headless = True
            self.browser = webdriver.Firefox(options=options)
        elif browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.binary_location = os.getenv("CHROME_BINARY_LOCATION")
            options.headless = True
            self.browser = webdriver.Chrome(options=options)

    def destroy(self):
        self.browser.quit()

    def get_medium_search_results(self, query: str) -> list[str]:
        params = {'q': query}
        param_str = urllib.parse.urlencode(params)
        url = f"https://medium.com/search/posts?{param_str}"

        self.browser.get(url)
        post_read_times = self.browser.find_elements(
            By.XPATH, "//span[contains(text(), 'min read')]/ancestor::a[contains(@aria-label, 'Post Preview Reading Time')]")
        post_urls = {prt.get_attribute("href") for prt in post_read_times}

        return list(post_urls)


def remove_member_only_posts(web_content_list):
    result_list = []
    for web_content in web_content_list:
        # check first 100 characters
        if "Member-only story" not in web_content.page_content[0:100]:
            result_list.append(web_content)
        else:
            logging.info(
                f"Removing (Member-only): {web_content.metadata['source']}")
            # TODO remove if logging works in jupyter
            print(f"Removing (Member-only): {web_content.metadata['source']}")
    return result_list


def load_web_content(browser: Literal["firefox", "chrome"] = "firefox", query: str = None, user_supplied_topic: str = None):
    # TODO exclude member-only pages
    scraper = Scraper(browser=browser)

    medium_post_urls = scraper.get_medium_search_results(query=query)
    for url in medium_post_urls:
        logging.info(f"Scraping: {url}")
        print(f"Scraping: {url}")  # TODO remove if logging works in jupyter

    web_loader = SeleniumURLLoader(
        urls=medium_post_urls, browser=browser)
    web_content = web_loader.load()

    # remove member only post
    web_content = remove_member_only_posts(web_content)

    # replace line breaks with whitespaces
    web_content_no_linebreaks = []
    for doc in web_content:
        doc.page_content = doc.page_content.replace("\n\n", " ")
        web_content_no_linebreaks.append(doc)

    return web_content_no_linebreaks
