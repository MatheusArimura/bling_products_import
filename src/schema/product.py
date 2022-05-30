from pony.orm import *
from entities import DB

class Product(DB.Entity):
    id = PrimaryKey(str)
    codigo = Required(str)
    descricao = Required(str)
    tipo = Optional(str)
    situacao = Required(str)
    preco = Required(float)
    precoCusto = Required(float)
    imgCapa = Required(LongStr)
    nomeFornecedor = Optional(str)