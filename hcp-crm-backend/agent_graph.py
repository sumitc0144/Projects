import os
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from agent_tools import tools_list
llm = ChatGroq(model="gemma2-9b-it", groq_api_key="gsk_your_actual_groq_api_key_here", temperature=0.2)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Fallback System Prompt instructs the model to act conversational if no tool applies
llm = ChatGroq(model="gemma2-9b-it", groq_api_key="YOUR_GROQ_API_KEY", temperature=0.2)
llm_with_tools = llm.bind_tools(tools_list)

def call_model(state: AgentState):
    messages = state['messages']
    # If it's a generic prompt, give a life-science context prompt hint
    system_instruction = (
        "You are an AI assistant for a life science CRM. Help the representative log interactions, "
        "check inventory, search profiles, or update information. If they say hi, greet them back warmly."
    )
    # Inject system context subtly if needed, or simply invoke the model
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def execute_tools(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    tool_outputs = []
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            target_tool = next(t for t in tools_list if t.name == tool_name)
            output = target_tool.invoke(tool_args)
            tool_outputs.append(ToolMessage(content=str(output), tool_call_id=tool_call['id']))
    return {"messages": tool_outputs}

def route_next_step(state: AgentState):
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", execute_tools)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", route_next_step, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

compiled_graph = workflow.compile()