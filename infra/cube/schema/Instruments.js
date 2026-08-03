cube(`Instruments`, {
  sql: `SELECT * FROM instruments`,

  joins: {
    MarketData: {
      sql: `${CUBE}.id = ${MarketData}.instrument_id`,
      relationship: `hasMany`,
    },
    Positions: {
      sql: `${CUBE}.id = ${Positions}.instrument_id`,
      relationship: `hasMany`,
    },
  },

  measures: {
    count: {
      sql: `id`,
      type: `count`,
      title: `Total Instruments`,
    },
    countByType: {
      sql: `instrument_type`,
      type: `countDistinct`,
      title: `Instrument Types`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true,
    },
    ticker: {
      sql: `ticker`,
      type: `string`,
      title: `Ticker`,
    },
    name: {
      sql: `name`,
      type: `string`,
      title: `Instrument Name`,
    },
    instrumentType: {
      sql: `instrument_type`,
      type: `string`,
      title: `Type`,
    },
    currency: {
      sql: `currency`,
      type: `string`,
      title: `Currency`,
    },
    exchange: {
      sql: `exchange`,
      type: `string`,
      title: `Exchange`,
    },
    sector: {
      sql: `sector`,
      type: `string`,
      title: `Sector`,
    },
    industry: {
      sql: `industry`,
      type: `string`,
      title: `Industry`,
    },
    created_at: {
      sql: `created_at`,
      type: `time`,
    },
  },
});
