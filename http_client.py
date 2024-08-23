import requests
from typing import Any
from selenium import webdriver
from urllib.parse import urlparse
from abc import ABC, abstractmethod
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class AbstractHttpClient(ABC):
    @abstractmethod
    def get(self, url: str, headers: dict = None) -> Any:
        """
        Faz uma requisição GET ao URL especificado.
        """
        pass

    @abstractmethod
    def post(self, url: str, headers: dict = None, payload: dict = None) -> Any:
        """
        Faz uma requisição POST ao URL especificado.
        """
        pass


class RequestsHttpClient(AbstractHttpClient):
    def __init__(self, headers: dict = None, proxies: str = None):
        self.headers = headers
        self.proxies = {'http': proxies}

    def get(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers, proxies=self.proxies)

    def post(self, url: str, payload: dict = None) -> requests.Response:
        return requests.post(url, headers=self.eaders, json=payload, proxies=self.proxies)


class SeleniumHttpClient(AbstractHttpClient):
    def __init__(self, driver_path: str, browser: str = "chrome", user_agent: str = None, proxies: str = None):
        self.user_agent = user_agent
        self.proxies = proxies

        if browser == "chrome":
            self.options = webdriver.ChromeOptions()
            self.options.add_argument('--headless')
            if self.user_agent:
                self.options.add_argument(f'user-agent={self.user_agent}')
            if self.proxies:
                self.options.add_argument(f'--proxy-server={self.proxies}')

            self.driver = webdriver.Chrome(service=ChromeService(driver_path), options=self.options) if driver_path else webdriver.Chrome(options=self.options)
            self.driver.maximize_window()

        elif browser == "firefox":
            self.profile = FirefoxProfile()
            if self.proxies:
                parsed_proxy_url = urlparse(self.proxies)
                self.profile.set_preference("network.proxy.type", 1)
                self.profile.set_preference("network.proxy.ssl", parsed_proxy_url.hostname)
                self.profile.set_preference("network.proxy.ssl_port", parsed_proxy_url.port)
                self.profile.update_preferences()

            self.options = FirefoxOptions()
            self.options.add_argument('--headless')
            if self.user_agent:
                self.options.set_preference("general.useragent.override", self.user_agent)

            self.driver = webdriver.Firefox(service=FirefoxService(driver_path), options=self.options, firefox_profile=self.profile) if driver_path else webdriver.Firefox(options=self.options, firefox_profile=self.profile)

        else:
            raise ValueError("Navegador não suportado: escolha 'chrome' ou 'firefox'")

    def get(self, url: str, headers: dict = None) -> str:
        self.driver.get(url)
        return self.driver.page_source

    def post(self, url: str, headers: dict = None, payload: dict = None) -> Any:
        self.driver.get(url)
        self.driver.execute_script("""
            fetch(arguments[0], {
                method: 'POST',
                headers: arguments[1],
                body: JSON.stringify(arguments[2])
            }).then(response => response.json())
        """, url, headers, payload)
        return "POST feito via Selenium"

    def __del__(self):
        self.driver.quit()