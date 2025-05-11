# Sistema de Conversación Multi-Agente para Preguntas de Telecomunicaciones

Este sistema implementa una arquitectura multi-agente para analizar y responder preguntas complejas sobre telecomunicaciones, generando automáticamente respuestas, análisis críticos y versiones mejoradas.

## Características

- **Conversación multi-agente**: Interacción entre experto, crítico y facilitador
- **Análisis crítico**: Evaluación detallada de las respuestas según múltiples criterios
- **Generación de mejoras**: Versiones mejoradas de las respuestas basadas en análisis
- **Reflexión sobre la IA**: Análisis de la utilidad y limitaciones de la IA
- **Soporte para múltiples modelos**: Compatible con modelos mediante Ollama
- **Generación en español**: Forzar todas las respuestas en español
- **Análisis directo**: Respuestas directas sin proceso de pensamiento

## Requisitos

- Python 3.8+
- Ollama instalado (`curl -fsSL https://ollama.com/install.sh | sh`)
- Modelo deepseek-coder:33b descargado (`ollama pull deepseek-coder:33b`)

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias:
```bash
pip install requests
```

## Uso

### 1. Generar respuestas iniciales

```bash
python main.py --model ollama --ollama-model deepseek-coder:33b --max-turns 3
```

Esto generará respuestas para todas las preguntas predefinidas y las guardará en el directorio `outputs/`.

Para una pregunta específica con más turnos de conversación:

```bash
python main.py --model ollama --ollama-model deepseek-coder:33b --question 5g_network_slicing --max-turns 5
```

### 2. Analizar críticamente las respuestas

```bash
python response_analyzer_with_llm.py --ollama-model deepseek-coder:33b
```

Esto generará un análisis crítico detallado en `outputs/analisis_critico_llm.md`.

## Parámetros de configuración

El sistema admite varios parámetros para personalizar su funcionamiento:

- `--model`: Modelo a utilizar (deepseek-r1, ollama, mock)
- `--model-variant`: Variante del modelo (ej. 32b)
- `--question`: Pregunta específica a abordar
- `--output-dir`: Directorio para guardar las salidas
- `--ollama-model`: Nombre del modelo en Ollama
- `--ollama-api`: URL base de la API de Ollama
- `--max-turns`: Número máximo de turnos de conversación (defecto: 3)
- `--debug`: Habilitar logs de depuración

## Forzar contenido en español

Para asegurar que todo el contenido generado esté en español, el modelo OllamaModel está configurado para generar respuestas en español.

## Formato de respuestas

Las respuestas se generan sin incluir el proceso de pensamiento, mostrando solo el análisis final, las recomendaciones concisas y las respuestas mejoradas directamente.

## Estructura del proyecto

- `main.py`: Punto de entrada principal, gestiona la conversación entre agentes
- `model_provider.py`: Provee interfaces para diferentes modelos de IA
- `agent_utils.py`: Utilidades para los agentes (definiciones, configuración, etc.)
- `response_analyzer.py`: Versión básica para análisis crítico
- `response_analyzer_with_llm.py`: Versión avanzada que usa LLM para análisis

## Archivos generados

- `outputs/resumen_respuestas.txt`: Resumen de todas las respuestas y análisis
- `outputs/[topic]_conversation.txt`: Conversación completa para cada tema
- `outputs/analisis_critico_llm.md`: Análisis crítico detallado con mejoras

## Preguntas predefinidas

El sistema viene con 5 preguntas predefinidas sobre telecomunicaciones:

1. 5G Network Slicing
2. Cloud Computing en Telecomunicaciones
3. Evolución del tráfico de Internet
4. QoE en 5G
5. Edge Computing en Telecomunicaciones

## Licencia

MIT 