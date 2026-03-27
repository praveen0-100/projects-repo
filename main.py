from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from researcher import Researcher

app = FastAPI(title="Endless Research Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

researcher = Researcher()


class ResearchRequest(BaseModel):
    topic: str
    iterations: int = 3
    sources: List[str] = ["DuckDuckGo", "Wikipedia"]


@app.get("/")
def root():
    return {"status": "Endless Research Agent API running"}


@app.post("/research")
def do_research(req: ResearchRequest):
    """
    Performs live web research:
      1. Searches DuckDuckGo for the topic
      2. Scrapes each result page for real content
      3. Extracts a summary from the scraped text
      4. Returns all data to the frontend
    """
    results = researcher.research(
        topic=req.topic,
        sources=req.sources,
        max_results=max(req.iterations, 3),
    )
    return {
        "topic": req.topic,
        "sources_used": req.sources,
        "total": len(results),
        "results": results,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
