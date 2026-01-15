from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class Finding(BaseModel):
    title: str
    detail: str
    severity: Literal["low", "medium", "high"]
    quote: Optional[str] = Field(None, description="Extrait court du contrat (si disponible)")
    location_hint: Optional[str] = Field(None, description="Ex: 'Section 4.2' ou 'page 3'")

class AgentReport(BaseModel):
    agent_name: str
    summary: str
    findings: List[Finding]
    recommendations: List[str]

class ConsolidatedReport(BaseModel):
    contract_summary: str
    key_risks: List[Finding]
    negotiation_plan: List[str]
    suggested_redlines: List[str]
    trace: List[AgentReport]  # <-- traçabilité: outputs bruts des 3 agents
