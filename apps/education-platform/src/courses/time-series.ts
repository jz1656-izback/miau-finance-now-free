import type { Course } from '../lib/types'

export const timeSeriesAnalysis: Course = {
  id: 'time-series-analysis',
  slug: 'time-series-analysis',
  title: 'Time Series Analysis',
  description: 'ARIMA, GARCH, stationarity, and forecasting — the cat predicts the future.',
  category: 'Quantitative Analysis',
  difficulty: 'advanced',
  icon: '📈',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ts-stationarity',
      slug: 'stationarity',
      title: 'Stationarity & Time Series Properties',
      description: 'Why stationarity matters for forecasting.',
      commands: ['ts', 'ts stationarity'],
      steps: [
        { instruction: 'Test for stationarity: `ts stationarity --series AAPL --test adf`', command: 'ts stationarity --series AAPL --test adf', expectedOutput: 'ADF test statistic, p-value, and stationarity verdict' },
        { instruction: 'A stationary series has constant mean, variance, and autocorrelation over time.' },
        { instruction: 'Stock prices are non-stationary; returns are typically stationary.' },
      ],
      quiz: [
        { question: 'What does it mean for a time series to be stationary?', options: ['Constant statistical properties over time', 'No movement in the series', 'A perfectly predictable pattern', 'Zero variance'], correctIndex: 0, explanation: 'A stationary time series has constant mean, variance, and autocorrelation structure over time.' },
      ],
    },
    {
      id: 'ts-arima',
      slug: 'arima-models',
      title: 'ARIMA Models',
      description: 'Autoregressive Integrated Moving Average for forecasting.',
      commands: ['arima', 'arima fit'],
      steps: [
        { instruction: 'Fit an ARIMA model: `arima fit --series AAPL --order 1-1-1`', command: 'arima fit --series AAPL --order 1-1-1', expectedOutput: 'ARIMA(1,1,1) summary with coefficients and AIC' },
        { instruction: 'ARIMA(p,d,q): p = autoregressive lags, d = differencing, q = moving average lags.' },
        { instruction: 'AIC and BIC help select the best ARIMA order — lower is better.' },
      ],
      quiz: [
        { question: 'What does the "d" parameter in ARIMA(p,d,q) represent?', options: ['Number of differencing steps to make series stationary', 'Number of autoregressive terms', 'Number of moving average terms', 'Forecast horizon'], correctIndex: 0, explanation: 'The "d" parameter represents the number of times the series must be differenced to become stationary.' },
      ],
    },
    {
      id: 'ts-garch',
      slug: 'garch-models',
      title: 'GARCH for Volatility Modeling',
      description: 'Model changing volatility over time.',
      commands: ['garch', 'garch fit'],
      steps: [
        { instruction: 'Fit a GARCH model: `garch fit --series AAPL --order 1-1`', command: 'garch fit --series AAPL --order 1-1', expectedOutput: 'GARCH(1,1) summary with volatility forecasts' },
        { instruction: 'GARCH captures volatility clustering — periods of high volatility tend to persist.' },
        { instruction: 'GARCH(1,1) is the most common specification — one lag each for ARCH and GARCH terms.' },
      ],
      quiz: [
        { question: 'What pattern does GARCH capture?', options: ['Volatility clustering — high vol follows high vol', 'Linear trends', 'Seasonal patterns', 'Price jumps'], correctIndex: 0, explanation: 'GARCH models capture volatility clustering, where large changes tend to be followed by large changes.' },
      ],
    },
    {
      id: 'ts-forecast',
      slug: 'forecasting',
      title: 'Forecasting with Time Series',
      description: 'Generate and evaluate forecasts.',
      commands: ['forecast', 'forecast run'],
      steps: [
        { instruction: 'Generate a forecast: `forecast run --series AAPL --model arima --horizon 30`', command: 'forecast run --series AAPL --model arima --horizon 30', expectedOutput: '30-day forecast with confidence intervals' },
        { instruction: 'Confidence intervals widen as the forecast horizon extends — uncertainty grows.' },
        { instruction: 'Walk-forward validation is essential for time series — never use future data.' },
      ],
      quiz: [
        { question: 'What happens to confidence intervals as forecast horizon increases?', options: ['They widen — more uncertainty', 'They narrow — more certainty', 'They stay the same', 'They become negative'], correctIndex: 0, explanation: 'Forecast uncertainty increases with horizon, so confidence intervals widen as you predict further into the future.' },
      ],
    },
  ],
}
