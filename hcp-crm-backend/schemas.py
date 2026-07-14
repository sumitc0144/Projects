from pydantic import BaseModel, Field
from typing import List, Optional

class InteractionExtractSchema(BaseModel):
    hcp_name: str = Field(description="Name of the healthcare professional/doctor.")
    interaction_type: str = Field(default="Meeting", description="Type of interaction, e.g., Meeting, Call, Email.")
    topics_discussed: Optional[str] = Field(None, description="Detailed topics and product efficacy points discussed.")
    materials_shared: List[str] = Field(default=[], description="Names of brochures or digital materials provided.")
    samples_distributed: List[str] = Field(default=[], description="Names of medical product samples handed over.")
    sentiment: str = Field(default="Neutral", description="Inferred sentiment: Positive, Neutral, or Negative.")
    outcomes: Optional[str] = Field(None, description="Key conclusions or clinical agreements reached.")
    follow_up_actions: Optional[str] = Field(None, description="Next actionable steps.")