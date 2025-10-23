from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:llama3.1",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
