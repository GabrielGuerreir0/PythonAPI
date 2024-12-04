# FastAPI CRUD Operations

This is a simple FastAPI application that provides CRUD operations for a healthcare management system involving Patients, Doctors, and Appointments. The backend is powered by FastAPI, with SQLite as the database, and SQLAlchemy for ORM.

## Tecnologias Utilizadas

- **Python 3.9+**
- **FastAPI**: Framework para criação de APIs rápidas e eficientes.
- **SQLAlchemy**: ORM para gerenciar interações com o banco de dados.
- **SQLite**: Banco de dados leve para persistência de dados.

---

## Pré-requisitos

1. **Python 3.9+** instalado.
2. Gerenciador de pacotes `pip`.

---

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-diretorio>
   ```

2. **Crie e ative um ambiente virtual:**

   No Linux/macOS:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   No Windows:

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o banco de dados SQLite:**
   O banco de dados será criado automaticamente ao executar o código, com base nos modelos definidos.

---

## Executando a API

1. Inicie o servidor:

   ```bash
   uvicorn main:app --reload
   ```

2. Acesse a documentação interativa no navegador:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Endpoints

### Pacientes

- **GET /pacientes**: Lista todos os pacientes.
- **POST /pacientes**: Cria um novo paciente.
- **PUT /pacientes/{paciente_id}**: Atualiza um paciente existente.
- **DELETE /pacientes/{paciente_id}**: Deleta um paciente.

### Médicos

- **GET /medicos**: Lista todos os médicos.
- **POST /medicos**: Cria um novo médico.
- **PUT /medicos/{medico_id}**: Atualiza um médico existente.
- **DELETE /medicos/{medico_id}**: Deleta um médico.

### Consultas

- **GET /consultas**: Lista todas as consultas.
- **POST /consultas**: Cria uma nova consulta.
- **PUT /consultas/{consulta_id}**: Atualiza uma consulta existente.
- **DELETE /consultas/{consulta_id}**: Deleta uma consulta.

---

## Modelos de Dados

### Paciente

- **nome**: String
- **idade**: Inteiro
- **historico_medico**: String

### Médico

- **nome**: String
- **especialidade**: String

### Consulta

- **paciente_id**: Inteiro (referência a `Paciente`)
- **medico_id**: Inteiro (referência a `Medico`)
- **data**: String
- **hora**: String

---
