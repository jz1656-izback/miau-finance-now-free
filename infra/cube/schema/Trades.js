cube(`Trades`, {
  sql: `SELECT * FROM trades`,

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
      title: `Total Trades`,
    },
    totalNotional: {
      sql: `notional`,
      type: `sum`,
      title: `Total Notional`,
    },
    avgNotional: {
      sql: `notional`,
      type: `avg`,
      title: `Avg Notional`,
    },
    totalCommission: {
      sql: `commission`,
      type: `sum`,
      title: `Total Commission`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true,
    },
    tradeId: {
      sql: `trade_id`,
      type: `string`,
      title: `Trade ID`,
    },
    tradeType: {
      sql: `trade_type`,
      type: `string`,
      title: `Trade Type`,
    },
    side: {
      sql: `side`,
      type: `string`,
      title: `Side`,
    },
    quantity: {
      sql: `quantity`,
      type: `number`,
      title: `Quantity`,
    },
    price: {
      sql: `price`,
      type: `number`,
      title: `Price`,
    },
    notional: {
      sql: `notional`,
      type: `number`,
      title: `Notional`,
    },
    currency: {
      sql: `currency`,
      type: `string`,
      title: `Currency`,
    },
    trader: {
      sql: `trader`,
      type: `string`,
      title: `Trader`,
    },
    status: {
      sql: `status`,
      type: `string`,
      title: `Status`,
    },
    tradeDate: {
      sql: `trade_date`,
      type: `time`,
      title: `Trade Date`,
    },
  },
});
