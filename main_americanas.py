import logging
from scrapers import RequestsScraper
from random_headers import RandomHeaders
from http_client import RequestsHttpClient
from scrapeds import AmericanasScraped

def main():
    logging.basicConfig(level=logging.INFO)
    
    scrapeops_key = 'c36424ca-4337-481c-85f9-43696441d7ea'
    proxy = 'http://brd-customer-hl_4ba48506-zone-data_center:zkus3rbg4d1v@brd.superproxy.io:22225'
    
    random_headers = RandomHeaders(scrapeops_key, http_client=RequestsHttpClient())
    http_client = RequestsHttpClient(headers, proxy)
    scrapper = RequestsScraper(http_client)
    scraped = AmericanasScraped()
    headers_list = random_headers.get_headers_list()
    headers = random_headers.get_random_header(headers_list)
    
    headers = {
        'authority': 'keyword-search-v1-ads.b2w.io',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'if-none-match': 'W/"24-yTziSr0RexiKyKhceywD5X7oaqo"',
        'origin': 'https://www.americanas.com.br',
        'referer': 'https://www.americanas.com.br/',
        'sec-ch-ua': 'Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }
    
    url = 'https://www.americanas.com.br/busca/bravecto/'
    response = scrapper.fetch_content(url)
    
    parsed_content = scrapper.parse_content(response)
    json_data = scraped.get_content_data(parsed_content)
    df_products = scraped.process_products(json_data)
    df_sellers = scraped.process_sellers(df_products, json_data)

## Completar código com upload para o BigQuery (bronze_table)