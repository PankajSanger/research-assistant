from langgraph.graph import START,END,StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_core.tools import tool   
from langgraph.prebuilt import ToolNode,tools_condition
from mcp_server import multiply,youtube

#loading .env 
load_dotenv()

#state
class ChatState(TypedDict):

    messages:Annotated[list,add_messages]

llm = ChatOpenAI(model='gpt-5')


#tool creation
@tool
def addition(first:int,second:int) -> int :
    """
    add two numbers.
    """
    return first+second

tools = [addition,multiply,youtube]

#tool binding
llm_with_tool = llm.bind_tools(tools)


#chatnode
def ChatNode(state:ChatState):
    "LLM node that may answer or request a tool call."
    message = state['messages']
    response = llm_with_tool.invoke(message)

    return {'messages':[response]}

#tool node
tool_node = ToolNode(tools)

#creating graph
graph = StateGraph(ChatState)

checkpointer = InMemorySaver()

graph.add_node('chatnode',ChatNode)
graph.add_node('tools',tool_node)


graph.add_edge(START,'chatnode')
graph.add_conditional_edges('chatnode',tools_condition)

chatbot = graph.compile(checkpointer=checkpointer)

CONFIG = {'configurable':{'thread_id':'1'}}

while True:
    user_message = input("Ask Anything : ")
    if user_message == 'exit' or user_message=='bye' or user_message=='quit':
        break
    else:
        print("Human : ",user_message)
        response = chatbot.invoke({'messages':user_message},config=CONFIG)
        print("AI : ",response['messages'][-1].content)






