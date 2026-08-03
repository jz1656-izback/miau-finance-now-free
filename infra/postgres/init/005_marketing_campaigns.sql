-- Marketing Campaign Seed Data
-- Run: docker exec -i miau-finance-db-1 psql -U miau -d miau < backend/postgres/init/005_marketing_campaigns.sql

-- Generate sample sessions with UTM campaign data
INSERT INTO visitor_sessions (session_id, host, start_time, end_time, page_views, landing_page, ip_address, country, user_agent, browser, os, device_type, is_active)
SELECT
  'camp_sess_' || g || '_' || c,
  'miau.finance',
  NOW() - INTERVAL '1 day' * (random() * 30)::int,
  NOW() - INTERVAL '1 day' * (random() * 30)::int + INTERVAL '1 minute' * (random() * 15)::int,
  (random() * 8 + 1)::int,
  CASE (random() * 5)::int
    WHEN 0 THEN '/' WHEN 1 THEN '/pricing' WHEN 2 THEN '/features'
    WHEN 3 THEN '/blog' WHEN 4 THEN '/papers' ELSE '/'
  END,
  '192.168.' || (random() * 255)::int || '.' || (random() * 255)::int,
  CASE (random() * 10)::int
    WHEN 0 THEN 'US' WHEN 1 THEN 'DE' WHEN 2 THEN 'GB' WHEN 3 THEN 'FR'
    WHEN 4 THEN 'JP' WHEN 5 THEN 'BR' WHEN 6 THEN 'IN' WHEN 7 THEN 'CA'
    WHEN 8 THEN 'AU' WHEN 9 THEN 'SG' ELSE 'US'
  END,
  'Mozilla/5.0 (campaign bot)',
  CASE (random() * 3)::int WHEN 0 THEN 'Chrome' WHEN 1 THEN 'Firefox' WHEN 2 THEN 'Safari' ELSE 'Chrome' END,
  CASE (random() * 2)::int WHEN 0 THEN 'macOS' WHEN 1 THEN 'Windows' ELSE 'Linux' END,
  CASE (random() * 2)::int WHEN 0 THEN 'desktop' WHEN 1 THEN 'mobile' ELSE 'tablet' END,
  false
FROM generate_series(1, 300) g,
  (VALUES ('cat-tuna-extravaganza'), ('pawborghini-launch'), ('miau-ai-revolution'),
          ('terminal-ninja'), ('purr-scription'), ('quantum-cat'),
          ('cbdc-meow'), ('papers-are-here'), ('meow-sive-update'),
          ('cats-in-space')) AS c(campaign)
ON CONFLICT (session_id) DO NOTHING;

-- Generate page views with UTM campaign data
INSERT INTO page_views (path, referrer, user_agent, ip_address, session_id, host, utm_source, utm_medium, utm_campaign, timestamp)
SELECT
  CASE (random() * 10)::int
    WHEN 0 THEN '/' WHEN 1 THEN '/pricing' WHEN 2 THEN '/features'
    WHEN 3 THEN '/blog' WHEN 4 THEN '/papers' WHEN 5 THEN '/docs'
    WHEN 6 THEN '/blog/why-cats-trade-better' WHEN 7 THEN '/pricing/pro'
    WHEN 8 THEN '/papers/43' WHEN 9 THEN '/papers/60' ELSE '/'
  END,
  CASE (random() * 3)::int
    WHEN 0 THEN 'https://twitter.com/cat_post' WHEN 1 THEN 'https://reddit.com/r/cats'
    WHEN 2 THEN 'https://news.ycombinator.com' ELSE NULL
  END,
  'Mozilla/5.0',
  '192.168.' || (random() * 255)::int || '.' || (random() * 255)::int,
  'camp_sess_' || g || '_' || c.campaign,
  'miau.finance',
  CASE (random() * 4)::int
    WHEN 0 THEN 'twitter' WHEN 1 THEN 'google' WHEN 2 THEN 'linkedin'
    WHEN 3 THEN 'reddit' ELSE 'direct'
  END,
  CASE (random() * 4)::int
    WHEN 0 THEN 'social' WHEN 1 THEN 'cpc' WHEN 2 THEN 'email'
    WHEN 3 THEN 'organic' ELSE 'direct'
  END,
  c.campaign,
  NOW() - INTERVAL '1 day' * (random() * 30)::int - INTERVAL '1 hour' * (random() * 8)::int
FROM generate_series(1, 300) g,
  (VALUES ('cat-tuna-extravaganza'), ('pawborghini-launch'), ('miau-ai-revolution'),
          ('terminal-ninja'), ('purr-scription'), ('quantum-cat'),
          ('cbdc-meow'), ('papers-are-here'), ('meow-sive-update'),
          ('cats-in-space')) AS c(campaign);

