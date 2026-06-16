# MetricMind: Agentic Root-Cause Analytics Engine

MetricMind is an AI-native analytics system that investigates why a business metric changed. It uses SQL-backed analysis, root-cause detection, Gemini-powered insight generation, and an evaluator agent to produce evidence-checked business recommendations.

## Problem Statement

Traditional dashboards tell users what happened, but not why it happened.

MetricMind enables users to ask natural-language business questions and automatically performs SQL analysis, root-cause detection, evidence verification, and insight generation.

## Key Features

- Natural Language → SQL Generation
- Automated Root-Cause Analysis
- DuckDB-Based Query Execution
- Failure Detection for Unsafe Queries
- AI-Generated Business Insights
- Evidence Verification Agent
- Interactive Visualizations
- Downloadable Analytics Reports
- 
## Architecture

User Question
      ↓
SQL Generation Agent
      ↓
DuckDB Query Execution
      ↓
Failure Detection Agent
      ↓
Analytics Result
      ↓
Insight Generation Agent
      ↓
Evidence Verification Agent
      ↓
Final Report


- ## Tech Stack

| Layer | Technology |
|---------|------------|
| Frontend | Streamlit |
| Analytics Engine | DuckDB |
| LLM | Gemini 2.5 Flash |
| Data Processing | Pandas |
| Visualization | Plotly |
| Language | Python |

## Sample Questions

- Which category had the highest revenue decline?
- Which region performed worst in June?
- Show categories with refund rates above 0.08.
- Which business segment caused the largest revenue drop?
- Which category recovered revenue despite high refunds?

- ## Results

MetricMind successfully converts natural-language business questions into executable SQL queries and generates evidence-backed business insights.

Current capabilities include:

- SQL generation from natural language
- Automated query execution
- Root-cause identification
- Business insight generation
- Evidence verification
- Report export


