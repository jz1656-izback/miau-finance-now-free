export class TradingModule {
  constructor(client) { this.client = client }
  async createOrder(ticker, side, qty, type, price) {
    return this.client.post('/api/v1/orders', { ticker, side, quantity: qty, order_type: type, price })
  }
  async listOrders(status) {
    const query = status ? `?status=${status}` : ''
    return this.client.get(`/api/v1/orders${query}`)
  }
  async cancelOrder(id) { return this.client.delete(`/api/v1/orders/${id}`) }
  async listStrategies() { return this.client.get('/api/v1/strategies') }
  async backtest(strategy, ticker, period) {
    return this.client.post('/api/v1/strategies/backtest', { strategy_name: strategy, ticker, period })
  }
}
