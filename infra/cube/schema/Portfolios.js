cube(`Portfolios`, {
  sql: `SELECT * FROM portfolios`,

  joins: {
    Positions: {
      sql: `${CUBE}.id = ${Positions}.portfolio_id`,
      relationship: `hasMany`,
    },
  },

  measures: {
    count: {
      sql: `id`,
      type: `count`,
      title: `Total Portfolios`,
    },
    totalValue: {
      sql: `${Positions.marketValue}`,
      type: `sum`,
      title: `Total Portfolio Value`,
    },
    avgPortfolioValue: {
      sql: `${Positions.marketValue}`,
      type: `avg`,
      title: `Avg Portfolio Value`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true,
    },
    name: {
      sql: `name`,
      type: `string`,
      title: `Portfolio Name`,
    },
    portfolioType: {
      sql: `portfolio_type`,
      type: `string`,
      title: `Type`,
    },
    baseCurrency: {
      sql: `base_currency`,
      type: `string`,
      title: `Base Currency`,
    },
    managementStyle: {
      sql: `management_style`,
      type: `string`,
      title: `Management Style`,
    },
  },
});
