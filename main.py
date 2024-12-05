from database import *

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

create_tables()

print("-----------------------------------------//-----------------------------------------")

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(request: Request):
    form_data = await request.form()
    login_data = Empresa(
        username=form_data['username'],
        password=form_data['password'],
    )
    return {"Cadastro" : "Tentando Cadastrar"}


@app.get("/cadastro_empresa")
async def get_create_empresa(request: Request):
    return templates.TemplateResponse("cadastrar_empresa.html", {"request": request})

@app.get("/empresas_cadastradas")
async def get_empresas_cadastradas(request: Request):
    # Busca todas as empresas no banco de dados
    empresas = Empresa.select()

    # Passa a lista de empresas para o template
    return templates.TemplateResponse("lista_empresas.html", {"request": request, "empresas": empresas})

@app.post("/cadastro_empresa")
async def post_create_empresa(request: Request):
    form_data = await request.form()
    nova_empresa = Empresa(
        nome=form_data['nome'],
        login=form_data['login'],
        senha=form_data['senha'],
        email=form_data['email'],
        telefone=form_data['telefone'],
    )
    try:
        nova_empresa.save()
        return templates.TemplateResponse("lista_empresas.html", {"request": request, "empresas": Empresa.select()})
    except IntegrityError as e:
        return {"error": str(e)}
    except:
        return {"error": "um erro inesperado ocorreu"}

@app.get("/cadastro_categoria")
async def get_cadastro_categoria(request: Request):
    return templates.TemplateResponse("cadastrar_categoria.html", {"request": request})

@app.get("/categorias_cadastradas")
async def get_categorias_cadastradas(request: Request):
    # Busca todas as categorias no banco de dados
    categorias = Categoria.select()

    # Passa a lista de categorias para o template
    return templates.TemplateResponse("lista_categorias.html", {"request": request, "categorias": categorias})

@app.post("/cadastro_categoria")
async def post_cadastro_categoria(request: Request):
    form_data = await request.form()
    nova_categoria = Categoria(
        nome=form_data['nome'],
        empresa=form_data['empresa']
    )
    try:
        nova_categoria.save()
        return templates.TemplateResponse("lista_categorias.html", {"request": request, "categorias": Categoria.select()})
    except IntegrityError as e:
        return {"error": str(e)}
    except:
        return {"error": "um erro inesperado ocorreu"}

@app.get("/cadastro_produto")
async def get_create_produto(request: Request):
    return templates.TemplateResponse("cadastrar_produto.html", {"request": request})

@app.post("/cadastro_produto")
async def post_cadastro_produto(request: Request):
    form_data = await request.form()
    novo_produto = Produto(
        nome=form_data['nome'],
        preco=form_data['preco'],
        descricao=form_data['descricao'],
        img_link=form_data['img_link'],
        categoria=form_data['categoria'],
        empresa=form_data['empresa']
    )
    try:
        novo_produto.save()
        return templates.TemplateResponse("lista_produtos.html", {"request": request, "produtos": Produto.select()
})
    except IntegrityError as e:
        return {"error": str(e)}
    except:
        return {"error": "um erro inesperado ocorreu"}
    
@app.get("/produtos_cadastrados")
async def get_produtos_cadastrados(request: Request):
    # Busca todos os produtos no banco de dados
    produtos = Produto.select()

    # Passa a lista de produtos para o template
    return templates.TemplateResponse("lista_produtos.html", {"request": request, "produtos": produtos})