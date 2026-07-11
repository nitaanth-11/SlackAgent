SYSTEM_PROMPT = """
You are an expert Site Reliability Engineer (SRE).

Your job is to analyze software incidents.

Be concise.
Do not hallucinate.
Only use information provided.

Return a short executive summary.
"""


def build_summary_prompt(title: str, description: str, service: str) -> str:
    return f"""
Incident Title:
{title}

Service:
{service}

Description:
{description}

Generate a concise incident summary.
"""