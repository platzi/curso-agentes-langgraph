## Create a new project

```sh
# Install python3 and create a new project.

python3 --version
mkdir my_agent
cd my_agent
python3 -m venv .venv
source .venv/bin/activate
which python
# install langgraph and langchain

pip install --pre langgraph langchain langchain-ollama
pip install "langgraph-cli[inmem]"

# run the agent
langgraph dev
```

### Env with UV

```sh
# Install uv

curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# deactivate the virtual environment
deactivate
rm -rf .venv

## init
uv init
uv venv

# add dependencies
uv add --pre langgraph langchain langchain-ollama
uv add "fastapi[standard]"

# add dev dependencies
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel --dev
uv add grandalf --dev

# run the agent
uv run langgraph dev



# install the project
uv pip install -e .
```

```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]
```

- https://mermaidviewer.com/editor


### Orchestrator Template

<details>
<summary>Template</summary>

```py
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from typing import Literal

class State(MessagesState):
    nodes: list[str]


def orchestrator(state: State):
    return state


def node_1(state: State):
    return state


def node_2(state: State):
    return state


def node_3(state: State):
    return state


def aggregator(state: State):
    return state


builder = StateGraph(State)

builder.add_node('orchestrator', orchestrator)
builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)
builder.add_node('aggregator', aggregator)

builder.add_edge(START, 'orchestrator')
builder.add_edge('orchestrator', 'node_1')
builder.add_edge('orchestrator', 'node_2')
builder.add_edge('orchestrator', 'node_3')
builder.add_edge('node_1', 'aggregator')
builder.add_edge('node_2', 'aggregator')
builder.add_edge('node_3', 'aggregator')
builder.add_edge('aggregator', END)
agent = builder.compile()

```

</details>






### Evaluator Template

<details>
<summary>Template</summary>

```py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
import random

class State(TypedDict):
    nodes: list[str]

class State(MessagesState):
    nodes: list[str]


def generator_node(state: State):
    return state


def evaluator_node(state: State):
    return state


builder = StateGraph(State)

builder.add_node('generator_node', generator_node)
builder.add_node('evaluator_node', evaluator_node)

builder.add_edge(START, 'generator_node')
builder.add_edge('generator_node', 'evaluator_node')
builder.add_edge('evaluator_node', END)
agent = builder.compile()
```
</details>

### Fast API Checkpoint

<details>
<summary>Template</summary>

```py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Depends
from typing import Annotated

from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = os.getenv("DB_URI")

# Global checkpointer instance
_checkpointer: PostgresSaver | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _checkpointer
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        _checkpointer = checkpointer
        _checkpointer.setup()
        yield

def get_checkpointer() -> PostgresSaver:
    if _checkpointer is None:
        raise RuntimeError("Checkpointer not initialized. Make sure lifespan is running.")
    return _checkpointer

CheckpointerDep = Annotated[PostgresSaver, Depends(get_checkpointer)]
```
</details>