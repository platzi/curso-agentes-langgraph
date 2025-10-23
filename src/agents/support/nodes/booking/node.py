from langchain.agents import create_agent

from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template


booking_node = create_agent(
    model="ollama:llama3.1",
    tools=tools,
    prompt=prompt_template.format(),
)
