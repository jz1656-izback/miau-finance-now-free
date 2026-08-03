export class MarketModule {
  constructor(client) { this.client = client }
  async getPrice(ticker) { return this.client.get(`/api/v1/market/live?tickers=${ticker}`) }
  async getHistory(ticker, period = '1y') { return this.client.get(`/api/v1/market/historical/${ticker}?period=${period}`) }
  async getCrypto() { return this.client.get('/api/v1/market/crypto') }
  async getForex() { return this.client.get('/api/v1/market/forex') }
  async getSectors() { return this.client.get('/api/v1/market/sectors') }
}
