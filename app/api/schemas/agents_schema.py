from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    response: str
