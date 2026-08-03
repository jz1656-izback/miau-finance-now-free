export class PortfolioModule {
  constructor(client) { this.client = client }
  async list() { return this.client.get('/api/v1/portfolios') }
  async get(id) { return this.client.get(`/api/v1/portfolios/${id}`) }
  async create(data) { return this.client.post('/api/v1/portfolios', data) }
  async update(id, data) { return this.client.put(`/api/v1/portfolios/${id}`, data) }
  async delete(id) { return this.client.delete(`/api/v1/portfolios/${id}`) }
}
