# MetricMind: Agentic Root-Cause Analytics Engine

MetricMind is an AI-native analytics system that investigates why a business metric changed. It uses SQL-backed analysis, root-cause detection, Gemini-powered insight generation, and an evaluator agent to produce evidence-checked business recommendations.
## Architecture

```text
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
