from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import creer_agent

load_dotenv()

app = FastAPI(title="Agent Financier API")

agent = creer_agent()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    reponse: str
    statut: str

@app.get("/")
def root():
    return {"message": "Agent Financier API", "statut": "actif"}

@app.post("/api/agent/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    try:
        result = agent.invoke({"input": request.question})
        return QueryResponse(
            question=request.question,
            reponse=result["output"],
            statut="OK"
        )
    except Exception as e:
        return QueryResponse(
            question=request.question,
            reponse=str(e),
            statut="KO"
        )