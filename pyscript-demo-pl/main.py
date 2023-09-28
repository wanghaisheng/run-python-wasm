"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""

from playwright.sync_api import Page
from typing import List
from js import document


class DuckDuckGoSearchPage:

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_button = page.locator('#search_button_homepage')
        self.search_input = page.locator('#search_form_input_homepage')
    
    def load(self) -> None:
        self.page.goto(self.URL)
    
    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.search_button.click()


class DuckDuckGoResultPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
    
    def result_link_titles(self) -> List[str]:
        self.result_links.nth(4).wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum

def basic_duckduckgo_search(
    phrase: str,
    page: Page,
    search_page: DuckDuckGoSearchPage,
    result_page: DuckDuckGoResultPage) -> None:
    
    # Given the DuckDuckGo home page is displayed
    search_page=DuckDuckGoSearchPage
    search_page.load()
    input_text = document.querySelector("#query")
    query = input_text.value
    # When the user searches for a phrase
    search_page.search(query)
    result_page=DuckDuckGoResultPage(search_page.page)
    output_div = document.querySelector("#output")
    output_div.innerText =result_page.result_link_titles()