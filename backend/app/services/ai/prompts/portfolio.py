PROMPT_TEMPLATE = """You are a financial analyst specializing in portfolio analysis. Analyze the following portfolio and provide insights in JSON format.

Holdings:
{holdings}

Performance:
{performance}

Risk Metrics:
{risk_metrics}

Benchmark:
{benchmark}

Provide a JSON response with the following structure:
- "summary": A brief overview of the portfolio's current state
- "strengths": List of portfolio strengths
- "weaknesses": List of portfolio weaknesses
- "recommendations": List of actionable recommendations
- "risk_level": One of "low", "medium", "high", "very_high"

Focus on actionable insights and data-driven analysis."""
