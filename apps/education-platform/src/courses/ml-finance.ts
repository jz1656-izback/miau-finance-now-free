import type { Course } from '../lib/types'

export const machineLearningFinance: Course = {
  id: 'machine-learning-finance',
  slug: 'machine-learning-finance',
  title: 'Machine Learning for Finance',
  description: 'Regression, classification, clustering, and overfitting — the cat trains models.',
  category: 'AI & Machine Learning',
  difficulty: 'advanced',
  icon: '🤖',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ml-regression',
      slug: 'regression-models',
      title: 'Regression in Finance',
      description: 'Predict continuous values like stock prices and returns.',
      commands: ['ml', 'ml regression'],
      steps: [
        { instruction: 'Run a regression model: `ml regression --target AAPL --features SPY GDP`', command: 'ml regression --target AAPL --features SPY GDP', expectedOutput: 'Regression summary with R², coefficients, and p-values' },
        { instruction: 'Linear regression finds the line of best fit through data points.' },
        { instruction: 'R² measures how much of the variance in the target is explained by features.' },
      ],
      quiz: [
        { question: 'What does R² measure in regression?', options: ['Proportion of variance explained by the model', 'Prediction accuracy', 'Number of features', 'Model complexity'], correctIndex: 0, explanation: 'R² (coefficient of determination) measures the proportion of variance in the target variable explained by the model.' },
      ],
    },
    {
      id: 'ml-classification',
      slug: 'classification-models',
      title: 'Classification Models',
      description: 'Predict categories: buy/sell/hold, default/no-default.',
      commands: ['predict', 'predict classification'],
      steps: [
        { instruction: 'Run a classification model: `ml classification --target buy-sell --features momentum volatility`', command: 'ml classification --target buy-sell --features momentum volatility', expectedOutput: 'Classification report with accuracy, precision, recall, and F1-score' },
        { instruction: 'Classification predicts discrete categories rather than continuous values.' },
        { instruction: 'Precision = true positives / (true positives + false positives). Recall = true positives / (true positives + false negatives).' },
      ],
      quiz: [
        { question: 'What does precision measure in classification?', options: ['How many selected items are relevant', 'How many relevant items are selected', 'Overall accuracy', 'Model speed'], correctIndex: 0, explanation: 'Precision measures the proportion of positive identifications that were actually correct (true positives / all positive predictions).' },
      ],
    },
    {
      id: 'ml-clustering',
      slug: 'clustering',
      title: 'Clustering & Unsupervised Learning',
      description: 'Find patterns in data without labels.',
      commands: ['train', 'train model'],
      steps: [
        { instruction: 'Run clustering: `ml cluster --k 5 --features returns volatility`', command: 'ml cluster --k 5 --features returns volatility', expectedOutput: 'Cluster assignments with centroids and silhouette score' },
        { instruction: 'K-means clustering groups similar data points into K clusters.' },
        { instruction: 'Use clustering for portfolio construction — find groups of stocks that behave similarly.' },
      ],
      quiz: [
        { question: 'What is unsupervised learning?', options: ['Finding patterns in data without labeled outputs', 'Learning with labeled training data', 'Learning from rewards', 'Learning from expert demonstrations'], correctIndex: 0, explanation: 'Unsupervised learning finds hidden patterns in unlabeled data, unlike supervised learning which uses labeled examples.' },
      ],
    },
    {
      id: 'ml-overfitting',
      slug: 'overfitting-prevention',
      title: 'Overfitting & Validation',
      description: 'The #1 problem in financial ML — fitting noise, not signal.',
      commands: ['feature', 'feature importance'],
      steps: [
        { instruction: 'Check for overfitting: `ml validate --model lr --method cross-val`', command: 'ml validate --model lr --method cross-val', expectedOutput: 'Cross-validation scores with train/test performance comparison' },
        { instruction: 'Overfitting means your model memorizes noise instead of learning the true signal.' },
        { instruction: 'Use train/test splits, cross-validation, and regularization to prevent overfitting.' },
      ],
      quiz: [
        { question: 'What is overfitting in machine learning?', options: ['Model performs well on training data but poorly on new data', 'Model performs poorly on all data', 'Model takes too long to train', 'Model uses too many features'], correctIndex: 0, explanation: 'Overfitting occurs when a model learns noise in the training data, resulting in poor generalization to unseen data.' },
      ],
    },
  ],
}
