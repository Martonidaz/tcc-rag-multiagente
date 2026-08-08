# Usamos uma imagem Python enxuta para economizar RAM no sistema
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (otimiza o cache do Docker)
COPY requirements.txt .

# Instala as dependências sem armazenar cache de instalação
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da API
COPY . .

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000