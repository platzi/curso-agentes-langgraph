# My Agent Project - Curso Platzi LangGraph

## 🚀 Setup del Proyecto

### Windows CMD (Manual)
```sh
# Crear proyecto y entorno en D:\Langgraph\Curso Platzi\my_course_agent
python -m venv .venv

# Activar entorno en Windows
.venv\Scripts\activate

# Verificar que apunte al entorno virtual
where python

# Instalar dependencias para Gemini y Gemma 4
pip install -U langgraph langchain langchain-ollama langchain-google-genai
pip install "langgraph-cli[inmem]"

# Ejecutar el agente en modo dev
langgraph dev

# Instalar uv e inicializar
curl -LsSf https://astral.sh | sh
uv init
uv venv

# Agregar dependencias necesarias
uv add --pre langgraph langchain-ollama langchain-google-genai
uv add "fastapi[standard]"

# Agregar herramientas de desarrollo
uv add "langgraph-cli[inmem]" ipykernel grandalf --dev

# Ejecutar
uv run langgraph dev

import os
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuración API Cloud (Obtenida en Google AI Studio)
os.environ["GOOGLE_API_KEY"] = "TU_API_KEY_AQUI"

# OPCIÓN A: Gemma 4 (Local vía Docker/Ollama)
# Nota: Los modelos residen en E:\Docker\ollama_data
llm_local = ChatOllama(model="gemma4", temperature=0)

# OPCIÓN B: Gemini 1.5 Flash (API)
llm_cloud = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Selección de modelo para los templates
model = llm_local 

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = ChatOllama(model="gemma4", temperature=0)
agent = create_react_agent(model, tools=[get_weather])

# Ejecución
# inputs = {"messages": [("user", "what is the weather in sf")]}
# response = agent.invoke(inputs)

from langgraph.graph import MessagesState, StateGraph, START, END

class State(MessagesState):
    nodes: list[str]

def orchestrator(state: State): return state
def node_1(state: State): return state
def aggregator(state: State): return state

builder = StateGraph(State)
builder.add_node('orchestrator', orchestrator)
builder.add_node('node_1', node_1)
builder.add_node('aggregator', aggregator)

builder.add_edge(START, 'orchestrator')
builder.add_edge('orchestrator', 'node_1')
builder.add_edge('node_1', 'aggregator')
builder.add_edge('aggregator', END)
agent = builder.compile()

from langgraph.graph import MessagesState, StateGraph, START, END

class State(MessagesState):
    nodes: list[str]

def generator_node(state: State): return state
def evaluator_node(state: State): return state

builder = StateGraph(State)
builder.add_node('generator_node', generator_node)
builder.add_node('evaluator_node', evaluator_node)

builder.add_edge(START, 'generator_node')
builder.add_edge('generator_node', 'evaluator_node')
builder.add_edge('evaluator_node', END)
agent = builder.compile()
