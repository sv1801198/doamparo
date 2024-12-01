import peewee
from peewee import IntegrityError

database = peewee.MySQLDatabase(
    'anaiza',
    user='root',
    password='Va123Va123@',
    host='localhost',
    port=3306
)

class Empresa(peewee.Model):
    nome = peewee.CharField()
    login = peewee.CharField(unique=True)
    senha = peewee.CharField()
    email = peewee.CharField(unique=True)
    telefone = peewee.CharField()

    class Meta:
        database = database

class Categorias(peewee.Model):
    nome = peewee.CharField()
    empresa = peewee.ForeignKeyField(Empresa, backref='cat')

    class Meta: 
        database = database

class Produto(peewee.Model):
    nome = peewee.CharField()
    preco = peewee.DecimalField(max_digits=10, decimal_places=2)
    img_link = peewee.CharField()
    descricao = peewee.CharField(null=True)
    categoria = peewee.ForeignKeyField(Categorias, backref='produto')
    empresa = peewee.ForeignKeyField(Empresa, backref='produtos')

    class Meta: 
        database = database

class Perfil(peewee.Model):
    nome = peewee.CharField(null=True)
    endereco = peewee.CharField(null=True)
    telefone1 = peewee.CharField(null=True)
    telefone2 = peewee.CharField(null=True)
    telefone3 = peewee.CharField(null=True)
    email = peewee.CharField(null=True)
    horario = peewee.CharField(null=True)
    empresa = peewee.ForeignKeyField(Empresa, backref='perfil')

    class Meta: 
        database = database

def create_tables():
    database.create_tables([Empresa], safe=True)
    database.create_tables([Produto], safe=True)
    database.create_tables([Categorias], safe=True)