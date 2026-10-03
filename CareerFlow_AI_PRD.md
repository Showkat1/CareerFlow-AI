# Product Requirements Document (PRD)
## CareerFlow AI
**Product:** CareerFlow AI — The Multi-Agent Career Operating System  
**Tagline:** Discover. Match. Apply. Prepare. Improve.  
**Document version:** 1.0  
**Status:** Draft for product review  
**Date:** October 3, 2026

---

## 1. Product Overview

CareerFlow AI is a multi-agent career assistance application designed to help job seekers organize and manage key stages of their job search in one place. It combines resume intelligence, job discovery, job matching, application preparation, interview preparation, learning guidance, and career insights through a Streamlit interface and a shared career mission workflow.

The product is intended to support and accelerate a user's job-search activities. It does not independently guarantee employment, verify employer decisions, or submit applications to external job portals unless a separately implemented and authorized integration supports that action.

## 2. Problem Statement

Job seekers often work across disconnected tools and manually repeat tasks such as:
- Reviewing and improving a resume for different roles.
- Finding relevant job openings across sources.
- Comparing job descriptions with their experience and skills.
- Preparing application materials.
- Tracking application progress and upcoming stages.
- Preparing for interviews and identifying learning gaps.

This fragmented workflow can make it difficult to maintain a consistent view of progress and decide what to work on next.

## 3. Product Vision

Provide a unified, understandable career workspace in which specialized AI agents assist with distinct job-search tasks and coordinate through a shared mission context.

## 4. Goals and Success Measures

### Product goals
1. Bring core job-search activities into one application.
2. Help users understand how their resumes and profiles relate to job requirements.
3. Surface relevant job opportunities using live job data where configured.
4. Make application preparation and status tracking easier.
5. Present agent activity and progress in a clear, actionable interface.
6. Keep users in control of decisions and external submissions.

### Proposed success measures
These are product metrics to instrument and validate; targets should be set after baseline testing.
- Resume analysis completion rate.
- Number and percentage of discovered jobs with a completed match analysis.
- User-rated usefulness of job matches.
- Application packages created per active user.
- Percentage of tracked applications with a current status.
- Interview-preparation sessions completed.
- Task completion time and user-reported ease of use.
- Error rate for external job-data requests and AI generation.

## 5. Target Users

### Primary users
- Active job seekers who want a structured workflow.
- Professionals exploring a career move or a new role.
- Candidates who need help tailoring application materials.
- Users who want to track applications and prepare for interviews in one workspace.

### User needs
- Understand what roles fit their experience.
- Find opportunities without repeatedly searching manually.
- See why a role may or may not match their profile.
- Prepare role-specific application materials.
- Know the current state of each application.
- Identify useful next steps without losing control of decisions.

## 6. Scope

### In scope
- Resume upload and resume intelligence.
- Job discovery, including configured live job-source integration.
- Job matching and fit analysis.
- Application preparation and application queue.
- Application status tracking.
- Interview preparation.
- Learning recommendations or learning-gap guidance.
- Career intelligence and dashboard insights.
- Multi-agent orchestration and mission progress.
- Configuration and operational safeguards for AI and external APIs.

### Out of scope for the current release
- Guaranteed job placement or claims of guaranteed match accuracy.
- Automatic submission to third-party job portals.
- Employer-side recruiting and applicant tracking.
- Payment processing, subscriptions, or billing.
- A fully featured mobile-native application.
- Unverified integrations not present in the current implementation.
- Claims that all job listings are complete, current, or independently verified.

## 7. Core User Journeys

### Journey A: Start a career mission
1. User opens CareerFlow AI.
2. User reviews or enters career profile information.
3. User uploads or selects a resume.
4. User starts a career mission.
5. The orchestrator coordinates the available agents.
6. The interface displays each agent's status, outputs, and any errors.
7. User reviews results and chooses the next action.

