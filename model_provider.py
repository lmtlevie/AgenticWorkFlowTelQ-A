"""
Module for providing model interfaces for different LLM backends
"""
import os
import logging
import json
import requests
from typing import Dict, Any, List, Optional, Union

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

logger = logging.getLogger(__name__)

class ModelInterface:
    """Base interface for language models"""
    
    def __init__(self):
        """Initialize the model interface"""
        pass
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response to the given prompt"""
        raise NotImplementedError("Subclasses must implement this method")

class MockModel(ModelInterface):
    """Mock model for testing"""
    
    def __init__(self):
        """Initialize the mock model"""
        super().__init__()
        self.responses = {
            "Experto en Telecomunicaciones": [
                "Como experto en Telecomunicaciones, puedo explicar que el Network Slicing es una tecnología clave en 5G que permite virtualizar la red física en múltiples redes lógicas independientes. Cada 'slice' puede ser optimizado para diferentes casos de uso, como el de vehículos conectados (V2X) que menciona.\n\nPara la gestión autónoma del ciclo de vida de un slice mediante IA, podemos dividirlo en cuatro fases:\n\n1. Creación: La IA podría analizar los requisitos específicos de V2X (baja latencia, alta fiabilidad) y automatizar la configuración de los recursos de red necesarios, definiendo las políticas de QoS adecuadas.\n\n2. Monitorización: La IA monitorizaría continuamente parámetros clave como:\n   - Latencia (crítica para comunicaciones V2X, idealmente <10ms)\n   - Ancho de banda (suficiente para transmisión de datos de sensores y video)\n   - Fiabilidad (99.999% para aplicaciones de seguridad V2X)\n   - Densidad de conexiones (en áreas de tráfico denso)\n   - Movilidad (handovers sin interrupciones)\n\n3. Adaptación: Basándose en los datos monitorizados, la IA podría:\n   - Ajustar dinámicamente los recursos asignados según la densidad de vehículos\n   - Redistribuir capacidad en tiempo real durante eventos de tráfico inusuales\n   - Priorizar tráfico crítico de seguridad sobre aplicaciones de entretenimiento\n   - Predecir congestión y realizar ajustes preventivos\n\n4. Terminación: La IA podría determinar cuándo un slice ya no es necesario o debe ser reconfigurado, liberando recursos eficientemente.\n\nLos desafíos principales de esta automatización incluyen:\n\n1. Seguridad entre slices: Garantizar aislamiento completo entre slices para evitar que problemas en uno afecten a otros, especialmente crítico en aplicaciones de seguridad V2X.\n\n2. Complejidad de orquestación: Coordinar recursos a través de diferentes dominios y proveedores de infraestructura.\n\n3. Predicción precisa: Anticipar correctamente necesidades futuras para adaptación proactiva.\n\n4. Latencia de decisión: Asegurar que la propia IA pueda tomar decisiones suficientemente rápido para casos de uso V2X.\n\n5. Interoperabilidad: Garantizar funcionamiento con diferentes fabricantes de equipos y vehículos.\n\n6. Cumplimiento regulatorio: Adaptarse a diferentes normativas según región geográfica, especialmente en seguridad vial.",
                "Analizando la adopción de arquitecturas Cloud por operadores de telecomunicaciones, es importante distinguir primero entre VNF (Virtual Network Functions) y CNF (Cloud-native Network Functions).\n\nLas VNF representan la primera generación de virtualización, donde las funciones de red tradicionales se virtualizaron pero manteniendo una arquitectura monolítica. Las CNF, en cambio, adoptan completamente los principios cloud-native: están basadas en microservicios, contenedores, son altamente escalables y diseñadas para orquestación automatizada.\n\nEl impacto de Cloud y Edge Computing en las redes Telco es profundo:\n\n1. Arquitectura de red: La infraestructura evoluciona hacia un modelo distribuido con procesamiento tanto centralizado (cloud) como descentralizado (edge). Esto permite:\n   - Despliegue flexible de funciones de red donde sean más eficientes\n   - Reducción de latencia para servicios críticos mediante edge computing\n   - Mayor resiliencia mediante distribución geográfica\n\n2. Gestión operativa: Las operaciones se transforman hacia:\n   - Automatización intensiva (CI/CD, DevOps aplicado a infraestructura)\n   - Orquestación inteligente mediante IA/ML\n   - Monitorización basada en análisis predictivo\n\n3. Mecanismos de IA para orquestación:\n   - Predicción de carga: Algoritmos que anticipan picos de tráfico permitiendo escalado proactivo\n   - Ubicación óptima de funciones: Determinación automática de si una función debe ejecutarse en cloud central o edge\n   - Healing automático: Detección y resolución de fallos sin intervención humana\n   - Optimización energética: Ajuste dinámico del consumo según carga real\n   - Gestión dinámica de SLAs: Asignación inteligente de recursos según acuerdos de nivel de servicio\n\n4. Complejidades de gestión de entornos híbridos:\n   - Coexistencia prolongada de infraestructuras físicas, virtuales y cloud-native\n   - Fragmentación tecnológica que dificulta la visibilidad unificada\n   - Diferentes ciclos de vida y metodologías de actualización\n   - Seguridad en entornos multi-vendor y multi-cloud\n   - Gestión de redundancia entre sistemas legados y nuevos\n   - Interoperabilidad entre componentes con diferentes niveles de madurez\n\nUn aspecto crítico es el cambio cultural y organizativo necesario, exigiendo nuevas competencias y metodologías ágiles. Los operadores más exitosos son aquellos que abordan la transformación no solo como un cambio tecnológico sino también organizacional.",
                "Recomendaría seguir explorando sobre el ciclo de vida en entornos cloud-native para telecomunicaciones."
            ],
            "Crítico de Telecomunicaciones": [
                "Tras analizar la respuesta del experto sobre Network Slicing, puedo ofrecer la siguiente crítica basada en los criterios establecidos:\n\n1. Claridad de la explicación de Network Slicing: \nLa explicación es adecuada y clara, definiendo correctamente el Network Slicing como la virtualización de la red física en múltiples redes lógicas independientes. Sin embargo, podría haber profundizado más en los aspectos técnicos de cómo se implementa esta separación (usando SDN, NFV, virtualización) y la arquitectura que lo hace posible en 5G (separación del plano de control y usuario).\n\n2. Detalle del rol de la IA en cada fase del ciclo de vida:\nEl experto ha estructurado bien las cuatro fases (creación, monitorización, adaptación y terminación), explicando en cada una cómo intervendría la IA. En la fase de creación, menciona correctamente el análisis de requisitos y configuración automática, pero podría haber detallado más los algoritmos específicos que la IA utilizaría para traducir requisitos de alto nivel en configuraciones técnicas.\n\nEn cuanto a la monitorización, enumera claramente los parámetros principales, incluso proporcionando valores de referencia adecuados para V2X (latencia <10ms, fiabilidad 99.999%).\n\nEn la adaptación, menciona varios escenarios relevantes de ajuste dinámico, pero podría haber elaborado más sobre los mecanismos de aprendizaje por refuerzo que permitirían a la IA mejorar con el tiempo.\n\n3. Parámetros mencionados para V2X:\nLos parámetros citados son precisamente los más relevantes para V2X: latencia ultra-baja, alta fiabilidad, ancho de banda adecuado, densidad de conexiones y movilidad. Acierta especialmente al mencionar no solo los parámetros tecnológicos sino también su contexto en escenarios de tráfico real.\n\n4. Identificación de desafíos realistas:\nLa respuesta identifica correctamente los desafíos principales, incluyendo los mencionados en los criterios (seguridad entre slices y complejidad de orquestación). Además, añade otros desafíos pertinentes como la predicción precisa, la latencia de decisión de la propia IA, la interoperabilidad y el cumplimiento regulatorio.\n\nEn resumen, la respuesta es sólida y completa, cubriendo todos los aspectos solicitados. Las principales áreas de mejora serían una explicación más profunda de los mecanismos técnicos de implementación del Network Slicing y más detalles sobre los algoritmos específicos de IA que se aplicarían en cada fase del ciclo de vida.",
                "La respuesta sobre Cloud Computing en telecomunicaciones es comprehensiva, pero requiere un análisis crítico según los criterios establecidos:\n\n1. Diferenciación entre VNF y CNF:\nEl experto establece correctamente la distinción entre VNF como primera generación de virtualización con arquitectura monolítica y CNF como evolución cloud-native basada en microservicios y contenedores. Sin embargo, falta profundidad en aspectos técnicos clave como:\n- Diferencias en el modelo de despliegue y ciclo de vida\n- Implicaciones en el consumo de recursos\n- Diferencias en portabilidad y dependencias del sistema operativo\n- Mecanismos de recuperación ante fallos\n\n2. Relación entre Cloud/Edge y red Telco:\nLa explicación de la arquitectura distribuida con procesamiento centralizado y descentralizado es acertada. Se mencionan beneficios clave como flexibilidad, reducción de latencia y resiliencia. Sin embargo, no se aborda adecuadamente:\n- La interacción específica entre las capas de acceso, transporte y core en este nuevo paradigma\n- La evolución de las interfaces entre componentes\n- El impacto en la topología de red física\n- La relación con tecnologías emergentes como Open RAN\n\n3. Mecanismos de IA para orquestación:\nSe mencionan varios mecanismos relevantes como predicción de carga, ubicación óptima de funciones, healing automático, optimización energética y gestión dinámica de SLAs. Esta sección es la más completa, aunque podría haberse beneficiado de:\n- Ejemplos de algoritmos específicos para cada caso de uso\n- Indicadores de rendimiento para evaluar la efectividad de estos mecanismos\n- Consideraciones sobre el entrenamiento y actualización de los modelos\n\n4. Complejidades de gestión de entornos híbridos:\nEl experto identifica correctamente los desafíos principales: coexistencia de diferentes infraestructuras, fragmentación tecnológica, diferentes ciclos de vida, seguridad, redundancia e interoperabilidad. Se destaca apropiadamente el cambio cultural y organizativo como factor crítico. Sin embargo, no se menciona suficientemente:\n- Estrategias de migración gradual de sistemas legados\n- Desafíos de observabilidad unificada en entornos híbridos\n- Implicaciones económicas de mantener sistemas paralelos\n- Desafíos en la gestión de APIs entre sistemas heterogéneos\n\nEn conclusión, la respuesta cubre los cuatro criterios solicitados, pero con distintos niveles de profundidad. Es particularmente sólida en mecanismos de IA para orquestación y complejidades de gestión, mientras que podría mejorar en la explicación técnica de VNF vs CNF y en detalles arquitectónicos de la integración Cloud/Edge con redes Telco.",
                "Creo que sería valioso profundizar en los mecanismos específicos de migración gradual desde infraestructuras tradicionales a entornos cloud-native en telecomunicaciones, así como en los desafíos de integración multi-vendor."
            ],
            "Facilitador de la Conversación": [
                "Bienvenidos a esta conversación sobre Network Slicing en 5G y el papel de la IA en su gestión. Como facilitador, me gustaría que comencemos con nuestro Experto en Telecomunicaciones explicando el concepto básico de Network Slicing y cómo la IA podría gestionar su ciclo de vida, especialmente para aplicaciones V2X. Después, nuestro Crítico podrá analizar esta respuesta según los criterios establecidos. ¿Podemos comenzar?",
                "Gracias por estas explicaciones detalladas. Para avanzar en la conversación y profundizar en algunos aspectos, ¿podría nuestro Experto abordar específicamente los desafíos técnicos de implementar la seguridad entre slices? Y al Crítico, ¿consideraría que se han cubierto adecuadamente los aspectos relacionados con los parámetros específicos que deben monitorizarse para aplicaciones V2X?",
                "Excelentes aportaciones. Para cerrar esta conversación, me gustaría pedir tanto al Experto como al Crítico que resumieran los puntos clave sobre cómo la IA puede contribuir a la optimización dinámica de slices para aplicaciones V2X, destacando tanto las oportunidades como las limitaciones actuales. ¿Podemos concluir con estas reflexiones finales?"
            ]
        }
        self.response_index = {}
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a mock response based on the role"""
        role = kwargs.get("role", "Facilitador de la Conversación")
        
        if role not in self.response_index:
            self.response_index[role] = 0
        
        if role not in self.responses:
            return "Lo siento, no tengo una respuesta para este rol."
        
        if self.response_index[role] >= len(self.responses[role]):
            # Cycle back to the first response if we've used all of them
            self.response_index[role] = 0
        
        response = self.responses[role][self.response_index[role]]
        self.response_index[role] += 1
        
        return response