-- Add second page view per session (more realistic)
INSERT INTO page_views (path, referrer, user_agent, ip_address, session_id, host, utm_source, utm_medium, utm_campaign, timestamp)
SELECT
  CASE (random() * 8)::int
    WHEN 0 THEN '/pricing' WHEN 1 THEN '/blog' WHEN 2 THEN '/papers'
    WHEN 3 THEN '/docs' WHEN 4 THEN '/features' WHEN 5 THEN '/papers/60'
    WHEN 6 THEN '/pricing/pro' WHEN 7 THEN '/blog/ai-hedge-fund' ELSE '/'
  END,
  NULL, 'Mozilla/5.0',
  '192.168.' || (random() * 255)::int || '.' || (random() * 255)::int,
  'camp_sess_' || g || '_' || c.campaign,
  'miau.finance',
  c.utm_source, c.utm_medium, c.campaign,
  c.ts + INTERVAL '1 minute' * (random() * 5)::int
FROM (
  SELECT g, campaign,
    CASE (random() * 4)::int WHEN 0 THEN 'twitter' WHEN 1 THEN 'google' WHEN 2 THEN 'linkedin' WHEN 3 THEN 'reddit' ELSE 'direct' END AS utm_source,
    CASE (random() * 4)::int WHEN 0 THEN 'social' WHEN 1 THEN 'cpc' WHEN 2 THEN 'email' WHEN 3 THEN 'organic' ELSE 'direct' END AS utm_medium,
    NOW() - INTERVAL '1 day' * (random() * 30)::int - INTERVAL '1 hour' * (random() * 8)::int AS ts
  FROM generate_series(1, 200) g,
    (VALUES ('cat-tuna-extravaganza'), ('pawborghini-launch'), ('miau-ai-revolution'),
            ('terminal-ninja'), ('purr-scription'), ('quantum-cat'),
            ('cbdc-meow'), ('papers-are-here'), ('meow-sive-update'),
            ('cats-in-space')) AS c(campaign)
) c;

-- Generate conversions with campaign attribution
INSERT INTO conversions (conversion_type, page, referrer, value, utm_source, utm_medium, utm_campaign, session_id, timestamp)
SELECT
  CASE (random() * 5)::int
    WHEN 0 THEN 'signup' WHEN 1 THEN 'trial_start' WHEN 2 THEN 'cta_click'
    WHEN 3 THEN 'newsletter' WHEN 4 THEN 'pricing_view' ELSE 'signup'
  END,
  CASE (random() * 5)::int WHEN 0 THEN '/pricing' WHEN 1 THEN '/' WHEN 2 THEN '/features' WHEN 3 THEN '/blog' WHEN 4 THEN '/papers' ELSE '/pricing' END,
  CASE (random() * 3)::int WHEN 0 THEN 'https://twitter.com' WHEN 1 THEN 'https://google.com' WHEN 2 THEN 'https://linkedin.com' ELSE NULL END,
  CASE WHEN random() < 0.3 THEN (random() * 100 + 10)::numeric(10,2) ELSE NULL END,
  CASE (random() * 4)::int WHEN 0 THEN 'twitter' WHEN 1 THEN 'google' WHEN 2 THEN 'linkedin' WHEN 3 THEN 'reddit' ELSE 'direct' END,
  CASE (random() * 4)::int WHEN 0 THEN 'social' WHEN 1 THEN 'cpc' WHEN 2 THEN 'email' WHEN 3 THEN 'organic' ELSE 'direct' END,
  c.campaign,
  'camp_sess_' || g || '_' || c.campaign,
  NOW() - INTERVAL '1 day' * (random() * 30)::int - INTERVAL '1 hour' * (random() * 8)::int
FROM generate_series(1, 80) g,
  (VALUES ('cat-tuna-extravaganza'), ('pawborghini-launch'), ('miau-ai-revolution'),
          ('terminal-ninja'), ('purr-scription'), ('quantum-cat'),
          ('cbdc-meow'), ('papers-are-here'), ('meow-sive-update'),
          ('cats-in-space')) AS c(campaign);

-- Also create some tracked links for campaigns
INSERT INTO tracked_links (url, slug, short_url, title, campaign, source, medium, total_clicks, unique_visitors)
VALUES
  ('https://miau.finance/pricing', 'cat-tuna', 'https://miau.finance/go/cat-tuna', 'Cat Tuna Deal', 'cat-tuna-extravaganza', 'twitter', 'social', 542, 389),
  ('https://miau.finance/pricing/pro', 'pawborghini', 'https://miau.finance/go/pawborghini', 'Pawborghini Early Adopter', 'pawborghini-launch', 'google', 'cpc', 1287, 901),
  ('https://miau.finance/ai', 'miau-ai', 'https://miau.finance/go/miau-ai', 'AI Revolution', 'miau-ai-revolution', 'linkedin', 'social', 876, 654),
  ('https://miau.finance/features', 'terminal-ninja', 'https://miau.finance/go/terminal-ninja', 'Become a Terminal Ninja', 'terminal-ninja', 'reddit', 'social', 234, 198),
  ('https://miau.finance/papers', 'read-papers', 'https://miau.finance/go/read-papers', '70 MiauPapers', 'papers-are-here', 'twitter', 'organic', 1567, 1123);
