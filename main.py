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
        return {"message": "Empresa cadastrada com sucesso!"}
    except IntegrityError as e:
        return {"error": str(e)}
    except:
        return {"error": "um erro inesperado ocorreu"}

@app.get("/cadastro_categoria")
async def get_cadastro_categoria(request: Request):
    return templates.TemplateResponse("cadastrar_categoria.html", {"request": request})

@app.post("/cadastro_categoria")
async def post_cadastro_categoria(request: Request):
    form_data = await request.form()
    nova_categoria = Categorias(
        nome=form_data['nome'],
        empresa=form_data['empresa']
    )
    try:
        nova_categoria.save()
        return {"message": "Categoria cadastrada com sucesso!"}
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
        empresa=form_data['empresa']
    )
    try:
        novo_produto.save()
        return {"message": "Produto cadastrado com sucesso!"}
    except IntegrityError as e:
        return {"error": str(e)}
    except:
        return {"error": "um erro inesperado ocorreu"}