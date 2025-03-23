import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings  # Importa as configurações do arquivo config.py

# Utilizando as variáveis de configuração da instância settings
db_user = settings.POSTGRES_USER
db_password = settings.POSTGRES_PASSWORD
db_host = settings.POSTGRES_HOST
db_name = settings.POSTGRES_DB
db_port = settings.DATABASE_PORT

# URL de conexão sem o nome do banco (para criar o banco, se necessário)
admin_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Função para verificar e criar o banco de dados
def create_database_if_not_exists():
    try:
        # Conectando ao PostgreSQL usando o banco padrão "postgres"
        conn = psycopg2.connect(admin_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Verifica se o banco já existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            print(f"Banco de dados '{db_name}' não encontrado. Criando...")
            cursor.execute(f"CREATE DATABASE {db_name}")
        else:
            print(f"Banco de dados '{db_name}' já existe.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao verificar/criar banco de dados: {e}")

# Verifica e cria o banco antes de configurar o SQLAlchemy
create_database_if_not_exists()

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
