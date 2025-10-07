from langchain.agents import create_agent

from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template


booking_node = create_agent(
    model="anthropic:claude-opus-4-1-20250805",
    tools=tools,
    system_prompt=prompt_template.format(),
)
