from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_graph import compiled_graph
from langchain_core.messages import HumanMessage
import json
import logging

app = FastAPI(title="AI-First CRM Module Gateway")

# Enable CORS safely for frontend communication
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
        # 1. Setup execution state parameters
        inputs = {"messages": [HumanMessage(content=payload.message)]}
        config = {"configurable": {"thread_id": "session_1"}}
        
        # 2. Invoke the LangGraph compiled state machine
        output_state = compiled_graph.invoke(inputs, config=config)
        
        # 🚨 DEBUG: Print the absolute raw graph state directly to your terminal console
        print("\n🔎 === RAW LANGGRAPH OUTPUT STATE START ===")
        print(output_state)
        print("=== RAW LANGGRAPH OUTPUT STATE END ===\n")
        
        # 3. Extract conversational text reply safely
        final_response = "Interaction processed successfully."
        if "messages" in output_state and len(output_state["messages"]) > 0:
            final_response = output_state["messages"][-1].content

        # 4. Smart Sentiment Extraction Pipeline
        sentiment = "Neutral"  # Default fallback
        extracted_fields = {}

        # Path A: Check if graph schema tracks 'sentiment' or 'form_data' at root level
        if "sentiment" in output_state and output_state["sentiment"]:
            sentiment = output_state["sentiment"]
        if "form_data" in output_state and isinstance(output_state["form_data"], dict):
            extracted_fields = output_state["form_data"]

        # Path B: Check if data is nested inside an internal 'state' dictionary slice
        if "state" in output_state and isinstance(output_state["state"], dict):
            internal_state = output_state["state"]
            if "sentiment" in internal_state:
                sentiment = internal_state["sentiment"]
            if "form_data" in internal_state:
                extracted_fields = internal_state["form_data"]

        # Path C: Check if the LLM returned a JSON string inside the message text itself
        if final_response.strip().startswith("{") and final_response.strip().endswith("}"):
            try:
                parsed_json = json.loads(final_response)
                if "sentiment" in parsed_json:
                    sentiment = parsed_json["sentiment"]
                if "reply" in parsed_json:
                    final_response = parsed_json["reply"]
                if "form_data" in parsed_json:
                    extracted_fields = parsed_json["form_data"]
            except Exception:
                pass  # String resembles JSON but failed parsing; fallback safely

        # 5. Print out cleaned values inside terminal for verification
        print("--- CLEANED PARSED ANALYSIS ---")
        print(f"Detected Sentiment : {sentiment}")
        print(f"Extracted Fields   : {extracted_fields}")
        print(f"Final Reply Text   : {final_response}")
        print("--------------------------------\n")

        # 6. Send payload back to React frontend UI
        return {
            "reply": final_response,
            "sentiment": str(sentiment).capitalize(),
            "form_data": extracted_fields
        }
            
    except Exception as e:
        print(f"EXCEPTION OCCURRED DURING APIS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Start app locally on port 8000 with auto-reload active
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)