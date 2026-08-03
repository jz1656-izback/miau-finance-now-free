cube(`MarketData`, {
  sql: `SELECT * FROM market_data`,

  joins: {
    Instruments: {
      sql: `${CUBE}.instrument_id = ${Instruments}.id`,
      relationship: `belongsTo`,
    },
  },

  measures: {
    avgClose: {
      sql: `close`,
      type: `avg`,
      title: `Avg Close Price`,
    },
    avgVolume: {
      sql: `volume`,
      type: `avg`,
      title: `Avg Volume`,
    },
    totalVolume: {
      sql: `volume`,
      type: `sum`,
      title: `Total Volume`,
    },
    highPrice: {
      sql: `high`,
      type: `max`,
      title: `High Price`,
    },
    lowPrice: {
      sql: `low`,
      type: `min`,
      title: `Low Price`,
    },
    priceRange: {
      sql: `high - low`,
      type: `avg`,
      title: `Avg Daily Range`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true,
    },
    date: {
      sql: `date`,
      type: `time`,
      title: `Date`,
    },
    open: {
      sql: `open`,
      type: `number`,
      title: `Open`,
    },
    high: {
      sql: `high`,
      type: `number`,
      title: `High`,
    },
    low: {
      sql: `low`,
      type: `number`,
      title: `Low`,
    },
    close: {
      sql: `close`,
      type: `number`,
      title: `Close`,
    },
    volume: {
      sql: `volume`,
      type: `number`,
      title: `Volume`,
    },
  },
});
