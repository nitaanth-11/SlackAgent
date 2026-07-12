# OpsPilot

> AI-powered incident management that keeps engineers inside Slack from alert to resolution.

OpsPilot is a Slack-native incident operations assistant that helps engineering teams triage, enrich, coordinate, and resolve incidents without leaving Slack.

## Why OpsPilot?

OpsPilot keeps the entire incident response lifecycle inside Slack. Instead of switching between dashboards, documentation, and communication tools, engineers receive AI-enriched context, collaborate with teammates, assign ownership, share updates, and resolve incidents from a single workspace.

## Architecture

> Slack Alert → FastAPI → AI Enrichment → Supabase → Slack Actions → Incident Resolution

## Problem Statement

Incident response is often hindered by tool fragmentation. On-call engineers lose critical time to context switching, leading to slow incident triage and delayed stakeholder communication. When knowledge is scattered across different monitoring systems, dashboards, and wikis, resolving an issue becomes significantly harder than it should be.

## Solution Overview

OpsPilot solves this by bringing the incident directly to the engineer. While AI context enrichment is a powerful component, it is only one part of the complete lifecycle. The full workflow ensures end-to-end visibility:
**Alert → AI Enrichment → Slack Collaboration → Ownership → Resolution**.

## Key Features

**Incident Ingestion**
- **Webhook Integration**: Receive structured JSON alerts from external monitoring tools to instantly initiate the incident workflow.

**AI Intelligence**
- **Automated Enrichment**: Analyzes raw alerts using LLMs to provide human-readable summaries, predict severity, and identify probable root causes.

**Slack Collaboration**
- **Interactive Block Kit**: Provides immediate, clickable actions in-channel to assign incident ownership, broadcast status updates, and mark incidents as resolved.

**Reliability**
- **Offline Resilience**: Queues incident creation requests locally, ensuring alerts are never dropped during temporary database or network outages.

## System Architecture

1. **Ingestion**: An external system sends an alert payload to the FastAPI webhook endpoint.
2. **Persistence**: The backend logs the raw incident securely into the Supabase database.
3. **Enrichment**: An AI provider analyzes the incident context and generates actionable insights.
4. **Delivery**: The Slack Bolt API constructs and pushes an interactive Block Kit message to the designated channel.
5. **Action**: Engineers use Slack buttons to update the incident state (e.g., assigning owners), which syncs back to the database.

## Tech Stack

- **Backend**: FastAPI, Python
- **Database**: Supabase
- **AI**: Ollama, OpenAI, Anthropic, Groq
- **Validation**: Pydantic
- **Collaboration**: Slack Bolt API

## Project Structure

```text
.
├── backend/
│   ├── ai/              # AI pipeline, mock providers, and LLM configuration
│   ├── api/             # FastAPI webhook and incident routes
│   ├── database/        # Database connection setup
│   ├── schemas/         # Pydantic models for validation
│   ├── services/        # Business logic for incidents and Slack messaging
│   ├── slack/           # Slack Bolt setup, actions, commands, and events
│   ├── app.py           # Main FastAPI application entry point
│   ├── config.py        # Environment configuration loader
│   └── requirements.txt # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Start the backend server:
```bash
python backend/app.py
```

## Environment Variables Required

| Variable | Purpose |
| --- | --- |
| `SLACK_BOT_TOKEN` | Authenticates the bot with the Slack API. |
| `SLACK_APP_TOKEN` | Enables Socket Mode for the Slack integration. |
| `SLACK_SIGNING_SECRET` | Verifies incoming webhook requests from Slack. |
| `DEFAULT_SLACK_CHANNEL` | Determines the channel where incidents are posted. |
| `SUPABASE_URL` | The endpoint for your Supabase database instance. |
| `SUPABASE_SERVICE_KEY` | Authenticates securely with Supabase for data access. |
| `OLLAMA_BASE_URL` | Points to a local or remote Ollama API for AI models. |
| `OPENAI_API_KEY` | Authenticates with the OpenAI API for AI models. |
| `ANTHROPIC_API_KEY` | Authenticates with the Anthropic API for AI models. |
| `GROQ_API_KEY` | Authenticates with the Groq API for AI models. |

## Demo Workflow

1. Send a test POST request to `/api/webhook/alert` containing incident details.
2. View the automatically generated, AI-enriched incident card in the designated Slack channel.
3. Click "Assign Owner" to claim responsibility for the incident.
4. Click "Generate Update" to post an automated status thread for stakeholders.
5. Click "Resolve" when the issue is mitigated to log the resolution time and close the incident.

## Repository Highlights

- **Modular backend architecture** separates Slack, AI, database, and business logic.
- **AI provider abstraction** allows multiple LLM providers with minimal changes.
- **Slack-native workflow** keeps engineers focused and reduces context switching.
- **Offline resilience** ensures no alerts are dropped during temporary database or network outages.
- **Production-oriented error handling** prevents silent failures and provides clear UI feedback.
- **Clean separation of services** makes the codebase easy to navigate, test, and extend.

## Future Improvements

- Better AI reasoning
- Historical incident analytics
- Team collaboration improvements
- Additional notification channels
- Better incident search
- Smarter runbook retrieval

## License

This project was developed as part of the Slack Agent Builder Hackathon.

## Team

- [Name 1] - [Role]
- [Name 2] - [Role]
