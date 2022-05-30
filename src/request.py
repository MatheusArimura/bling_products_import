from types import NoneType
import requests
import time
from settings import API_KEY
from entities import Product
from pony.orm import *

class Products():
    def __init__(self):
        self.api_key = API_KEY
        self.output_type = "json"
        self.consoles = ['PS5', 'PS4', 'PS3', 'PS2', 'PS1', 'Xbox Series', 'Xbox One', 'Xbox 360', 'Switch']

    def execute(self):
        page = 1
        valid = True
        while valid == True:
            response = requests.get(f"https://bling.com.br/Api/v2/produtos/page={page}/{self.output_type}&apikey={self.api_key}&imagem=S")
            fetch_response = response.json()
            if "erros" in fetch_response['retorno']:
                print(fetch_response)
                valid = False
            else:
                for product in fetch_response['retorno']['produtos']:
                    self.handle_product(product_data=product['produto'])

                page = page + 1
            time.sleep(1)

    @db_session
    def save_product(self, product_data: dict):
        duplicate_test = Product.get(id=product_data['id'])
        if duplicate_test:
            duplicate_test.set(**product_data)
            print(f"Produto atualizado: {duplicate_test}")
        else:             
            product = Product(**product_data)
            print(f"Produto inserido: {product}")

        return True

    def handle_product(self, product_data: dict) -> bool:
        result = False
        try:
            if 'Jogos' in product_data['categoria']['descricao'] or 'Console' in product_data['categoria']['descricao'] or 'Acessórios' in product_data['categoria']['descricao'] or '(Usado)' in product_data['descricao'] or any(console in product_data['descricao'] for console in self.consoles):
                if product_data['codigo']:
                    formatted_data = self.format_product(unformatted_data=product_data)
                    self.save_product(formatted_data)
                    result = True
                else:
                    result = False
            else:
                print(f'Nome do produto: {product_data["descricao"]} -> {product_data["categoria"]["descricao"]}')
        except:
            print("Produto não possui categoria.")

        return result

    def format_product(self, unformatted_data: dict) -> dict:
        validated_data = self.validate_data(unformatted_data)
        try:
            title = validated_data['descricao']
            body = {
                "id": validated_data['id'],
                "codigo": validated_data['codigo'],
                "descricao": title.replace('(Usado)', ""),
                "tipo": validated_data['tipo'],
                "situacao": validated_data['situacao'],
                "preco": float(validated_data['preco']),
                "precoCusto": float(validated_data['precoCusto']),
                "imgCapa": validated_data['imagem'][0]["link"].replace("\\", ""),
                "nomeFornecedor": validated_data['nomeFornecedor'],
            }
        except:
            title = validated_data['descricao']
            body = {
                "id": validated_data['id'],
                "codigo": validated_data['codigo'],
                "descricao": title.replace('(Usado)', ""),
                "tipo": validated_data['tipo'],
                "situacao": validated_data['situacao'],
                "preco": float(validated_data['preco']),
                "precoCusto": float(validated_data['precoCusto']),
                "imgCapa": "",
                "nomeFornecedor": validated_data['nomeFornecedor'],
            }
        return body

    def validate_data(self, unformatted_data: dict) -> dict:
        for key, value in unformatted_data.items():
            if isinstance(value, NoneType):
                if key == "precoCusto":
                    unformatted_data[key] = 0
                else:
                    unformatted_data[key] = ""

        return unformatted_data
