# 1. Imagen base ligera y con versión fija
FROM python:3.10-slim

# 2. Crear un usuario no root por seguridad
RUN useradd -m -r appuser

# Establecer el directorio de trabajo
WORKDIR /app

# 3. Capas ordenadas para aprovechar la caché: primero dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar código fuente y datos
COPY src/ /app/src/
COPY prompts/ /app/prompts/

# Crear carpeta para los resultados y dar permisos al usuario no root
RUN mkdir -p /app/results && chown -R appuser:appuser /app

# 5. Cambiar al usuario no root
USER appuser

# 6. El modelo no se copia en la imagen (se conectará al host o se montará)
# Configurar el punto de entrada
ENTRYPOINT ["python", "src/inference.py"]
CMD ["--model", "mistral", "--temp", "0.7", "--max_tokens", "500"]  