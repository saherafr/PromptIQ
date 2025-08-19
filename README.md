# PromptIQ – Intelligent Prompt Analyzer

## Overview
PromptIQ is a backend system that provides **prompt analysis, scoring, explanation, and response generation** for Large Language Model (LLM) applications.  
It is designed as a **production-ready service** that emphasizes **fault tolerance, scalability, and extensibility**, built on AWS-managed infrastructure.

The project is intentionally structured with **system design principles** to demonstrate how an AI-powered service can be built to scale beyond a prototype.

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

## Architecture Diagram (Mermaid)

```mermaid
flowchart TD
    A[Frontend (UI)] --> B[Amazon CloudFront (CDN + optional WAF)]
    B --> C[Amazon API Gateway]

    subgraph LambdaScaling[Lambda Horizontal Scaling (Multi-AZ)]
        C --> L1[Lambda Instance (Handler)]
        C --> L2[Lambda Instance (Handler)]
        C --> L3[Lambda Instance (Handler)]
    end

    L1 --> D[Service Layer]
    L2 --> D
    L3 --> D

    subgraph Services[Service Layer]
        D1[Analyzer] --> D
        D2[Scorer] --> D
        D3[Explainer] --> D
        D4[Bedrock Client] --> D
    end

    D --> E[AWS Bedrock (Claude LLM API)]
    E --> F[Response JSON]

    %% Fault Tolerance Notes
    classDef ft fill=#f9f,stroke=#333,stroke-width=1px;
    C:::ft
    L1:::ft
    L2:::ft
    L3:::ft
    E:::ft
