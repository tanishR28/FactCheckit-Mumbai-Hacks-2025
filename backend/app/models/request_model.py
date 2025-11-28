from pydantic import BaseModel, Field

class VerifyRequest(BaseModel):
    claim: str = Field(..., min_length=10, max_length=1000, description="The claim or news headline to verify")
    
    class Config:
        json_schema_extra = {
            "example": {
                "claim": "Scientists have discovered a cure for all types of cancer in 2025"
            }
        }
