# Miau Finance curl Examples
API key: `export MIAU_API_KEY="miau_abc123"`
## Market
curl -H "Authorization: Bearer $MIAU_API_KEY" https://miau.finance/api/v1/market/live?tickers=AAPL
curl https://miau.finance/api/v1/market/historical/AAPL?period=1y
curl https://miau.finance/api/v1/currencies
curl https://miau.finance/api/v1/currencies/convert?amount=100&from=USD&to=EUR
## Portfolios
curl https://miau.finance/api/v1/portfolios
curl https://miau.finance/api/v1/portfolios/{id}/positions
## Trading
curl -X POST -H "Content-Type: application/json" -d '{"ticker":"AAPL","quantity":10,"side":"BUY"}' https://miau.finance/api/v1/orders
