from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_graph import compiled_graph
from langchain_core.messages import HumanMessage
import logging

app = FastAPI(title="AI-First CRM Module Gateway")

# Enable CORS safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatPayload(BaseModel):
    message: str

@app.post("/api/interact")
async def process_interaction(payload: ChatPayload):
    try:
        inputs = {"messages": [HumanMessage(content=payload.message)]}
        config = {"configurable": {"thread_id": "session_1"}}
        
        # Invoke the LangGraph compiled state machine
        output_state = compiled_graph.invoke(inputs, config=config)
        
        # Safely extract the last message content
        if "messages" in output_state and len(output_state["messages"]) > 0:
            final_response = output_state["messages"][-1].content
            return {"reply": final_response}
        else:
            return {"reply": "Interaction processed, but no text response was generated."}
            
    except Exception as e:
        print(f"EXCEPTION OCCURRED: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)