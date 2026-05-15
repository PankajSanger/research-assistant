from langgraph.graph import START,END,StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict

#loading .env 
load_dotenv()

#state
class ChatState(TypedDict):

    messages:str

llm = ChatOpenAI(model='gpt-5')


#chatnode
def ChatNode(state:ChatState):

    message = state['messages']
    response = llm.invoke(message)

    return {'messages':response}


#creating graph
graph = StateGraph(ChatState)

checkpointer = InMemorySaver()

graph.add_node('chatnode',ChatNode)

graph.add_edge(START,'chatnode')

chatbot = graph.compile(checkpointer=checkpointer)