from abc import ABC, abstractmethod
from typing import Any

class AbstractScraper(ABC):
    @abstractmethod
    def fetch_content(self, url: str) -> Any:
        """
        Método para fazer a requisição do conteúdo do site.
        Pode usar selenium, requests, scrapy, etc.
        """
        pass

    @abstractmethod
    def parse_content(self, content: Any) -> Any:
        """
        Método para fazer o parsing do conteúdo. Pode usar BeautifulSoup, lxml, etc.
        """
        pass

    @abstractmethod
    def run(self, url: str) -> Any:
        """
        Método principal para executar o scraper: faz a requisição e o parsing.
        """
        pass

