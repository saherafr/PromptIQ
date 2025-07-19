# PromptIQ — Enterprise-Grade LLM Prompt Optimization Backend System

PromptIQ is a SaaS-style backend system that evaluates and improves prompts written for large language models.  
It uses AWS Bedrock (Claude) to generate better versions of user prompts, assigns detailed quality scores, explains improvements, and stores versioned prompt history in DynamoDB.  
Designed as a modular, distributed backend with production-level deployment via Docker and AWS EC2.

---


### What is PromptIQ?

PromptIQ provides an API for prompt evaluation and optimization. It is designed for engineers, researchers, and LLM users who want to refine their prompts for clarity, structure, and detail.  
The system uses Claude via AWS Bedrock to generate improved versions of prompts and applies scoring and feedback logic for each submission.  
PromptIQ is built using FastAPI, DynamoDB, and Docker, and follows system design principles for enterprise scalability and extensibility.

---

### Functional Requirements

- Rewrite prompts using Claude
- Return structured quality scores (clarity, structure, detail)
- Generate explanations and root cause feedback
- Support rewrite modes: `refine`, `summarize`, `elaborate`
- Maintain prompt versioning with timestamps and metadata
- Provide debug mode with Claude inputs/outputs and latency
- Validate API key for authorized access (optional)

---

### Non-Functional Requirements

- Designed for low-latency (<3 seconds end-to-end)
- Modular and stateless architecture
- Deployable via Docker to AWS EC2
- Scalable AWS-native components (DynamoDB, Bedrock)
- Extensible to support other LLMs (OpenAI, Gemini, etc.)
- Secure with IAM roles and environment-based secrets
- Observable through internal logging and trace mode

---

### Key User Actions

- Submit a prompt for rewriting
- Select a rewrite mode (`refine`, `summarize`, or `elaborate`)
- Receive a better version of the prompt
- Get a detailed score report with explanation
- View feedback on why their prompt was weak
- Access full version history (optional)
- Enable debug mode to trace Claude inputs and latency
- Access the API using a secure API key (optional)

---

### Prompt Flow (End-to-End)

1. User sends a POST request to `/optimize` with:
   - Prompt text
   - Selected rewrite mode
   - Optional debug flag
   - Optional API key

2. FastAPI validates the request and checks the API key

3. PromptAnalyzer service:
   - Sends prompt to Claude via Bedrock
   - Receives rewritten prompt
   - Sends original + rewritten prompts to scoring service
   - Sends both prompts to explanation engine
   - Assembles response

4. DynamoDB stores:
   - Prompt ID and timestamps
   - User prompt and rewritten version
   - Scoring breakdown
   - Explanation and root cause
   - Rewrite mode used

5. API returns:
   - Optimized prompt
   - Score breakdown and total score
   - Explanation and feedback
   - Prompt version ID and timestamp
   - Debug data if enabled

---

### System Design Concepts Applied

- Stateless service interactions
- Loose coupling between rewrite, scoring, and explanation components
- Clear data versioning for audit trail
- Parameterized model prompting via rewrite modes
- Observability via structured debug logs
- Simulated SaaS access model with API keys

