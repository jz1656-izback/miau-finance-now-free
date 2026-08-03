import { useQuery } from '@tanstack/react-query'
import type {
  AnalyticsOverview, PageAnalytics, ReferrerAnalytics,
  CampaignAnalytics, TrendPoint, Conversion,
  RealtimeSnapshot, GeoLocation, DeviceAnalytics, ComparisonData,
  TrackedLink, LinkClick,
  Experiment, ExperimentVariant,
  MarketingAlert, AlertHistoryItem,
} from '../types'

const BASE = '/api/v1/marketing'

async function fetchJSON<T>(url: string): Promise<T> {
  const token = localStorage.getItem('miau_token')
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(url, { headers })
  if (!res.ok) {
    if (res.status === 401) {
      localStorage.removeItem('miau_token')
      window.dispatchEvent(new CustomEvent('auth:unauthorized'))
    }
    throw new Error(`API error: ${res.status}`)
  }
  return res.json()
}

async function postJSON<T>(url: string, body: unknown): Promise<T> {
  const token = localStorage.getItem('miau_token')
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) })
  if (!res.ok) {
    if (res.status === 401) {
      localStorage.removeItem('miau_token')
      window.dispatchEvent(new CustomEvent('auth:unauthorized'))
    }
    throw new Error(`API error: ${res.status}`)
  }
  return res.json()
}

export function useStats(period = 30) {
  return useQuery<AnalyticsOverview>({
    queryKey: ['marketing', 'stats', period],
    queryFn: () => fetchJSON(`${BASE}/stats?period=${period}`),
  })
}

export function usePages(period = 30, limit = 50) {
  return useQuery<PageAnalytics[]>({
    queryKey: ['marketing', 'pages', period, limit],
    queryFn: () => fetchJSON(`${BASE}/pages?period=${period}&limit=${limit}`),
  })
}

export function useReferrers(period = 30) {
  return useQuery<ReferrerAnalytics[]>({
    queryKey: ['marketing', 'referrers', period],
    queryFn: () => fetchJSON(`${BASE}/referrers?period=${period}`),
  })
}

export function useCampaigns(period = 30) {
  return useQuery<CampaignAnalytics[]>({
    queryKey: ['marketing', 'campaigns', period],
    queryFn: () => fetchJSON(`${BASE}/campaigns?period=${period}`),
  })
}

export function useTrends(period = 30) {
  return useQuery<TrendPoint[]>({
    queryKey: ['marketing', 'trends', period],
    queryFn: () => fetchJSON(`${BASE}/trends?period=${period}`),
  })
}

export function useConversions(period = 30, limit = 100) {
  return useQuery<Conversion[]>({
    queryKey: ['marketing', 'conversions', period, limit],
    queryFn: () => fetchJSON(`${BASE}/conversions?period=${period}&limit=${limit}`),
  })
}

export function useRealtime() {
  return useQuery<RealtimeSnapshot>({
    queryKey: ['marketing', 'realtime'],
    queryFn: () => fetchJSON(`${BASE}/realtime`),
    refetchInterval: 15_000,
  })
}

export function useGeo(period = 30) {
  return useQuery<GeoLocation[]>({
    queryKey: ['marketing', 'geo', period],
    queryFn: () => fetchJSON(`${BASE}/geo?period=${period}`),
  })
}

export function useDevices(period = 30) {
  return useQuery<DeviceAnalytics[]>({
    queryKey: ['marketing', 'devices', period],
    queryFn: () => fetchJSON(`${BASE}/devices?period=${period}`),
  })
}

export function useCompare(period = 30) {
  return useQuery<ComparisonData>({
    queryKey: ['marketing', 'compare', period],
    queryFn: () => fetchJSON(`${BASE}/compare?period=${period}`),
  })
}

export function useLinks() {
  return useQuery<TrackedLink[]>({
    queryKey: ['marketing', 'links'],
    queryFn: () => fetchJSON(`${BASE}/links`),
  })
}

export function useLinkClicks(linkId: string, period = 30) {
  return useQuery<LinkClick[]>({
    queryKey: ['marketing', 'links', linkId, 'clicks', period],
    queryFn: () => fetchJSON(`${BASE}/links/${linkId}/clicks?period=${period}`),
    enabled: !!linkId,
  })
}

export function useCreateLink() {
  return (data: { url: string; slug?: string; title?: string; campaign?: string; source?: string; medium?: string }) =>
    postJSON(`${BASE}/links`, data)
}

export function useExperiments() {
  return useQuery<Experiment[]>({
    queryKey: ['marketing', 'experiments'],
    queryFn: () => fetchJSON(`${BASE}/experiments`),
  })
}

export function useExperimentResults(id: string) {
  return useQuery<{ experiment: Experiment; results: ExperimentVariant[] }>({
    queryKey: ['marketing', 'experiments', id, 'results'],
    queryFn: () => fetchJSON(`${BASE}/experiments/${id}/results`),
    enabled: !!id,
  })
}

export function useCreateExperiment() {
  return (data: { name: string; page: string; description?: string; metric?: string; min_sample_size?: number }) =>
    postJSON(`${BASE}/experiments`, data)
}

export function useAlerts() {
  return useQuery<MarketingAlert[]>({
    queryKey: ['marketing', 'alerts'],
    queryFn: () => fetchJSON(`${BASE}/alerts`),
  })
}

export function useAlertHistory(limit = 50) {
  return useQuery<AlertHistoryItem[]>({
    queryKey: ['marketing', 'alerts', 'history', limit],
    queryFn: () => fetchJSON(`${BASE}/alerts/history?limit=${limit}`),
  })
}

export function useCreateAlert() {
  return (data: { name: string; metric: string; condition: string; threshold: number; period_minutes?: number; channel?: string; webhook_url?: string }) =>
    postJSON(`${BASE}/alerts`, data)
}

export function useToggleAlert() {
  return (alertId: string, active: boolean) =>
    postJSON(`${BASE}/alerts/${alertId}/toggle?active=${active}`, {})
}
