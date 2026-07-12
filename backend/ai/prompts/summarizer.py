SYSTEM_PROMPT = """
You are an expert Site Reliability Engineer (SRE).

Analyze software incidents accurately.

Do not invent facts.
Only use the information provided.

Return the answer in plain English.

Keep every section short.
"""


def build_summary_prompt(title: str, description: str, service: str) -> str:
    return f"""
Incident Title:
{title}

Service:
{service}

Description:
{description}

Analyze this incident and provide:

Summary:
(1-2 sentences)

Possible Root Cause:
(1-2 bullet points)

Recommended Actions:
(3 short bullet points)

Confidence:
(High / Medium / Low)
"""