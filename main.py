from database import *
from utils import *

from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

create_tables()

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(request: Request,
    username: str = Form(...),
    password: str = Form(...),
    persist: bool = Form(False)  # Define um valor padrão para a checkbox
   
):
    if verificar_login(username, password):

        access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        response = templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "message": "Login realizado com sucesso!",
                "message_type": "success",
            }
        )
        response.set_cookie(
            key="access_token", 
            value=access_token, 
            httponly=True,  # Isso ajuda a evitar acesso via JavaScript (segurança)
            max_age=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # Expira com o token
            secure=True,  # Use True para HTTPS
            samesite="Strict"  # Para evitar o envio em requisições de terceiros
        )

        return response


    else:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "message": "Login ou senha incorretos!",
                "message_type": "error",
            }
        )

@app.get("/logout")
async def logout(request: Request, response: Response):
    # Remove o cookie de autenticação (o token de acesso)
    
    response = templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "message": "Deslogado com sucesso!",
                "message_type": "success",
            }
        )
    
    response.delete_cookie("access_token")

    return response

@app.get("/protected-route")
async def protected_route(request: Request):
    """
    Rota protegida que verifica o token JWT presente no cookie.
    """
    # Resgata o cookie "access_token"
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado")
    
    # Verifica o token
    username = verify_token(token)
    
    # Retorna o conteúdo protegido
    return {"message": f"Bem-vindo, {username}!"}

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