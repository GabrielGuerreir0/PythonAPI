from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import paciente, medico, consulta 

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI()  # Adicione parênteses aqui

# Configuração de CORS
origins = [
    "http://localhost:8000", 
     # Substitua pelo endereço do seu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")

# Inclui as rotas das diferentes entidades
app.include_router(paciente.router, tags=["Pacientes"], prefix="/pacientes")
app.include_router(medico.router, tags=["Medicos"], prefix="/medicos")
app.include_router(consulta.router, tags=["Consultas"], prefix="/consultas")

# Rota de verificação de saúde
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/listaMedicos", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("medicos.html", {"request": request})

@app.get("/listaPacientes", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("pacientes.html", {"request": request})

@app.get("/listaConsultas", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("consulta.html", {"request": request})