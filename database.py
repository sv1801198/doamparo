import peewee
from peewee import IntegrityError

# Configuração do banco de dados
database = peewee.MySQLDatabase(
    'anaiza',
    user='root',
    password='Va123Va123@',
    host='localhost',
    port=3306
)

# Modelo Empresa
class Empresa(peewee.Model):
    nome = peewee.CharField()
    login = peewee.CharField(unique=True)
    senha = peewee.CharField()
    email = peewee.CharField(unique=True)
    telefone = peewee.CharField()

    class Meta:
        database = database

# Modelo Categoria
class Categoria(peewee.Model):
    nome = peewee.CharField()
    empresa = peewee.ForeignKeyField(Empresa, backref='categorias')

    class Meta: 
        database = database

# Modelo Produto
class Produto(peewee.Model):
    nome = peewee.CharField()
    preco = peewee.DecimalField(max_digits=10, decimal_places=2)
    img_link = peewee.CharField()
    descricao = peewee.CharField(null=True)
    categoria = peewee.ForeignKeyField(Categoria, backref='produtos')  # Agora é uma ForeignKeyField
    empresa = peewee.ForeignKeyField(Empresa, backref='produtos')

    class Meta: 
        database = database

# Modelo Perfil
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

# Função para criar tabelas
def create_tables():
    database.create_tables([Empresa, Categoria, Produto, Perfil], safe=True)

# Criando as tabelas no banco de dados
if __name__ == "__main__":
    create_tables()
