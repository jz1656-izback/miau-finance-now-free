PROMPT_TEMPLATE = """You are a risk management expert. Assess the portfolio risk based on the following metrics and provide insights in JSON format.

Value at Risk (VaR):
{var}

Conditional VaR (CVaR):
{cvar}

Maximum Drawdown:
{max_drawdown}

Volatility:
{volatility}

Correlations:
{correlations}

Provide a JSON response with the following structure:
- "risk_score": A numeric score from 0 to 100
- "risk_factors": List of key risk factors identified
- "mitigation": List of risk mitigation suggestions
- "stress_test_results": Description of how the portfolio might perform under stress scenarios

Be conservative in your risk assessment and highlight the most critical risks first."""
