from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import paciente, medico, consulta 

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI()  # Adicione parênteses aqui



# Configuração de CORS
origins = [
    "http://localhost:3000",  # Substitua pelo endereço do seu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas das diferentes entidades
app.include_router(paciente.router, tags=["Pacientes"], prefix="/pacientes")
app.include_router(medico.router, tags=["Medicos"], prefix="/medicos")
app.include_router(consulta.router, tags=["Consultas"], prefix="/consultas")

# Rota de verificação de saúde
@app.get("/")
def root():
    return {"message": " Consulte a documentação da api em http://127.0.0.1:8000/docs#"}