### Journey B: Discover and evaluate jobs
1. User specifies role, location, and other available search criteria.
2. Job Discovery Agent retrieves jobs from configured sources or uses fallback data when necessary.
3. Matching Agent compares available jobs with the user's profile or resume information.
4. User reviews job details and match explanations.
5. User saves or moves relevant opportunities into the application workflow.

### Journey C: Prepare an application
1. User opens an opportunity from the queue.
2. User reviews the role and relevant profile information.
3. Application Agent generates or assists with a tailored resume version, cover letter, or answers where supported.
4. User edits and approves the materials.
5. User applies externally using the employer or job-board process.
6. User manually records the application as submitted in CareerFlow AI.

### Journey D: Track an application
1. User opens the application tracker.
2. User filters or searches applications.
3. User updates an application's status as it progresses.
4. The system records status changes and relevant timestamps where implemented.
5. User reviews the current pipeline and decides on follow-up actions.

### Journey E: Prepare for an interview or skill gap
1. User selects a role or application.
2. User opens interview preparation or learning guidance.
3. The relevant agent generates practice questions, guidance, or learning suggestions.
4. User reviews and uses the material.
5. User can return to the career workspace to continue the mission.

## 8. Functional Requirements

Priority definitions: **P0** = required for the current core workflow; **P1** = important enhancement; **P2** = later consideration. Priorities are proposed and should be confirmed against the implementation.

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-01 | Resume upload and access | P0 | User can provide a resume in supported formats; invalid or unsupported files produce a clear message. |
| FR-02 | Resume intelligence | P0 | The system extracts or analyzes available resume content and presents understandable results. |
| FR-03 | Job discovery | P0 | User can search using available criteria and view returned job records. |
| FR-04 | External job-source handling | P0 | Source errors and empty results are handled gracefully; fallback data is clearly identified as fallback/demo data. |
| FR-05 | Job matching | P0 | Jobs can be analyzed against candidate information; results include a score or explanation only where supported by the implementation. |
| FR-06 | Job detail review | P0 | User can inspect relevant job information and access an available external job link. |
| FR-07 | Application queue | P0 | Opportunities ready for application can be viewed separately from submitted/in-progress applications. |
| FR-08 | Application preparation | P0 | User can generate or review supported application materials and retain control over final content. |
| FR-09 | Manual application tracking | P0 | User can record that they applied and update a tracked application's status. The UI must not imply that CareerFlow AI submitted it externally. |
| FR-10 | Application status model | P0 | Supported statuses include READY_TO_APPLY, APPLIED, SCREENING, ASSESSMENT, INTERVIEW, OFFER, REJECTED, and WITHDRAWN, subject to implementation validation. |
| FR-11 | Application timestamps | P1 | The system records applied/updated timestamps consistently when status changes occur. |
| FR-12 | Interview preparation | P1 | User can access role-relevant interview practice or preparation content where the agent is configured. |
| FR-13 | Learning guidance | P1 | User can review learning suggestions or skill-gap guidance where available. |
| FR-14 | Career intelligence | P1 | User can view career insights based on available profile, job, and activity data. |
| FR-15 | Mission orchestration | P0 | The application displays which agents ran, their progress or state, and any failures. |
| FR-16 | Dashboard | P0 | The dashboard summarizes available career and application information without displaying misleading or stale values as current. |
| FR-17 | Search and filtering | P1 | Users can search or filter job and application lists using supported fields. |
| FR-18 | Configuration | P0 | Required API configuration is read from environment or secrets configuration, not hard-coded in source. |
| FR-19 | Error handling | P0 | AI-provider, network, data, and validation errors are surfaced in understandable language and do not silently corrupt workflow state. |
| FR-20 | User review and control | P0 | Generated materials and recommendations are presented for user review; external actions require user initiation. |

## 9. Application Lifecycle

The proposed application lifecycle is:

`READY_TO_APPLY → APPLIED → SCREENING → ASSESSMENT → INTERVIEW → OFFER`

