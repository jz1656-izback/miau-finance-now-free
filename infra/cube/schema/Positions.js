cube(`Positions`, {
  sql: `SELECT * FROM positions`,

  joins: {
    Instruments: {
      sql: `${CUBE}.instrument_id = ${Instruments}.id`,
      relationship: `belongsTo`,
    },
    Portfolios: {
      sql: `${CUBE}.portfolio_id = ${Portfolios}.id`,
      relationship: `belongsTo`,
    },
  },

  measures: {
    count: {
      sql: `id`,
      type: `count`,
      title: `Total Positions`,
    },
    totalQuantity: {
      sql: `quantity`,
      type: `sum`,
      title: `Total Quantity`,
    },
    marketValue: {
      sql: `market_value`,
      type: `sum`,
      title: `Market Value`,
    },
    totalUnrealizedPnl: {
      sql: `unrealized_pnl`,
      type: `sum`,
      title: `Unrealized P&L`,
    },
    totalRealizedPnl: {
      sql: `realized_pnl`,
      type: `sum`,
      title: `Realized P&L`,
    },
    totalCostBasis: {
      sql: `cost_basis`,
      type: `sum`,
      title: `Cost Basis`,
    },
    returnPct: {
      sql: `CASE WHEN cost_basis != 0 THEN ((market_value - cost_basis) / ABS(cost_basis)) * 100 ELSE 0 END`,
      type: `avg`,
      title: `Return %`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true,
    },
    quantity: {
      sql: `quantity`,
      type: `number`,
      title: `Quantity`,
    },
    averagePrice: {
      sql: `average_price`,
      type: `number`,
      title: `Avg Price`,
    },
    marketValue: {
      sql: `market_value`,
      type: `number`,
      title: `Market Value`,
    },
    unrealizedPnl: {
      sql: `unrealized_pnl`,
      type: `number`,
      title: `Unrealized P&L`,
    },
    costBasis: {
      sql: `cost_basis`,
      type: `number`,
      title: `Cost Basis`,
    },
    asOfDate: {
      sql: `as_of_date`,
      type: `time`,
      title: `As Of Date`,
    },
  },
});
