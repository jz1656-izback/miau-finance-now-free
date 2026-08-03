export interface AnalyticsOverview {
  total_visitors: number
  total_page_views: number
  bounce_rate: number
  avg_session_duration: number
  conversion_rate: number
  active_sessions: number
  total_conversions: number
}

export interface PageAnalytics {
  path: string
  views: number
  unique_views: number
  avg_time_on_page: number
  bounce_rate: number
}

export interface ReferrerAnalytics {
  source: string
  visitors: number
  page_views: number
  bounce_rate: number
  conversions: number
}

export interface CampaignAnalytics {
  campaign: string
  source: string
  medium: string
  visitors: number
  page_views: number
  conversions: number
  conversion_rate: number
  revenue: number
}

export interface TrendPoint {
  date: string
  visitors: number
  page_views: number
  conversions: number
}

export interface Conversion {
  id: string
  conversion_type: string
  page: string | null
  referrer: string | null
  value: number | null
  utm_source: string | null
  utm_medium: string | null
  utm_campaign: string | null
  timestamp: string
}

export interface RealtimeSnapshot {
  active_sessions: number
  page_views_last_minute: number
  page_views_last_5_minutes: number
  conversions_last_hour: number
  top_page_current: string | null
  recent_events: RealtimeEvent[]
  hourly_breakdown: HourlyBucket[]
}

export interface RealtimeEvent {
  id: string
  event: string
  path: string
  timestamp: string
  session_id?: string
  host?: string
  conversion_type?: string | null
}

export interface HourlyBucket {
  hour: string
  page_views: number
  visitors: number
}

export interface GeoLocation {
  country: string
  country_code: string
  visitors: number
  page_views: number
  lat: number
  lng: number
}

export interface DeviceAnalytics {
  device_type: string
  visitors: number
  page_views: number
  percentage: number
}

export interface ComparisonData {
  current: { visitors: number; page_views: number; conversions: number; bounce_rate: number; avg_session_duration: number }
  previous: { visitors: number; page_views: number; conversions: number; bounce_rate: number; avg_session_duration: number }
}

export interface TrackedLink {
  id: string
  url: string
  slug: string
  short_url: string
  title: string | null
  campaign: string | null
  source: string | null
  medium: string | null
  total_clicks: number
  unique_visitors: number
  created_at: string
  created_by: string | null
}

export interface LinkClick {
  id: string
  link_id: string
  ip_address: string | null
  user_agent: string | null
  country: string | null
  timestamp: string
}

export interface Experiment {
  id: string
  name: string
  page: string
  description: string | null
  metric: string
  min_sample_size: number
  status: string
  created_at: string
  created_by: string | null
  variants: ExperimentVariant[]
  total_participants: number
}

export interface ExperimentVariant {
  id: string
  name: string
  is_control: boolean
  traffic_pct: number
  participants: number
  conversions: number
  conversion_rate: number
  improvement: number | null
  is_winner: boolean
  confidence: number | null
}

export interface MarketingAlert {
  id: string
  name: string
  metric: string
  condition: string
  threshold: number
  period_minutes: number
  channel: string
  webhook_url: string | null
  active: boolean
  last_fired: string | null
  created_at: string
  created_by: string | null
}

export interface AlertHistoryItem {
  id: string
  alert_id: string
  alert_name: string
  metric_value: number
  threshold: number
  triggered_at: string
}
