import type { Course } from '../lib/types'

export const sqlForFinance: Course = {
  id: 'sql-finance',
  slug: 'sql-for-finance',
  title: 'SQL for Finance',
  description: 'Querying databases, joins, window functions, and financial data — the cat speaks SQL better than you speak cat.',
  category: 'Data Science',
  difficulty: 'intermediate',
  icon: '🗄️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'sql-basics',
      slug: 'sql-query-basics',
      title: 'SQL Query Basics',
      description: 'SELECT, FROM, WHERE for financial data.',
      commands: ['sql', 'sql query'],
      steps: [
        { instruction: 'Run a basic SQL query on trades data: `sql query "SELECT symbol, SUM(volume) FROM trades WHERE date >= \'2025-01-01\' GROUP BY symbol"`', command: 'sql query "SELECT symbol, SUM(volume) FROM trades WHERE date >= \'2025-01-01\' GROUP BY symbol"', expectedOutput: 'Result table with symbols and their total trading volumes' },
        { instruction: 'SQL is the lingua franca of data analysis — every quant must know it.' },
        { instruction: 'The cat SELECTs tuna FROM bowl WHERE hungry = true.' },
      ],
      quiz: [
        { question: 'What does GROUP BY do in a SQL query?', options: ['Aggregates rows sharing the same column value', 'Groups queries into transactions', 'Creates table partitions', 'Orders the result set'], correctIndex: 0, explanation: 'GROUP BY collects rows with the same values in specified columns and allows aggregate functions to run per group.' },
      ],
    },
    {
      id: 'sql-joins',
      slug: 'sql-joins-finance',
      title: 'Joins for Financial Data',
      description: 'Combining tables for deeper analysis.',
      commands: ['query', 'query join'],
      steps: [
        { instruction: 'Join trades with reference data: `query join --trades trades --ref securities --on ticker --select symbol,company_name,volume`', command: 'query join --trades trades --ref securities --on ticker --select symbol,company_name,volume', expectedOutput: 'Joined table with trade volumes and company names' },
        { instruction: 'INNER JOIN returns only matching rows; LEFT JOIN keeps all rows from the left table.' },
        { instruction: 'The cat loves LEFT JOINs — it never leaves anything behind.' },
      ],
      quiz: [
        { question: 'When would you use a LEFT JOIN?', options: ['When you need all records from the left table regardless of matches', 'When you only want exact matches', 'When joining more than two tables', 'When performance is critical'], correctIndex: 0, explanation: 'LEFT JOIN returns all rows from the left table and matching rows from the right table, filling non-matches with NULL.' },
      ],
    },
    {
      id: 'sql-window',
      slug: 'window-functions-finance',
      title: 'Window Functions',
      description: 'Rolling calculations and rankings.',
      commands: ['sql', 'sql window'],
      steps: [
        { instruction: 'Calculate running total: `sql window --function "SUM(volume) OVER (PARTITION BY symbol ORDER BY date)" --table trades`', command: 'sql window --function "SUM(volume) OVER (PARTITION BY symbol ORDER BY date)" --table trades', expectedOutput: 'Running cumulative volume per symbol over time' },
        { instruction: 'Window functions perform calculations across rows related to the current row.' },
        { instruction: 'The cat\'s window function tracks tuna consumption over time — it is always increasing.' },
      ],
      quiz: [
        { question: 'What does ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date) do?', options: ['Assigns a sequential number per symbol ordered by date', 'Counts total rows in the table', 'Numbers all rows sequentially', 'Creates a new partitioned table'], correctIndex: 0, explanation: 'ROW_NUMBER() assigns a unique sequential integer to each row within a partition, starting at 1 for each group.' },
      ],
    },
    {
      id: 'sql-financial',
      slug: 'financial-data-analysis-sql',
      title: 'Financial Data Analysis with SQL',
      description: 'Real-world financial queries.',
      commands: ['query', 'query financial'],
      steps: [
        { instruction: 'Find top 10 stocks by Sharpe ratio: `query financial --metric sharpe --top 10 --period 1y`', command: 'query financial --metric sharpe --top 10 --period 1y', expectedOutput: 'Top 10 stocks ranked by Sharpe ratio with annualized returns and volatility' },
        { instruction: 'SQL can calculate portfolio metrics, risk measures, and attribution.' },
        { instruction: 'The cat\'s portfolio SQL query returns: buy more tuna.' },
      ],
      quiz: [
        { question: 'Why use SQL over Excel for financial analysis?', options: ['SQL handles larger datasets and is reproducible', 'Excel cannot do financial analysis', 'SQL is always faster', 'SQL has better charting'], correctIndex: 0, explanation: 'SQL scales to millions of rows, is fully scriptable, and produces reproducible analyses compared to manual Excel work.' },
      ],
    },
  ],
}
