from __future__ import annotations

from copy import deepcopy
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from graph import graph


class AgentRunRequest(BaseModel):
    task_informations: dict[str, Any]
    task: list[dict[str, Any]]
    settings: dict[str, Any]
    recursion_limit: int = Field(default=1000, ge=1, le=100000)


class AgentRunResponse(BaseModel):
    success: bool
    result: dict[str, Any]


app = FastAPI(
    title="Auto PR Chat Agent API",
    version="0.1.0",
    description="Wraps the LangGraph AI Agent as HTTP APIs.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/agent/run", response_model=AgentRunResponse)
def run_agent(payload: AgentRunRequest) -> AgentRunResponse:
    state = {
        "task_informations": deepcopy(payload.task_informations),
        "task": deepcopy(payload.task),
        "settings": deepcopy(payload.settings),
    }

    try:
        result = graph.invoke(state, {"recursion_limit": payload.recursion_limit})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent invoke failed: {exc}") from exc

    return AgentRunResponse(success=True, result=result)