Alternative terminal or user-controlled states:
- `REJECTED`
- `WITHDRAWN`

The application queue should show items in `READY_TO_APPLY`. The application tracker should show submitted or otherwise progressed items. Exact transition rules, whether backward transitions are allowed, and timestamp behavior must be confirmed in implementation and tested.

## 10. Agent Responsibilities

| Agent | Responsibility | Expected output |
|---|---|---|
| Resume Intelligence Agent | Analyze resume content and candidate information | Resume insights, skills, experience details, or score where implemented |
| Job Discovery Agent | Retrieve opportunities from configured job sources | Normalized job records |
| Matching Agent | Compare jobs with candidate profile | Match results and supporting rationale where implemented |
| Application Agent | Assist with role-specific application materials | Draft materials for user review |
| Interview Agent | Support interview preparation | Practice questions and preparation guidance |
| Learning Agent | Identify learning opportunities | Skill-gap or learning suggestions |
| Career Intelligence Agent | Synthesize career and job-search information | Career insights and next-step guidance |
| Career Orchestrator | Coordinate agents using shared mission context | Mission state, agent outputs, and error information |

Agent outputs should be traceable to the relevant input data where feasible. The interface should distinguish completed, pending, skipped, and failed steps.

## 11. UX and Interface Requirements

- Use a clear, professional, responsive layout.
- Keep primary navigation understandable and consistent.
- Separate the Application Queue from the Applications Tracker.
- Make mission progress and agent activity easy to scan.
- Use consistent terminology for jobs, matches, application materials, and statuses.
- Show loading, empty, success, and error states.
- Avoid presenting demo or fallback records as live listings.
- Provide clear next actions without forcing automatic actions.
- Support keyboard-accessible controls and readable contrast.
- Preserve user-entered information across normal navigation where supported.

## 12. Data Requirements

Core data entities expected in the current product include:
- Candidate profile.
- Resume and extracted resume information.
- Job records.
- Match results.
- Application records.
- Mission and agent execution state.
- Generated application materials.
- Interview and learning content, where persisted.

The current SQLite application schema includes an `applications` table with fields such as job ID, status, resume version, cover letter, application answers, notes, applied timestamp, and updated timestamp. The exact schema and persistence behavior should be verified against the working repository before treating this PRD as an implementation specification.

Data requirements:
- Use stable identifiers for records.
- Validate status values and required fields.
- Avoid storing API secrets in the database or repository.
- Define retention and deletion behavior before handling real user data at scale.
- Avoid exposing one user's records to another if multi-user support is introduced.

## 13. External Services and Dependencies

Known or previously used components:
- Streamlit for the web interface.
- Python for application and agent logic.
- Groq for language-model generation in the current development setup.
- SQLite for local persistence.
- Adzuna for live job discovery, where configured.

The exact model names, API variables, supported resume formats, rate limits, and external service terms should be verified from the current code and provider documentation. External service availability is not guaranteed by CareerFlow AI.

## 14. Non-Functional Requirements

### Performance
- Provide visible feedback during long-running AI and job-search operations.
- Avoid unnecessary repeated model calls.
- Paginate or limit large result sets where appropriate.
- Establish measurable response-time targets after baseline testing.

### Reliability
- Handle provider timeouts, rate limits, empty responses, and malformed outputs.
- Preserve existing records when a downstream agent fails.
- Make retries explicit and bounded where implemented.

### Security and privacy
- Keep secrets out of Git and source files.
- Use least-privilege credentials for external services.
- Validate uploaded files and user inputs.
- Avoid logging API keys, credentials, or unnecessary sensitive resume content.
- Document what data is sent to external AI and job-search providers.
- Define authentication, authorization, backup, and deletion requirements before production multi-user deployment.

### Accessibility and usability
- Use readable labels and consistent interaction patterns.
- Provide text alternatives for meaningful visual indicators.
- Ensure important actions are not conveyed by color alone.
- Test the interface at common desktop and mobile viewport sizes.

