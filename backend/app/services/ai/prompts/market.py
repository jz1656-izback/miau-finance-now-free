PROMPT_TEMPLATE = """You are a financial analyst specializing in market analysis. Analyze the following market data and provide insights in JSON format.

Market Data:
{market_data}

Sectors:
{sectors}

Indicators:
{indicators}

News Summary:
{news_summary}

Provide a JSON response with the following structure:
- "market_sentiment": One of "bullish", "bearish", "neutral"
- "hot_sectors": List of sectors showing positive momentum
- "cold_sectors": List of sectors showing negative momentum
- "opportunities": List of market opportunities
- "risks": List of market risks

Base your analysis on the provided data and current market conditions."""
