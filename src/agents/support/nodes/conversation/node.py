from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.tools import tools
from agents.support.nodes.conversation.prompt import prompt_template
from langchain_core.messages import AIMessage

llm = init_chat_model("ollama:llama3.1", temperature=1)
llm = llm.bind_tools(tools)

def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]
    customer_name = state.get("customer_name", 'John Doe')
    prompt = prompt_template.format(name=customer_name)
    print('*'*100)
    print(last_message.text)
    ai_message = llm.invoke([("system", prompt), ("user", last_message.text)])
    ai_message = AIMessage(content=ai_message.text)
    new_state["messages"] = [ai_message]
    return new_state