### Maintainability
- Keep agent responsibilities modular.
- Separate UI, orchestration, services, and persistence concerns.
- Add tests for status transitions, matching behavior, provider failures, and key user journeys.

## 15. Assumptions and Constraints

- The current product is a Streamlit application rather than a native mobile app.
- Some capabilities may be implemented as prototypes or may require configuration.
- Job availability and quality depend on external sources.
- AI-generated scores, summaries, and materials may be incomplete or inaccurate and require user review.
- The PRD describes intended product behavior; it is not proof that every requirement is already implemented.
- Current implementation and repository files take precedence when assessing what is already working.

## 16. Risks and Mitigations

| Risk | Potential impact | Mitigation |
|---|---|---|
| AI output is inaccurate or generic | Poor application materials or misleading guidance | Show drafts for review; support editing; communicate limitations. |
| Job data is stale, duplicated, or incomplete | Wasted time or missed opportunities | Display source and retrieval context where available; normalize and deduplicate records. |
| Provider quota or rate limits | Interrupted workflows | Handle errors clearly; bound retries; support provider configuration without exposing secrets. |
| Matching scores are misunderstood | Users over-rely on a numeric score | Explain factors and limitations; avoid implying guaranteed suitability. |
| Application status is mistaken for an external submission | Incorrect tracking | Label status changes as manual tracking and clearly distinguish external application actions. |
| Data or secrets are exposed | Privacy or account risk | Use secret management, input validation, safe logging, and repository checks. |
| Scope grows before release | Reduced testing and stability | Freeze feature scope for the current release and prioritize validation and demo readiness. |

## 17. Release and Acceptance Plan

### Current release focus
- Validate the end-to-end career mission.
- Confirm live job discovery and fallback labeling.
- Check matching outputs against a small set of known examples.
- Verify that queue and tracker are distinct and status changes persist.
- Test resume analysis and application-material generation.
- Test AI-provider and job-source failure states.
- Review UI navigation, empty states, and presentation flow.
- Confirm `.env`, database files, local data, and secrets are excluded from Git as appropriate.
- Prepare a repeatable demo scenario and document known limitations.

### Release acceptance checklist
- [ ] Application starts using documented setup instructions.
- [ ] Required configuration is documented without including secrets.
- [ ] Core workflow can be completed from resume input to job review.
- [ ] Matching results are displayed consistently with the jobs analyzed.
- [ ] Application Queue and Applications Tracker show the intended separate datasets.
- [ ] Status updates persist and timestamps behave as specified.
- [ ] Generated materials can be reviewed before external use.
- [ ] Errors and fallback data are clearly identified.
- [ ] No secrets or private user data are committed.
- [ ] Known limitations are documented for the demo/release.

## 18. Future Considerations

Potential future work, subject to validation and prioritization:
- User accounts and secure multi-user workspaces.
- Additional job-board integrations.
- Notifications and follow-up reminders.
- Application analytics and customizable dashboards.
- Resume version history and document export.
- Calendar integration for interviews.
- More detailed skill development plans.
- Deployment, observability, and production operations.
- Subscription or monetization features.

## 19. Open Questions

1. Which resume file formats and maximum sizes are officially supported?
2. Which job-source fields and filters are guaranteed by the current Adzuna integration?
3. What matching factors and score interpretation are currently implemented?
4. Are generated resumes and cover letters exportable, or only viewable in the app?
5. Which agent outputs are persisted between sessions?
6. Is the current release single-user/local, or is multi-user deployment planned?
7. What are the data retention and deletion expectations?
8. Which tests and acceptance thresholds must pass before public deployment?
9. What license and contribution model should the repository use?
10. Which features are confirmed working versus planned or partially implemented?

---

**Document note:** This PRD is based on the available CareerFlow AI project context and previously described workflows. It should be reconciled with the current repository before being used as a final engineering contract.
