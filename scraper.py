from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
from typing import Literal, List

class Scraper:
    def __init__(self, browser: Literal["firefox", "chrome"] = "firefox"):
        if browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            options  = Options()
            options.headless = True
            self.browser = webdriver.Firefox(options=options)
        elif browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            options  = Options()
            options.headless = True
            self.browser = webdriver.Chrome(options=options)

    def destroy(self):
        self.browser.quit()
        
    def get_medium_search_results(self, query: str) -> List[str]:
        params = {'q': query}
        param_str = urllib.parse.urlencode(params)
        url = f"https://medium.com/search/posts?{param_str}"

        self.browser.get(url)
        post_read_times = self.browser.find_elements(By.XPATH, "//span[contains(text(), 'min read')]/ancestor::a[contains(@aria-label, 'Post Preview Reading Time')]")
        post_urls = {prt.get_attribute("href") for prt in post_read_times}
        
        return post_urls