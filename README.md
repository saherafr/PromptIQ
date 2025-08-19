# PromptIQ – Intelligent Prompt Analyzer

## Overview
PromptIQ is a backend system that provides **prompt analysis, scoring, explanation, and response generation** for Large Language Model (LLM) applications.  
It is designed as a **production-ready service** that emphasizes **fault tolerance, scalability, and extensibility**, built on AWS-managed infrastructure.

The project is intentionally structured with **system design principles** to demonstrate how an AI-powered service can be built to scale beyond a prototype.

👉 The live frontend is deployed here: [https://prompt-iq-frontend.vercel.app/](https://prompt-iq-frontend.vercel.app/)


---

## Workflow

### High-Level Flow
1. **Frontend (Client UI)** sends a request containing a prompt and action through **API Gateway**.  
2. **API Gateway** acts as the managed entry point and routes requests to the backend.  
3. **Lambda Handler** receives the event and dispatches based on the requested action:  
   - `analyze` → Analyzer service  
   - `score` → Prompt scorer  
   - `explain` → Explanation generator  
   - `respond` → Direct Bedrock Claude inference  
4. **Service Layer** encapsulates business logic (`analyzer.py`, `scorer.py`, `explainer.py`, `bedrock_client.py`).  
5. **AWS Bedrock (Anthropic Claude)** executes inference with retry and fault-tolerance mechanisms.  
6. **Response** is returned to API Gateway and forwarded to the frontend.

---

## Architecture Diagram

                      +--------------------+
                      |   Frontend (UI)    |
                      +--------------------+
                                |
                                v
                    +--------------------------+
                    |   Amazon CloudFront      |
                    |  (CDN + optional WAF)    |
                    +--------------------------+
                                |
                                v
                    +--------------------------+
                    |   Amazon API Gateway     |
                    | (Entry point + routing)  |
                    +--------------------------+
                       /           |          \
                      /            |           \
                     v             v            v
          +----------------+  +----------------+  +----------------+
          | Lambda Instance|  | Lambda Instance|  | Lambda Instance|
          |   (Handler)    |  |   (Handler)    |  |   (Handler)    |
          +----------------+  +----------------+  +----------------+
                      | (horizontal scaling across AZs)
                      v
              +------------------------+
              |  Service Layer         |
              |  - Analyzer            |
              |  - Scorer              |
              |  - Explainer           |
              |  - Bedrock Client      |
              +------------------------+
                      |
                      v
           +-------------------------------+
           | AWS Bedrock (Claude LLM API)  |
           +-------------------------------+
                      |
                      v
              +----------------------+
              |   Response JSON      |
              +----------------------+

---

## Fault Tolerance
- **Multi-AZ Resiliency**: Lambda automatically runs across multiple Availability Zones.  
- **Retry + Circuit Breaker**: Bedrock client uses exponential backoff and breaker patterns.  
- **Future Improvements**:  
  - Multi-region failover with Route 53 health checks.  
  - Dead-letter queues (SQS) for failed Lambda executions.  
  - Distributed caching (DynamoDB DAX or ElastiCache) to reduce repeated calls.  

---

## Load Balancing
- **Current**:  
  - API Gateway distributes requests across Lambda instances.  
  - Lambda scales horizontally to handle increased load.  
  - CloudFront provides edge caching.  
- **Future Improvements**:  
  - Weighted load balancing for A/B testing different model versions.  
  - Latency-based routing across regions.  
  - ALB in front of ECS/EKS microservices for advanced routing.  

---

## Use Cases
- **Prompt Engineering**: Audit prompts for ambiguity, bias, and weaknesses.  
- **LLM Evaluation**: Score responses for quality and consistency.  
- **Education & Training**: Explain why a response is strong or weak.  
- **AI Application Integration**: Serve as a “QA layer” for prompts in production apps.  

---

## Functional Requirements
- Analyze prompts for clarity, structure, and risks.  
- Score prompt-response pairs with **numeric + categorical feedback**.  
- Provide **natural language explanations** of scores.  
- Generate responses via **AWS Bedrock Claude**.  
- Implement **retry + circuit breaker** for resiliency.  
- Maintain consistent **JSON schema** for API responses.  
- Provide **observability** through CloudWatch.  
- Ensure **fault tolerance + load balancing**.  

---

## Architecture and Design Choices

### AWS Lambda + API Gateway
- **Reasoning**: Serverless → auto-scaling + cost efficiency.  
- **Trade-off**: Cold starts add latency.  
- **Future**: ECS/Fargate for persistent services.  

### Service Layer Abstraction
- **Reasoning**: Separation improves modularity & testability.  
- **Trade-off**: Slightly more complex than a monolith.  
- **Future**: Move to microservices with independent scaling.  

### AWS Bedrock (Claude)
- **Reasoning**: Secure, managed, enterprise-ready LLM.  
- **Trade-off**: Vendor lock-in + request-based cost.  
- **Future**: Abstraction layer for OpenAI, HuggingFace, local models.  

### Retry + Circuit Breaker
- **Reasoning**: Resiliency against transient failures.  
- **Trade-off**: More error handling complexity.  
- **Future**: AWS Step Functions for workflow retries.  

### CloudWatch Logging & Metrics
- **Reasoning**: Observability for debugging + metrics.  
- **Trade-off**: Logging cost must be managed.  
- **Future**: Centralized analysis via OpenSearch or third-party APM.  

### Security & Rate Limiting
- **Current**: CORS at API Gateway, monitoring, WAF planned.  
- **Trade-off**: HTTP APIs lack quota/usage plan features.  
- **Future**: Deploy behind CloudFront + AWS WAF.  

---

## Trade-offs Made
- **HTTP API vs REST API**: HTTP API chosen → simplicity & cost.  
- **Serverless vs Persistent**: Serverless chosen → cost efficiency, but adds latency.  
- **Single Region**: Runs in `us-east-1` only → simple but no regional redundancy.  
- **Synchronous Requests**: LLM latency blocks client response.  
- **Managed Scalability**: Relies on API Gateway + Lambda → less fine-grained control.  

---

## Possible Future Improvements
- Multi-model abstraction (OpenAI, HuggingFace, local).  
- Persistent storage (DynamoDB, RDS) for histories/analytics.  
- Asynchronous workloads (SQS + worker Lambdas).  
- Multi-region active-active deployment.  
- CloudFront + WAF for global caching & security.  
- RBAC, audit trails, billing features.  
- Advanced routing & distributed cache.  

---

## System Design Lessons
- Modular service design = maintainability & scaling flexibility.  
- Fault tolerance patterns are **mandatory** for LLM APIs.  
- Serverless → elasticity + resilience but sacrifices control.  
- Observability must evolve into **centralized, proactive monitoring**.  
- Design favors **simplicity today**, but is extensible for enterprise scale.  

---

## Conclusion
PromptIQ demonstrates how an **AI-powered backend** can be designed with **scalability, fault tolerance, and system design principles** in mind.  
It is **optimized for modularity and cost efficiency today**, with a **roadmap toward enterprise SaaS capabilities** for LLM prompt evaluation and optimization.

