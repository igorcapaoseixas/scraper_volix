from abc import ABC, abstractmethod
from typing import Any
import pandas as pd
import json

class AbstractScraped(ABC):

    @abstractmethod
    def get_content_data(self, parsed_content: Any) -> Any:
        """Método para pegar o conteúdo retornado do site."""
        pass

class AmericanasScraped(AbstractScraped):
    
    def get_content_data(self, parsed_content: str) -> str:
        """Extrai o script que contém '__APOLLO_STATE__' do HTML."""
        scripts = parsed_content.find_all('script')
        for script in scripts:
            if '__APOLLO_STATE__' in script.text:
                return json.loads(script.text[26:])
        return None

    def url_finder(self, product_id: str) -> str:
        """Gera a URL do produto com base no ID."""
        return f'https://americanas.com.br/produto/{product_id}'

    def process_products(self, data):
        """Processa os produtos a partir do JSON extraído."""
        offset_key = next((x for x in data['ROOT_QUERY'] if 'search' in x), None)
        if not offset_key:
            raise KeyError("Key 'search' not found JSON.")
        
        products_json = data['ROOT_QUERY'][offset_key]['products']
        products = []
        
        for x in products_json:
            try:
                product = x['product'].get('name', 'Nome indisponível')
                price = (x['product']
                        .get('offers({"promoted":true,"sort":""})', {})
                        .get('result', [{}])[0]
                        .get('bestPaymentOption', {})
                        .get('installment({"filter":"min"})', [{}])[0]
                        .get('value', 'Preço indisponível'))
                seller_id = (x['product']
                            .get('offers({"promoted":true,"sort":""})', {})
                            .get('result', [{}])[0]
                            .get('seller', {})
                            .get('__ref', 'ID do vendedor indisponível'))
                product_id = x['product'].get('id', 'ID indisponível')
                link = self.url_finder(product_id)
                
                products.append([product, price, seller_id, product_id, link])
            
            except (KeyError, IndexError, TypeError) as e:
                print(f"|Exception raised: {e}")
                continue
            
        df_products = pd.DataFrame(products, columns=['produto', 'preco', 'id_vendedor', 'cod_produto', 'link'])
        
        return df_products

    def process_sellers(self, df_products, data):
        """Processa os vendedores com base nos IDs extraídos."""
        sellers_ids = df_products['id_vendedor'].unique().tolist()
        df_vendedores = pd.DataFrame()

        for seller_id in sellers_ids:
            info_vendedor = data.get(seller_id, {})
            if info_vendedor:
                df_iv = pd.json_normalize(info_vendedor)
                df_iv['id_vendedor'] = seller_id
                df_vendedores = pd.concat([df_vendedores, df_iv], ignore_index=True)
        
        return df_vendedores
