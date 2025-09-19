# Usa a imagem oficial do Python 3.13
FROM python:3.13

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o Poetry
RUN pip install poetry

# Copia os arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala as dependências do projeto
RUN poetry install --no-root

# Copia o restante do projeto
COPY . .

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
