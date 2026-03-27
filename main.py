from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from researcher import Researcher
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

researcher = Researcher()

class ResearchRequest(BaseModel):
    topic: str
    iterations: int = 3
    sources: List[str] = ["DuckDuckGo", "Wikipedia"]

@app.get("/")
def read_root():
    return {"message": "Endless Research Agent API is running."}

@app.post("/research")
async def research(req: ResearchRequest):
    """Perform actual research by searching and scraping."""
    # To simulate iterations, for now we can call once and return more results, 
    # or loop and fetch more topics based on findings. 
    # For a start, let's fetch results related to the topic.
    
    results = researcher.research_topic(req.topic, sources=req.sources)
    return {
        "topic": req.topic,
        "iterations": req.iterations,
        "results": results,
        "summary": "Synthesized results from real-world search and content extraction."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
