cube(`PnL`, {
  sql: `SELECT * FROM pnl`,

  joins: {
    Portfolios: {
      sql: `${CUBE}.portfolio_id = ${Portfolios}.id`,
      relationship: `belongsTo`,
    },
  },

  measures: {
    totalPnl: {
      sql: `pnl_amount`,
      type: `sum`,
      title: `Total P&L`,
    },
    avgPnl: {
      sql: `pnl_amount`,
      type: `avg`,
      title: `Avg P&L`,
    },
    positivePnl: {
      sql: `CASE WHEN pnl_amount > 0 THEN pnl_amount ELSE 0 END`,
      type: `sum`,
      title: `Positive P&L`,
    },
    negativePnl: {
      sql: `CASE WHEN pnl_amount < 0 THEN pnl_amount ELSE 0 END`,
      type: `sum`,
      title: `Negative P&L`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true,
    },
    pnlType: {
      sql: `pnl_type`,
      type: `string`,
      title: `P&L Type`,
    },
    pnlAmount: {
      sql: `pnl_amount`,
      type: `number`,
      title: `P&L Amount`,
    },
    currency: {
      sql: `currency`,
      type: `string`,
      title: `Currency`,
    },
    source: {
      sql: `source`,
      type: `string`,
      title: `Source`,
    },
    fromDate: {
      sql: `from_date`,
      type: `time`,
      title: `From Date`,
    },
    toDate: {
      sql: `to_date`,
      type: `time`,
      title: `To Date`,
    },
  },
});
