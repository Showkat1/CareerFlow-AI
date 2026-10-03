# CareerFlow AI
### The Multi-Agent Career Operating System

**Discover. Match. Apply. Prepare. Improve.**

CareerFlow AI is an AI-powered career management platform designed to help job seekers organize and streamline their job search using specialized AI agents. It brings together resume intelligence, job discovery, job matching, application preparation, interview preparation, and career development in a unified Streamlit application.

## Key Features

- **Resume Intelligence:** Upload and analyze your resume to extract relevant career information and assess your profile.
- **Job Discovery:** Discover job opportunities using live job-source integrations, including Adzuna.
- **Intelligent Job Matching:** Analyze job opportunities against your career profile and identify relevant matches.
- **Application Preparation:** Organize opportunities and prepare application materials.
- **Interview Preparation:** Access interview preparation support based on job opportunities and career information.
- **Career Intelligence:** Get career-related insights and guidance.
- **Learning Support:** Explore learning and skill-development opportunities.
- **Mission Control:** Coordinate specialized agents through a shared mission context.
- **Application Management:** Organize your application pipeline and track application statuses.
- **Analytics and Dashboard:** View career-search activity, matches, application progress, and other relevant information.

## Multi-Agent Architecture

CareerFlow AI uses a modular agent architecture in which specialized agents handle distinct career-related tasks.

| Agent | Responsibility |
|---|---|
| Resume Intelligence Agent | Resume analysis and career profile insights |
| Job Discovery Agent | Job opportunity discovery |
| Matching Agent | Job and candidate profile matching |
| Application Agent | Application preparation |
| Interview Agent | Interview preparation |
| Learning Agent | Learning and skill development |
| Career Intelligence Agent | Career-related insights |

The core orchestration layer coordinates agents and manages shared mission context.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend and UI | Streamlit |
| Programming Language | Python |
| AI Model Integration | Groq |
| Language Model | Configured Groq-supported model |
| Database | SQLite |
| Job Discovery | Adzuna API integration |
| Resume Processing | Python-based resume parsing |
| Architecture | Modular multi-agent system |
| Version Control | Git and GitHub |

## Project Structure

```text
CareerFlow-AI/
├── agents/
│   ├── application_agent.py
│   ├── career_intelligence_agent.py
│   ├── interview_agent.py
│   ├── job_search_agent.py
│   ├── learning_agent.py
│   ├── matching_agent.py
│   └── resume_agent.py
├── core/
│   ├── agent_base.py
│   ├── agent_registry.py
│   ├── mission.py
│   ├── orchestrator.py
│   └── shared_context.py
├── database/
│   └── db.py
├── locations/
│   ├── location_data.py
│   └── location_selector.py
├── services/
│   ├── adzuna_client.py
│   ├── ai_service.py
│   ├── job_source.py
│   └── resume_parser.py
├── ui/
│   ├── components.py
│   └── theme.py
├── views/
│   ├── agent_activity.py
│   ├── analytics.py
│   ├── applications.py
│   ├── career.py
│   ├── dashboard.py
│   ├── interview.py
│   ├── jobs.py
│   ├── matches.py
│   ├── mission.py
│   ├── resume.py
│   ├── scores.py
│   └── settings.py
├── app.py
├── requirements.txt
├── test_adzuna.py
├── test_location.py
├── test_ui.py
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.11 or later (use a Python version compatible with the dependencies in `requirements.txt`)
- pip
- Git
- API credentials for the AI model provider
- Adzuna API credentials for live job discovery

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CareerFlow-AI.git
cd CareerFlow-AI
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository URL if needed.

### 2. Create a Virtual Environment

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux or macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the credentials required by your application.

Example:

```env
GROQ_API_KEY=your_groq_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

These are illustrative variable names. Confirm the exact names expected by your current implementation in `services/ai_service.py`, `services/adzuna_client.py`, and related configuration code before using this example.

**Security:** Never commit your `.env` file, API keys, passwords, or other secrets to GitHub.

### 5. Run the Application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your browser to access CareerFlow AI.

## Testing

The repository includes test files for selected application components.

Run the tests with:

```bash
python -m pytest
```

If `pytest` is not installed and is not included in your dependencies:

```bash
pip install pytest
```

The tests available in the repository cover selected areas. A successful test run does not necessarily verify every agent, integration, or end-to-end workflow.

## Configuration and Security

- Store API credentials in environment variables or an appropriate secrets manager.
- Keep `.env`, local databases, virtual environments, and private configuration files out of version control.
- Use restricted API credentials and rotate any credentials that may have been exposed.
- Review external API quotas and usage limits.
- Avoid placing personal resume data or sensitive application information in public repositories or logs.

## Current Project Scope

CareerFlow AI is developed as a modular, AI-assisted career management platform.

The repository includes its core application, specialized agent modules, database layer, job-source integration, UI components, and selected tests.

Feature availability and reliability may vary depending on configuration, API access, data availability, and the current implementation. Some agent capabilities and integrations may require further validation before production use.

## Future Enhancements

Potential areas for further development include:

- Expanded job-source integrations
- More advanced resume-to-job matching
- Improved application workflow automation
- Enhanced interview simulation
- Personalized learning roadmaps
- More comprehensive analytics
- Deployment and production-readiness improvements
- Stronger testing, monitoring, and observability

## Contributing

Contributions, feedback, and ideas are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request with a clear description.

## License

A license has not yet been specified. Add a license file before presenting the repository as open source or defining reuse permissions.

## Acknowledgments

CareerFlow AI is an independent AI-powered career platform project exploring multi-agent orchestration, intelligent job discovery, and AI-assisted career workflows.

**CareerFlow AI — Discover. Match. Apply. Prepare. Improve.**
