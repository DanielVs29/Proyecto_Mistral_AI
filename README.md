# Proyecto de Investigación - Explorando la Inteligencia Artificial con Mistral AI

Curso: Programación 4 - Universidad Central  
Estudiante: Daniel Vargas Soto 
Fecha: Octubre 2026  

# Descripción del Proyecto
El objetivo principal de este proyecto es demostrar la instalación, configuración y ejecución de un Modelo de Lenguaje Grande (LLM) de forma 100% local. Utilizando Mistral 7B a través de Ollama, el proyecto ilustra cómo automatizar la interacción con una inteligencia artificial mediante Python sin depender de servicios en la nube.

# Requisitos Previos

Para reproducir este proyecto, asegúrese de contar con el siguiente software instalado en su equipo:

* [Ollama](https://ollama.com/): Motor de inferencia local.
* Python 3.8+: Requerido para la ejecución nativa del script.
* [Docker Desktop](https://www.docker.com/): Para pruebas en contenedor.
* Git: Para clonar este repositorio.

# Como Reproducir este Proyecto


1. Clonar el repositorio y entrar a la carpeta:
```bash
git clone https://github.com/DanielVs29/Proyecto_Mistral_AI.git
cd Proyecto_Mistral_AI
```

2. Descargar el modelo de IA local:
```bash
ollama pull mistral
```

3. Construir la imagen de Docker:
```bash
docker build -t mistral-eval .
```

4. Ejecutar mediante Docker:
```bash
docker run --rm -e OLLAMA_HOST="host.docker.internal" mistral-eval --model mistral --prompts prompts/suite.json
```