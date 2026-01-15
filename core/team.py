from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat

from core.tools import ContractTools

MODEL_ID = "gpt-4o" 

contract_tools = ContractTools()

contract_structure_agent = Agent(
    id="contract-structure-agent",
    name="Contract Structure Agent",
    model=OpenAIChat(id=MODEL_ID),
    role="Analyze the contract structure and clause quality (scope, obligations, payment, SLA, liability, termination).",
    instructions=[
        "You are a contract structuring expert.",
        "You review how the contract is structured and organized.",
        "Work ONLY from the provided contract text.",
        "Identify missing sections, unclear organization, or inconsistent structure.",
        "Focus on: scope, obligations, payment, liability, termination, governing law.",
        "When relevant, quote short excerpts from the contract as evidence.",
        "Suggest practical improvements or missing sections.",
        "Do NOT provide legal advice.",
        "Return a concise Markdown output."
    ],
    tools=[contract_tools],
    markdown=True,
)

legal_framework_agent = Agent(
    id="legal-framework-agent",
    name="Legal Framework Agent",
    model=OpenAIChat(id=MODEL_ID),
    role="Analyze legal framework & compliance: governing law, confidentiality, data protection (DPA/GDPR), IP, liability limits, local regulatory concerns.",
    instructions=[
        "You identify potential legal or compliance issues in the contract.",
        "Work ONLY from the provided contract text.",
        "Focus on high-impact areas: governing law, confidentiality, data protection (GDPR/DPA), IP, liability, termination.",
        "When raising an issue, reference the relevant clause or say if it is missing.",
        "Use cautious language and avoid legal conclusions.",
        "Return a clear and concise Markdown summary."
    ],
    tools=[contract_tools],
    markdown=True,
)

negotiating_agent = Agent(
    id="negotiating-agent",
    name="Negotiating Agent",
    model=OpenAIChat(id=MODEL_ID),
    role="Build a negotiation strategy: redlines, concessions, opening positions, fallback options, alternative wording.",
    instructions=[
        "You identify clauses that are commonly negotiable or potentially unbalanced.",
        "Work ONLY from the provided contract text.",
        "For each point, explain briefly why it may be negotiable.",
        "Suggest a practical alternative or counter-proposal.",
        "Quote the clause when relevant.",
        "Keep suggestions concise and business-oriented.",
        "Return Markdown."
        "Return Markdown: Summary / Negotiation Plan / Redlines / Proposed Wording."
    ],
    tools=[contract_tools],
    markdown=True,
)

manager_team = Team(
    name="Contract Multi-Agent Team (Manager)",
    members=[contract_structure_agent, legal_framework_agent, negotiating_agent],
    model=OpenAIChat(id=MODEL_ID),
    instructions=(
        "You are the manager. Produce a client-ready contract review that clearly covers three lenses: "
        "Structure, Legal/Compliance, and Negotiation.\n"
        "Prioritize the USER GOAL if provided. Keep it concise, actionable, and professional.\n"
        "Do NOT include raw agent traces, internal reasoning, or intermediate outputs forcing the reader to parse.\n"
        "Do not invent clauses. If something is missing/unclear, say 'Not found' or 'Unclear from text'.\n"
        "For key claims, include a short exact quote as evidence.\n\n"
        "OUTPUT FORMAT (Markdown):\n"
        "# Executive Summary\n"
        "- 5–8 bullets: the most important risks + quick wins\n\n"
        "# 1) Structure Review\n"
        "- Main gaps (bullets)\n"
        "- Recommended improvements (bullets)\n\n"
        "# 2) Legal & Compliance Review\n"
        "- Top risks (bullets)\n"
        "- Missing/unclear clauses checklist (bullets)\n\n"
        "# 3) Negotiation Playbook\n"
        "- Top 3–5 negotiation points: Clause quote / Ask / Fallback / Suggested wording\n\n"
        "# Open Questions\n"
        "- 3–8 clarifying questions for the client\n\n"
        "# Disclaimer\n"
        "- Informational only; not legal advice.\n"
    ),
    markdown=True,
)

def run_contract_team(file_bytes: bytes, filename: str, user_goal: str = "") -> str:
    """
    Single entry point used by Streamlit / Telegram / WhatsApp.
    """
    # Robust approach: extract text server-side and pass the text to the team.
    contract_text = contract_tools.get_contract(file_bytes, filename)

    prompt = f"""
USER GOAL (optional):
{user_goal or "N/A"}

CONTRACT FILENAME: {filename}

CONTRACT TEXT:
{contract_text}

TASK:
- Produce a consolidated manager answer (structure + legal + negotiation).
"""
    result = manager_team.run(prompt)
    return result.content
