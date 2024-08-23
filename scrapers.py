import requests
from typing import Any
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from abstract_scraper import AbstractScraper


class RequestsScraper(AbstractScraper):
    
    def __init__(self, http_client):
        self.http_client = http_client

    def fetch_content(self, url: str) -> str:

        response = self.http_client.get(url)
        response.raise_for_status()
        return response.content

    def parse_content(self, content: str) -> Any:
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def run(self, url: str) -> Any:
        content = self.fetch_content(url)
        return self.parse_content(content)


class SeleniumScraper(AbstractScraper):

    def fetch_content(self, url: str) -> str:
        self.http_client.get(url)
        return self.driver.page_source

    def parse_content(self, content: str) -> Any:
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def run(self, url: str) -> Any:
        content = self.fetch_content(url)
        return self.parse_content(content)

    def __del__(self):
        self.driver.quit()