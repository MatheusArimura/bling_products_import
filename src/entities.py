from unittest import TestResult
from pony.orm import *
from settings import DB_PSWD, DB_HOST, DB_NAME, DB_PORT, DB_USER

db = Database()
db.bind(provider='mysql', host=DB_HOST, user=DB_USER, passwd=DB_PSWD, db=DB_NAME, port=DB_PORT)

class Product(db.Entity):
    id = PrimaryKey(str)
    codigo = Required(str)
    descricao = Required(str)
    tipo = Optional(str)
    situacao = Required(str)
    preco = Required(float)
    precoCusto = Optional(float)
    imgCapa = Optional(LongStr)
    nomeFornecedor = Optional(str)

db.generate_mapping(create_tables=True)