class DeepseekModel(ModelInterface):
    """Interface for Deepseek model"""
    
    def __init__(self, model_name: str = "deepseek-ai/deepseek-coder-1.3b-instruct", 
                 load_in_8bit: bool = False, 
                 device_map: str = "auto"):
        """
        Initialize the Deepseek model
        
        Args:
            model_name: Name or path of the model
            load_in_8bit: Whether to load the model in 8-bit precision
            device_map: Device mapping strategy
        """
        super().__init__()
        
        if not HF_AVAILABLE:
            raise ImportError("transformers and torch are required to use DeepseekModel")
        
        logger.info(f"Loading model {model_name}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        model_kwargs = {"device_map": device_map}
        if load_in_8bit:
            model_kwargs["load_in_8bit"] = True
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            **model_kwargs
        )
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.1
        )
        
        logger.info("Model loaded successfully")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using the Deepseek model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional arguments for generation
        
        Returns:
            The generated response
        """
        role = kwargs.get("role", None)
        
        if role:
            # If a role is provided, format the prompt accordingly
            full_prompt = f"You are acting as {role}. {prompt}"
        else:
            full_prompt = prompt
        
        max_new_tokens = kwargs.get("max_new_tokens", 512)
        temperature = kwargs.get("temperature", 0.7)
        
        # Update generation parameters if provided
        generation_kwargs = {}
        if max_new_tokens != self.pipe.model.generation_config.max_new_tokens:
            generation_kwargs["max_new_tokens"] = max_new_tokens
        if temperature != self.pipe.model.generation_config.temperature:
            generation_kwargs["temperature"] = temperature
        
        # Generate response
        output = self.pipe(full_prompt, **generation_kwargs)
        response = output[0]["generated_text"]
        
        # Remove the prompt from the response if it's included
        if response.startswith(full_prompt):
            response = response[len(full_prompt):].strip()
        
        return response

class OllamaModel(ModelInterface):
    """Ollama API model implementation"""
    
    def __init__(self, model_name: str = "deepseek-coder:33b", api_base: str = "http://localhost:11434"):
        """
        Initialize Ollama model
        
        Args:
            model_name: Name of the model in Ollama
            api_base: Base URL for the Ollama API
        """
        self.model_name = model_name
        self.api_base = api_base
        logger.info(f"Initialized Ollama model: {model_name}")
    
    def generate(self, prompt: str, role: str = "Assistant", max_tokens: int = 1000) -> str:
        """
        Generate text using Ollama API
        
        Args:
            prompt: The prompt to generate text from
            role: The role the model should assume
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            The generated text
        """
        # Asegurar que las respuestas estén en español y sin proceso de pensamiento
        prompt_es = "INSTRUCCIÓN: RESPONDE COMPLETAMENTE EN ESPAÑOL. NO INCLUYAS PROCESO DE PENSAMIENTO, NI ETIQUETAS <think>. PROPORCIONA SOLO LA RESPUESTA FINAL DIRECTA.\n\n" + prompt
        system_prompt = f"Eres un {role}. Proporciona una respuesta detallada e informativa COMPLETAMENTE EN ESPAÑOL, sin proceso de pensamiento ni reflexiones previas."
        
        try:
            url = f"{self.api_base}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt_es,
                "system": system_prompt,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            logger.info(f"Sending request to Ollama API for model: {self.model_name}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result["response"]
            
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}")
            return f"Error: No se pudo generar la respuesta usando Ollama. {str(e)}"

def get_model(model_name: str, model_variant: str = None) -> ModelInterface:
    """
    Get a model interface based on the model name
    
    Args:
        model_name: Name of the model to use
        model_variant: Optional variant of the model (e.g., "32b")
    
    Returns:
        A model interface
    """
    return OllamaModel(model_name="deepseek-r1:32b")

    if model_name == "deepseek-r1":
        # Use Ollama for deepseek models
        ollama_model = "deepseek-coder:33b"  # Default to 33b
        
        if model_variant == "32b":
            ollama_model = "deepseek-coder:33b"
        
        return OllamaModel(model_name=ollama_model)
    elif model_name == "mock":
        return MockModel()
    else:
        logger.warning(f"Unknown model: {model_name}. Using mock model instead.")
        return MockModel() 