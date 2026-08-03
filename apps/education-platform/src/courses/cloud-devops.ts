import type { Course } from '../lib/types'

export const cloudDevops: Course = {
  id: 'cloud-devops-finance',
  slug: 'cloud-and-devops-for-finance',
  title: 'Cloud & DevOps for Finance',
  description: 'Deploying trading systems, Docker, CI/CD, and monitoring — the cat automates everything except naptime.',
  category: 'DevOps',
  difficulty: 'advanced',
  icon: '☁️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'devops-cloud',
      slug: 'cloud-infrastructure-trading',
      title: 'Cloud Infrastructure for Trading',
      description: 'AWS, GCP, and Azure for quant systems.',
      commands: ['deploy', 'deploy infra'],
      steps: [
        { instruction: 'Deploy cloud infrastructure: `deploy infra --provider aws --region us-east-1 --services ec2,rds,elasticache`', command: 'deploy infra --provider aws --region us-east-1 --services ec2,rds,elasticache', expectedOutput: 'Cloud infrastructure deployed: 3 EC2 instances, 1 RDS cluster, 1 ElastiCache node' },
        { instruction: 'Cloud services let you scale trading infrastructure on demand.' },
        { instruction: 'The cat\'s cloud bill is mostly tuna server costs.' },
      ],
      quiz: [
        { question: 'Why use cloud infrastructure for trading systems?', options: ['Elastic scaling, global deployment, and managed services', 'Cloud is always cheaper than on-premise', 'Cloud eliminates all latency', 'Cloud requires no security configuration'], correctIndex: 0, explanation: 'Cloud provides on-demand compute, global regions for low-latency access, and managed services that reduce operational overhead.' },
      ],
    },
    {
      id: 'devops-docker',
      slug: 'docker-containerization',
      title: 'Docker & Containerization',
      description: 'Packaging quant models in containers.',
      commands: ['docker', 'docker build'],
      steps: [
        { instruction: 'Build a container for your trading bot: `docker build --file Dockerfile.trading --tag trading-bot:latest`', command: 'docker build --file Dockerfile.trading --tag trading-bot:latest', expectedOutput: 'Docker image built: trading-bot:latest (2.1 GB)' },
        { instruction: 'Containers ensure your strategy runs the same everywhere.' },
        { instruction: 'The cat containers its food — separate bowls for wet and dry.' },
      ],
      quiz: [
        { question: 'What problem do containers solve in quant development?', options: ['Reproducible environments across machines', 'Faster trading execution', 'Better prediction models', 'Larger data storage'], correctIndex: 0, explanation: 'Containers bundle code, dependencies, and configuration so the same environment runs identically everywhere.' },
      ],
    },
    {
      id: 'devops-cicd',
      slug: 'ci-cd-pipelines',
      title: 'CI/CD Pipelines',
      description: 'Automated testing and deployment.',
      commands: ['ci', 'ci run'],
      steps: [
        { instruction: 'Run a CI pipeline: `ci run --branch develop --tests all`', command: 'ci run --branch develop --tests all', expectedOutput: 'CI pipeline started: linting, unit tests, integration tests, deploy (estimated 12m)' },
        { instruction: 'CI/CD catches bugs before they hit production.' },
        { instruction: 'The cat\'s CI pipeline checks: does it compile? Does it purr?' },
      ],
      quiz: [
        { question: 'What is the main benefit of a CI/CD pipeline?', options: ['Automated testing and deployment reduces human error', 'It writes code automatically', 'It replaces the need for code review', 'It optimizes trading strategies'], correctIndex: 0, explanation: 'CI/CD automates testing and deployment, catching issues early and enabling frequent, reliable releases.' },
      ],
    },
    {
      id: 'devops-monitor',
      slug: 'monitoring-alerting',
      title: 'Monitoring & Alerting',
      description: 'Keeping systems healthy 24/7.',
      commands: ['monitor', 'monitor dashboard'],
      steps: [
        { instruction: 'Set up system monitoring: `monitor dashboard --name trading-prod --metrics cpu,memory,latency,errors`', command: 'monitor dashboard --name trading-prod --metrics cpu,memory,latency,errors', expectedOutput: 'Monitoring dashboard trading-prod created with alert thresholds for all metrics' },
        { instruction: 'Set alerts for critical thresholds before they become incidents.' },
        { instruction: 'The cat monitors its food bowl with motion sensors — empty bowl detected, alert triggered.' },
      ],
      quiz: [
        { question: 'Why is monitoring critical for trading systems?', options: ['Latency spikes or downtime can cause significant financial loss', 'Monitoring makes the system run faster', 'It replaces the need for testing', 'It automatically fixes bugs'], correctIndex: 0, explanation: 'In trading, milliseconds matter — monitoring detects performance degradation before it causes financial damage.' },
      ],
    },
  ],
}
