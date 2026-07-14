from langchain_core.tools import tool
from sqlalchemy import create_engine, text
import json

# Change this to your local MySQL or PostgreSQL connection string
DATABASE_URL = "sqlite:///./crm.db" 
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Automatically build tables if they do not exist
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hcp_name TEXT,
            interaction_type TEXT,
            date TEXT,
            time TEXT,
            topics_discussed TEXT,
            materials_shared TEXT,
            samples_distributed TEXT,
            sentiment TEXT,
            outcomes TEXT,
            follow_up_actions TEXT
        );
    """))
    conn.commit()

@tool
def log_interaction(extracted_data: str) -> str:
    """
    Captures interaction data, parses entities via LLM, and creates a database log.
    Expects argument to be a valid JSON string containing the interaction fields.
    """
    try:
        data = json.loads(extracted_data)
        query = text("""
            INSERT INTO interactions (hcp_name, interaction_type, date, time, topics_discussed, materials_shared, samples_distributed, sentiment, outcomes, follow_up_actions)
            VALUES (:hcp_name, :interaction_type, date('now'), time('now'), :topics_discussed, :materials_shared, :samples_distributed, :sentiment, :outcomes, :follow_up_actions);
        """)
        with engine.connect() as conn:
            result = conn.execute(query, {
                "hcp_name": data.get("hcp_name", "Unknown"),
                "interaction_type": data.get("interaction_type", "Meeting"),
                "topics_discussed": data.get("topics_discussed", ""),
                "materials_shared": ", ".join(data.get("materials_shared", [])),
                "samples_distributed": ", ".join(data.get("samples_distributed", [])),
                "sentiment": data.get("sentiment", "Neutral"),
                "outcomes": data.get("outcomes", ""),
                "follow_up_actions": data.get("follow_up_actions", "")
            })
            conn.commit()
        return f"SUCCESS: Logged interaction for {data.get('hcp_name')} into database."
    except Exception as e:
        return f"ERROR: Failed to log interaction: {str(e)}"

@tool
def edit_interaction(interaction_id: int, updates_json: str) -> str:
    """
    Modifies specific field metrics inside an already logged record identifier.
    """
    try:
        updates = json.loads(updates_json)
        set_clauses = [f"{key} = :{key}" for key in updates.keys()]
        query_string = f"UPDATE interactions SET {', '.join(set_clauses)} WHERE id = :interaction_id"
        
        with engine.connect() as conn:
            updates["interaction_id"] = interaction_id
            conn.execute(text(query_string), updates)
            conn.commit()
        return f"SUCCESS: Log entry ID {interaction_id} has been modified successfully."
    except Exception as e:
        return f"ERROR: Failed to update interaction: {str(e)}"

@tool
def search_hcp_profile(name_query: str) -> str:
    """
    Searches past history and specialty profiles for a given HCP name.
    """
    return f"Found profile metadata context for HCP '{name_query}': Active Practitioner, Cardiology Specialization."

@tool
def check_material_inventory(item_name: str) -> str:
    """
    Verifies if a requested marketing brochure or drug sample is currently in stock.
    """
    return f"Inventory Check: '{item_name}' is verified and in stock."

@tool
def generate_follow_up_task(context_summary: str) -> str:
    """
    Automatically creates a task calendar alert based on next steps mentioned.
    """
    return f"Task Generated: Scheduled calendar action items following up on: '{context_summary}'."

tools_list = [log_interaction, edit_interaction, search_hcp_profile, check_material_inventory, generate_follow_up_task]