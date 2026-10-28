import argparse
import json
import csv
import os
import time
import requests
import sys
from pathlib import Path

def llamar_ollama(prompt, modelo, temperatura, max_tokens):
    host = os.environ.get("OLLAMA_HOST", "localhost")
    url = f"http://{host}:11434/api/generate"
    
    payload = {
        "model": modelo,
        "prompt": prompt,
        "temperature": temperatura,
        "options": {
            "num_predict": max_tokens
        }
    }
    
    inicio = time.time()
    try:
        # Usamos stream=True para capturar el instante exacto del primer token (TTFT)
        respuesta = requests.post(url, json=payload, stream=True)
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor de Ollama. ¿Está ejecutándose?")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con el modelo: {e}")
        sys.exit(1)

    ttft = None
    texto_completo = ""
    
    for linea in respuesta.iter_lines():
        if linea:
            datos = json.loads(linea)
            if ttft is None:
                ttft = time.time() - inicio
            
            texto_completo += datos.get("response", "")
            
            if datos.get("done"):
                # Ollama devuelve las métricas totales al finalizar
                eval_duration_ns = datos.get("eval_duration", 0)
                eval_count = datos.get("eval_count", 0)
                
                # Convertir de nanosegundos a segundos para la métrica exigida
                eval_duration_s = eval_duration_ns / 1e9
                tokens_por_segundo = eval_count / eval_duration_s if eval_duration_s > 0 else 0
                
                return texto_completo, ttft, tokens_por_segundo, eval_count

    return texto_completo, ttft, 0, 0

def main():
    parser = argparse.ArgumentParser(description="Inferencia local con Mistral AI")
    parser.add_argument("--model", type=str, required=True, help="Nombre del modelo (ej. mistral)")
    parser.add_argument("--prompts", type=str, default="prompts/suite.json", help="Ruta al archivo de prompts")
    parser.add_argument("--temp", type=float, default=0.7, help="Temperatura de muestreo")
    parser.add_argument("--max_tokens", type=int, default=500, help="Máximo de tokens a generar")
    args = parser.parse_args()

    archivo_prompts = Path(args.prompts)
    if not archivo_prompts.exists():
        print(f"Error: No se encontró el archivo {args.prompts}")
        sys.exit(1)

    with open(archivo_prompts, "r", encoding="utf-8") as f:
        suite = json.load(f)

    resultados = []
    ruta_resultados = Path("results/resultados.csv")
    
    print(f"Iniciando inferencia con el modelo: {args.model}")
    
    for item in suite:
        print(f"\nProcesando prompt {item['id']}: {item['categoria']}...")
        salida, ttft, tps, tokens = llamar_ollama(item["prompt"], args.model, args.temp, args.max_tokens)
        
        print(f"Completado en {ttft:.2f}s (TTFT) | {tps:.2f} tokens/s")
        
        resultados.append({
            "id": item["id"],
            "categoria": item["categoria"],
            "prompt": item["prompt"],
            "salida": salida.strip(),
            "tokens_generados": tokens,
            "ttft_segundos": round(ttft, 4),
            "tokens_por_segundo": round(tps, 2)
        })

    claves = resultados[0].keys()
    with open(ruta_resultados, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, fieldnames=claves)
        dict_writer.writeheader()
        dict_writer.writerows(resultados)
        
    print(f"\n¡Listo! Resultados guardados en {ruta_resultados}")

if __name__ == "__main__":
    main()