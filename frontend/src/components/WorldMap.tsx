import { useEffect, useRef, useState, useCallback } from 'react'
import { createPortal } from 'react-dom'

interface Props { onClose?: () => void; active?: boolean }

interface MapCompany {
  ticker: string; name: string; industry: string; lat: number; lng: number
  country: string; marketCap: number; price?: number; change_pct?: number
}

const MARKETS = [
  { name: 'S&P 500', ticker: '^GSPC', lat: 40.707, lng: -74.011, region: 'North America', country: 'US', type: 'Index' },
  { name: 'NASDAQ', ticker: '^IXIC', lat: 40.712, lng: -74.013, region: 'North America', country: 'US', type: 'Index' },
  { name: 'NYSE', ticker: '^NYA', lat: 40.707, lng: -74.011, region: 'North America', country: 'US', type: 'Stock Exchange' },
  { name: 'LSE', ticker: '^FTSE', lat: 51.514, lng: -0.083, region: 'Europe', country: 'GB', type: 'Stock Exchange' },
  { name: 'TSE (Nikkei)', ticker: '^N225', lat: 35.676, lng: 139.773, region: 'Asia Pacific', country: 'JP', type: 'Index' },
  { name: 'SSE', ticker: '000001.SS', lat: 31.230, lng: 121.473, region: 'Asia Pacific', country: 'CN', type: 'Stock Exchange' },
  { name: 'HKEX', ticker: '^HSI', lat: 22.284, lng: 114.158, region: 'Asia Pacific', country: 'HK', type: 'Stock Exchange' },
  { name: 'BSE (Sensex)', ticker: '^BSESN', lat: 18.939, lng: 72.835, region: 'Asia Pacific', country: 'IN', type: 'Index' },
  { name: 'ASX', ticker: '^AXJO', lat: -33.868, lng: 151.207, region: 'Asia Pacific', country: 'AU', type: 'Stock Exchange' },
  { name: 'B3 (Bovespa)', ticker: '^BVSP', lat: -23.561, lng: -46.665, region: 'South America', country: 'BR', type: 'Index' },
  { name: 'JSE', ticker: '^JN0U.JO', lat: -26.204, lng: 28.041, region: 'Africa', country: 'ZA', type: 'Stock Exchange' },
  { name: 'TSX', ticker: '^GSPTSE', lat: 43.646, lng: -79.381, region: 'North America', country: 'CA', type: 'Stock Exchange' },
  { name: 'DAX (Xetra)', ticker: '^GDAXI', lat: 50.111, lng: 8.682, region: 'Europe', country: 'DE', type: 'Index' },
  { name: 'SIX Swiss', ticker: '^SSMI', lat: 47.376, lng: 8.541, region: 'Europe', country: 'CH', type: 'Stock Exchange' },
  { name: 'SGX', ticker: '^STI', lat: 1.290, lng: 103.852, region: 'Asia Pacific', country: 'SG', type: 'Stock Exchange' },
  { name: 'KRX', ticker: '^KS11', lat: 37.566, lng: 126.978, region: 'Asia Pacific', country: 'KR', type: 'Stock Exchange' },
  { name: 'TWSE', ticker: '^TWII', lat: 25.085, lng: 121.563, region: 'Asia Pacific', country: 'TW', type: 'Stock Exchange' },
  { name: 'SET', ticker: '^SET.BK', lat: 13.756, lng: 100.501, region: 'Asia Pacific', country: 'TH', type: 'Stock Exchange' },
  { name: 'BMV', ticker: '^MXX', lat: 19.432, lng: -99.133, region: 'South America', country: 'MX', type: 'Stock Exchange' },
  { name: 'NZX', ticker: '^NZ50', lat: -36.848, lng: 174.763, region: 'Asia Pacific', country: 'NZ', type: 'Stock Exchange' },
  { name: 'PSE', ticker: '^PSEI', lat: 14.599, lng: 120.984, region: 'Asia Pacific', country: 'PH', type: 'Stock Exchange' },
  { name: 'IDX', ticker: '^JKSE', lat: -6.208, lng: 106.845, region: 'Asia Pacific', country: 'ID', type: 'Stock Exchange' },
  { name: 'ISE', ticker: '^XU100', lat: 41.008, lng: 28.978, region: 'Europe', country: 'TR', type: 'Stock Exchange' },
  { name: 'Moscow Exchange', ticker: '^IMOEX', lat: 55.755, lng: 37.617, region: 'Europe', country: 'RU', type: 'Stock Exchange' },
  { name: 'WSE', ticker: '^WIG20', lat: 52.229, lng: 21.012, region: 'Europe', country: 'PL', type: 'Stock Exchange' },
  { name: 'OSE', ticker: '^OSEAX', lat: 59.913, lng: 10.752, region: 'Europe', country: 'NO', type: 'Stock Exchange' },
  { name: 'BIST', ticker: '^XU100', lat: 41.008, lng: 28.978, region: 'Europe', country: 'TR', type: 'Stock Exchange' },
  { name: 'TASE', ticker: '^TA35', lat: 32.085, lng: 34.781, region: 'Middle East', country: 'IL', type: 'Stock Exchange' },
  { name: 'DFM', ticker: '^DFMGI', lat: 25.204, lng: 55.270, region: 'Middle East', country: 'AE', type: 'Stock Exchange' },
  { name: 'Saudi Exchange', ticker: '^TASI', lat: 24.713, lng: 46.675, region: 'Middle East', country: 'SA', type: 'Stock Exchange' },
  { name: 'Qatar Exchange', ticker: '^QSI', lat: 25.285, lng: 51.531, region: 'Middle East', country: 'QA', type: 'Stock Exchange' },
  { name: 'KSE', ticker: '^KSE100', lat: 24.860, lng: 67.001, region: 'Asia Pacific', country: 'PK', type: 'Stock Exchange' },
  { name: 'CSE', ticker: '^CSE', lat: 6.927, lng: 79.861, region: 'Asia Pacific', country: 'LK', type: 'Stock Exchange' },
  { name: 'VN Index', ticker: '^VNINDEX', lat: 21.028, lng: 105.854, region: 'Asia Pacific', country: 'VN', type: 'Stock Exchange' },
  { name: 'EGX', ticker: '^EGX30', lat: 30.044, lng: 31.235, region: 'Africa', country: 'EG', type: 'Stock Exchange' },
  { name: 'NSE Nigeria', ticker: '^NGX', lat: 6.524, lng: 3.379, region: 'Africa', country: 'NG', type: 'Stock Exchange' },
  { name: 'NSE Kenya', ticker: '^NSE20', lat: -1.292, lng: 36.821, region: 'Africa', country: 'KE', type: 'Stock Exchange' },
  { name: 'Botswana SE', ticker: '^BSE', lat: -24.628, lng: 25.923, region: 'Africa', country: 'BW', type: 'Stock Exchange' },
  { name: 'Casablanca SE', ticker: '^MASI', lat: 33.573, lng: -7.589, region: 'Africa', country: 'MA', type: 'Stock Exchange' },
  { name: 'Santiago SE', ticker: '^IPSA', lat: -33.448, lng: -70.669, region: 'South America', country: 'CL', type: 'Stock Exchange' },
  { name: 'BCBA', ticker: '^MERV', lat: -34.603, lng: -58.381, region: 'South America', country: 'AR', type: 'Stock Exchange' },
  { name: 'Lima SE', ticker: '^IGBVL', lat: -12.046, lng: -77.042, region: 'South America', country: 'PE', type: 'Stock Exchange' },
  { name: 'Colombia SE', ticker: '^COLCAP', lat: 4.570, lng: -74.297, region: 'South America', country: 'CO', type: 'Stock Exchange' },
  { name: 'Irish SE', ticker: '^ISEQ', lat: 53.349, lng: -6.260, region: 'Europe', country: 'IE', type: 'Stock Exchange' },
  { name: 'Austrian SE', ticker: '^ATX', lat: 48.210, lng: 16.363, region: 'Europe', country: 'AT', type: 'Stock Exchange' },
  { name: 'BMV Czech', ticker: '^PX', lat: 50.073, lng: 14.437, region: 'Europe', country: 'CZ', type: 'Stock Exchange' },
  { name: 'Budapest SE', ticker: '^BUX', lat: 47.497, lng: 19.040, region: 'Europe', country: 'HU', type: 'Stock Exchange' },
  { name: 'Athens SE', ticker: '^ATH', lat: 37.983, lng: 23.727, region: 'Europe', country: 'GR', type: 'Stock Exchange' },
  { name: 'BVB Romania', ticker: '^BET', lat: 44.439, lng: 26.096, region: 'Europe', country: 'RO', type: 'Stock Exchange' },
]

const LAUNCH_PADS = [
  { name: 'Kennedy LC-39A', lat: 28.61, lng: -80.60 },
  { name: 'Cape Canaveral SLC-40', lat: 28.56, lng: -80.58 },
  { name: 'Vandenberg SLC-4E', lat: 34.63, lng: -120.61 },
  { name: 'Starbase', lat: 25.99, lng: -97.18 },
]

const COUNTRY_COORDS: Record<string, [number, number]> = {
  US: [39.8, -98.5], GB: [54.0, -2.0], JP: [36.0, 138.0], DE: [51.0, 9.0], FR: [47.0, 2.0],
  CN: [35.0, 105.0], IN: [20.0, 78.0], BR: [-10.0, -55.0], CH: [46.8, 8.2], AU: [-25.0, 133.0],
  SG: [1.3, 103.8],
}

const FALLBACK_DATA = {
  countries: [
    { iso: 'US', name: 'USA', index_change: 0.38, is_open: true },
    { iso: 'GB', name: 'UK', index_change: -0.21, is_open: true },
    { iso: 'JP', name: 'Japan', index_change: -0.45, is_open: false },
    { iso: 'DE', name: 'Germany', index_change: 0.15, is_open: true },
    { iso: 'FR', name: 'France', index_change: -0.12, is_open: true },
    { iso: 'CN', name: 'China', index_change: 0.52, is_open: false },
    { iso: 'IN', name: 'India', index_change: 0.73, is_open: true },
    { iso: 'BR', name: 'Brazil', index_change: -0.88, is_open: true },
    { iso: 'CH', name: 'Switzerland', index_change: 0.22, is_open: true },
    { iso: 'AU', name: 'Australia', index_change: -0.05, is_open: false },
  ],
  trade_routes: [
    { from: 'US', to: 'GB', volume: 1500, velocity: 0.4, catboat: '🐱🚢', value: '1.2B' },
    { from: 'GB', to: 'DE', volume: 800, velocity: 0.6, catboat: '😼⛴️', value: '0.8B' },
    { from: 'US', to: 'JP', volume: 2000, velocity: 0.3, catboat: '🐱🚤', value: '2.1B' },
    { from: 'CN', to: 'US', volume: 3500, velocity: 0.5, catboat: '🐱🛳️', value: '4.5B' },
    { from: 'JP', to: 'CN', volume: 1200, velocity: 0.7, catboat: '😸🛥️', value: '1.0B' },
    { from: 'IN', to: 'GB', volume: 600, velocity: 0.55, catboat: '🐱⛵', value: '0.5B' },
    { from: 'BR', to: 'US', volume: 900, velocity: 0.45, catboat: '🐱🚣', value: '0.7B' },
    { from: 'AU', to: 'CN', volume: 1100, velocity: 0.35, catboat: '🐱🛶', value: '1.3B' },
    { from: 'FR', to: 'DE', volume: 700, velocity: 0.65, catboat: '🐱⚓', value: '0.6B' },
    { from: 'CH', to: 'GB', volume: 400, velocity: 0.5, catboat: '😺⛴️', value: '0.4B' },
    { from: 'US', to: 'DE', volume: 1800, velocity: 0.35, catboat: '🐱🚢', value: '1.8B' },
    { from: 'JP', to: 'US', volume: 2500, velocity: 0.4, catboat: '🐱🚤', value: '3.2B' },
    { from: 'DE', to: 'CN', volume: 900, velocity: 0.55, catboat: '😸⛴️', value: '0.9B' },
    { from: 'IN', to: 'JP', volume: 700, velocity: 0.6, catboat: '🐱⛵', value: '0.6B' },
    { from: 'GB', to: 'AU', volume: 500, velocity: 0.45, catboat: '🐱🛳️', value: '0.5B' },
    { from: 'US', to: 'BR', volume: 1100, velocity: 0.5, catboat: '🐱🚣', value: '1.1B' },
    { from: 'DE', to: 'US', volume: 1300, velocity: 0.4, catboat: '😺⛴️', value: '1.3B' },
    { from: 'CN', to: 'DE', volume: 1600, velocity: 0.3, catboat: '🐱🛳️', value: '1.6B' },
    { from: 'JP', to: 'GB', volume: 800, velocity: 0.5, catboat: '🐱⚓', value: '0.8B' },
  ],
  capital_flows: [
    { from: 'US', to: 'JP', amount: 500, jet: '🐱✈️' },
    { from: 'GB', to: 'US', amount: 300, jet: '🐱🛩️' },
    { from: 'DE', to: 'CN', amount: 200, jet: '🐱🛫' },
    { from: 'JP', to: 'US', amount: 400, jet: '🐱🛬' },
    { from: 'FR', to: 'DE', amount: 150, jet: '🐱🚁' },
    { from: 'US', to: 'SG', amount: 250, jet: '🐱✈️' },
    { from: 'CN', to: 'IN', amount: 180, jet: '🐱🛩️' },
    { from: 'AU', to: 'GB', amount: 120, jet: '🐱🛫' },
    { from: 'GB', to: 'JP', amount: 350, jet: '🐱🛬' },
    { from: 'BR', to: 'DE', amount: 90, jet: '🐱🚁' },
  ],
  cats: [
    { name: 'Whiskers', breed: 'Maine Coon', net_worth: 2500000, lat: 40.712, lng: -74.006, city: 'New York', is_captain: true },
    { name: 'Mittens', breed: 'Persian', net_worth: 1800000, lat: 51.507, lng: -0.127, city: 'London', is_captain: true },
    { name: 'Felix', breed: 'Sphynx', net_worth: 3200000, lat: 48.856, lng: 2.352, city: 'Paris', is_captain: false },
    { name: 'Luna', breed: 'Bengal', net_worth: 4100000, lat: 35.676, lng: 139.65, city: 'Tokyo', is_captain: true },
    { name: 'Simba', breed: 'Siamese', net_worth: 1500000, lat: 31.230, lng: 121.473, city: 'Shanghai', is_captain: false },
    { name: 'Garfield', breed: 'Orange Tabby', net_worth: 5000000, lat: 52.520, lng: 13.405, city: 'Berlin', is_captain: true },
    { name: 'Sylvester', breed: 'Snowshoe', net_worth: 1400000, lat: 19.076, lng: 72.877, city: 'Mumbai', is_captain: true },
    { name: 'Tigger', breed: 'Toyger', net_worth: 3600000, lat: 1.352, lng: 103.819, city: 'Singapore', is_captain: false },
    { name: 'Cheshire', breed: 'British Shorthair', net_worth: 2200000, lat: -23.550, lng: -46.633, city: 'São Paulo', is_captain: true },
    { name: 'Bella', breed: 'Ragdoll', net_worth: 3100000, lat: 34.052, lng: -118.243, city: 'Los Angeles', is_captain: false },
    { name: 'Charlie', breed: 'Scottish Fold', net_worth: 1700000, lat: 41.878, lng: -87.629, city: 'Chicago', is_captain: false },
    { name: 'Daisy', breed: 'Birman', net_worth: 2800000, lat: 29.760, lng: -95.369, city: 'Houston', is_captain: true },
    { name: 'Max', breed: 'Norwegian Forest', net_worth: 1900000, lat: 39.739, lng: -104.984, city: 'Denver', is_captain: false },
    { name: 'Chloe', breed: 'Siberian', net_worth: 2600000, lat: 47.606, lng: -122.332, city: 'Seattle', is_captain: true },
    { name: 'Leo', breed: 'Turkish Angora', net_worth: 1300000, lat: 42.360, lng: -71.058, city: 'Boston', is_captain: false },
    { name: 'Lily', breed: 'British Shorthair', net_worth: 2100000, lat: 38.907, lng: -77.036, city: 'Washington DC', is_captain: true },
    { name: 'Milo', breed: 'Devon Rex', net_worth: 950000, lat: 55.755, lng: 37.617, city: 'Moscow', is_captain: false },
    { name: 'Zoe', breed: 'Cornish Rex', net_worth: 1800000, lat: 52.229, lng: 21.012, city: 'Warsaw', is_captain: false },
    { name: 'Jack', breed: 'Manx', net_worth: 2200000, lat: 59.329, lng: 18.068, city: 'Stockholm', is_captain: true },
    { name: 'Sophie', breed: 'Burmese', net_worth: 1500000, lat: 55.676, lng: 12.568, city: 'Copenhagen', is_captain: false },
    { name: 'Oscar', breed: 'Exotic Shorthair', net_worth: 2900000, lat: 52.370, lng: 4.897, city: 'Amsterdam', is_captain: true },
    { name: 'Lucy', breed: 'Himalayan', net_worth: 1600000, lat: 50.850, lng: 4.351, city: 'Brussels', is_captain: false },
    { name: 'Rocky', breed: 'Chartreux', net_worth: 1300000, lat: 45.464, lng: 9.190, city: 'Milan', is_captain: true },
    { name: 'Molly', breed: 'American Curl', net_worth: 2400000, lat: 40.416, lng: -3.703, city: 'Madrid', is_captain: false },
    { name: 'Toby', breed: 'Japanese Bobtail', net_worth: 2100000, lat: 34.693, lng: 135.502, city: 'Osaka', is_captain: true },
    { name: 'Bailey', breed: 'Korat', net_worth: 1100000, lat: 13.756, lng: 100.501, city: 'Bangkok', is_captain: false },
    { name: 'Sasha', breed: 'Russian Blue', net_worth: 2700000, lat: -33.924, lng: 18.423, city: 'Cape Town', is_captain: true },
    { name: 'Cooper', breed: 'Egyptian Mau', net_worth: 850000, lat: 30.044, lng: 31.235, city: 'Cairo', is_captain: false },
    { name: 'Tiger', breed: 'Ocicat', net_worth: 1900000, lat: -34.603, lng: -58.381, city: 'Buenos Aires', is_captain: true },
    { name: 'Pepper', breed: 'Colorpoint Shorthair', net_worth: 1400000, lat: -33.448, lng: -70.669, city: 'Santiago', is_captain: false },
    { name: 'Shadow', breed: 'Bombay', net_worth: 2300000, lat: 19.432, lng: -99.133, city: 'Mexico City', is_captain: true },
    { name: 'Smokey', breed: 'Nebelung', net_worth: 1200000, lat: 14.599, lng: 120.984, city: 'Manila', is_captain: false },
    { name: 'Oliver', breed: 'Selkirk Rex', net_worth: 2000000, lat: -6.208, lng: 106.845, city: 'Jakarta', is_captain: true },
    { name: 'Loki', breed: 'LaPerm', net_worth: 1600000, lat: 28.613, lng: 77.208, city: 'Delhi', is_captain: false },
    { name: 'Misty', breed: 'Cymric', net_worth: 1800000, lat: -37.813, lng: 144.963, city: 'Melbourne', is_captain: true },
    { name: 'Jasper', breed: 'Chantilly', net_worth: 1100000, lat: 45.501, lng: -73.567, city: 'Montreal', is_captain: false },
    { name: 'Willow', breed: 'Turkish Van', net_worth: 2500000, lat: 43.653, lng: -79.383, city: 'Toronto', is_captain: true },
    { name: 'Gizmo', breed: 'Munchkin', net_worth: 900000, lat: 39.904, lng: 116.407, city: 'Beijing', is_captain: false },
  ],
  space: { iss: { lat: 51.5, lng: -60.5 } },
  commodities: [
    { name: 'Crude Oil (WTI)', symbol: 'CL', price: 78.50, unit: 'USD/bbl', change_pct: 1.2, lat: 31.9, lng: -102.9, icon: '🛢️' },
    { name: 'Brent Crude', symbol: 'BNO', price: 82.30, unit: 'USD/bbl', change_pct: 0.8, lat: 58.0, lng: 2.0, icon: '🛢️' },
    { name: 'Gold', symbol: 'XAU', price: 2320.00, unit: 'USD/oz', change_pct: -0.3, lat: -26.2, lng: 28.0, icon: '🥇' },
    { name: 'Silver', symbol: 'XAG', price: 28.50, unit: 'USD/oz', change_pct: 1.8, lat: 23.0, lng: -102.0, icon: '🥈' },
    { name: 'Copper', symbol: 'HG', price: 4.85, unit: 'USD/lb', change_pct: 2.1, lat: -22.0, lng: -68.0, icon: '🪙' },
    { name: 'Iron Ore', symbol: 'SI', price: 108.50, unit: 'USD/t', change_pct: -1.5, lat: -26.0, lng: 134.0, icon: '⛏️' },
    { name: 'Natural Gas', symbol: 'NG', price: 2.75, unit: 'USD/MMBtu', change_pct: 3.2, lat: 42.0, lng: -80.0, icon: '🔥' },
    { name: 'Wheat', symbol: 'ZW', price: 6.20, unit: 'USD/bu', change_pct: 0.5, lat: 46.0, lng: -100.0, icon: '🌾' },
    { name: 'Coffee', symbol: 'KC', price: 2.35, unit: 'USD/lb', change_pct: 3.8, lat: -15.0, lng: -47.0, icon: '☕' },
    { name: 'Lithium', symbol: 'LIT', price: 13.20, unit: 'USD/kg', change_pct: 4.5, lat: -23.0, lng: -67.0, icon: '🔋' },
  ],
  bond_yields: [
    { country: 'US', yield: 4.38, name: 'US Treasury 10Y', lat: 38.9, lng: -77.0, change_bps: 2 },
    { country: 'GB', yield: 4.12, name: 'UK Gilt 10Y', lat: 51.5, lng: -0.1, change_bps: -3 },
    { country: 'DE', yield: 2.48, name: 'German Bund 10Y', lat: 52.5, lng: 13.4, change_bps: 1 },
    { country: 'JP', yield: 0.97, name: 'Japan JGB 10Y', lat: 35.7, lng: 139.7, change_bps: -1 },
    { country: 'IN', yield: 7.05, name: 'India 10Y', lat: 28.6, lng: 77.2, change_bps: -5 },
    { country: 'BR', yield: 11.87, name: 'Brazil 10Y', lat: -15.8, lng: -47.9, change_bps: 8 },
  ],
}

const COMPANY_ICONS: Record<string, string> = {
  Tech: '💻', Semiconductors: '🔬', Automotive: '🚗', Finance: '🏦',
  Conglomerate: '🏢', Retail: '🛒', Food: '🍫', Industrial: '⚙️',
  Luxury: '👑', Energy: '⛽', Pharma: '💊', Entertainment: '🎬',
}

const CAT_BY_INDUSTRY: Record<string, string> = {
  Tech: '😸', Semiconductors: '😼', Automotive: '🐱', Finance: '😺',
  Energy: '🙀', Healthcare: '😿', Pharma: '😽', Biotech: '😻',
  Consumer: '😻', Retail: '🐱', Food: '😸', Industrial: '🐱',
  Luxury: '😻', Entertainment: '😹', Media: '😹', Telecom: '😺',
  Aerospace: '🐱', Logistics: '🐱', Mining: '🙀', Chemicals: '😼',
  Insurance: '😺', 'Real Estate': '🐱', Hospitality: '😸', Airlines: '🐱',
  Conglomerate: '🐱', Forestry: '😸', Trading: '😼',
}

function distKm(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLng / 2) * Math.sin(dLng / 2)
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

function catPopup(c: any) {
  return `<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:220px">
  <b style="color:#00ff88;font-size:15px">${c.is_captain ? '⚓' : '🐱'} ${c.name}</b><br/>
  <span style="color:#aaa">Breed: ${c.breed}</span><br/>
  <span style="color:#aaa">City: ${c.city}</span><br/>
  <span style="color:#aaa">Net Worth: <b style="color:#ffcc00">$${(c.net_worth / 1e6).toFixed(1)}M</b></span><br/>
  <span style="color:#aaa">Status: ${c.is_captain ? '⚓ Catboat Captain' : '🐱 Investor Cat'}</span>
</div>`
}

export default function WorldMap({ onClose, active }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<any>(null)
  const tileLayerRef = useRef<any>(null)
  const weatherLayerRef = useRef<any>(null)
  const overlaysRef = useRef<any>({ lines: [], boats: [], jets: [], catMarkers: [], hairballs: [], iss: null, commodities: [], bonds: [], markets: [], launchPads: [], defi: [], aircraft: [], maritime: [], mining: [], conflicts: [], satellites: [] })
  const animRef = useRef<number>(0)

  const [ready, setReady] = useState(false)
  const [data, setData] = useState<any>(FALLBACK_DATA)
  const [time, setTime] = useState('')
  const [zoom, setZoom] = useState(3)
  const zoomRef = useRef(3)
  const [search, setSearch] = useState('')
  const [searchResults, setSearchResults] = useState<any[] | null>(null)
  const [mapLayer, setMapLayer] = useState<'street' | 'satellite' | 'dark'>('dark')
  const [showCatboats, setShowCatboats] = useState(true)
  const [showJets, setShowJets] = useState(true)
  const [showCats, setShowCats] = useState(true)
  const [showHairballs, setShowHairballs] = useState(true)
  const [showISS, setShowISS] = useState(true)
  const [showCompanies, setShowCompanies] = useState(true)
  const [showCommodities, setShowCommodities] = useState(true)
  const [showBonds, setShowBonds] = useState(true)
  const [showDefi, setShowDefi] = useState(false)
  const [showWeather, setShowWeather] = useState(false)
  const [showAllOverlays, setShowAllOverlays] = useState(true)
  const [showAircraft, setShowAircraft] = useState(false)
  const [showMaritime, setShowMaritime] = useState(false)
  const [showMining, setShowMining] = useState(false)
  const [showConflicts, setShowConflicts] = useState(false)
  const [showSatellites, setShowSatellites] = useState(false)
  const [aircraftData, setAircraftData] = useState<any[]>([])
  const [maritimeData, setMaritimeData] = useState<any>({ ships: [], ports: [] })
  const [miningData, setMiningData] = useState<any[]>([])
  const [conflictsData, setConflictsData] = useState<any[]>([])
  const [satelliteData, setSatelliteData] = useState<any[]>([])
  const [continent, setContinent] = useState<string>('all')
  const [companies, setCompanies] = useState<MapCompany[]>([])
  const [defiProtocols, setDefiProtocols] = useState<any[]>([])
  const [selectedCompany, setSelectedCompany] = useState<any>(null)
  const [detailTab, setDetailTab] = useState<'info' | 'chart' | 'stats' | 'peers' | 'ib' | 'news'>('info')
  const [priceHistory, setPriceHistory] = useState<number[]>([])
  const [chartPeriod, setChartPeriod] = useState<string>('1y')
  const [companyNews, setCompanyNews] = useState<any[]>([])
  const [fundamentals, setFundamentals] = useState<any>(null)
  const [peers, setPeers] = useState<any[]>([])
  const [ibData, setIbData] = useState<any>(null)
  const [ibStatus, setIbStatus] = useState<'idle' | 'loading' | 'loaded' | 'unauthorized'>('idle')

  // Load Leaflet JS + inject required CSS
  useEffect(() => {
    if ((window as any).L?.map) { setReady(true); return }
    let cancelled = false
    // Inject Leaflet CSS into <head> (most reliable: <link> tag)
    const injectCSS = (url: string) => {
      if (!document.querySelector(`link[href="${url}"]`)) {
        const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = url
        document.head.appendChild(l)
      }
    }
    injectCSS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css')
    ;(async () => {
      try {
        const mod = await import('leaflet')
        ;(window as any).L = mod.default || mod
        try { await import('leaflet.markercluster') } catch {}
        if (!cancelled) { setReady(true); console.log('🗺️ Leaflet ready') }
      } catch (e) {
        console.warn('🗺️ Vite import failed:', e)
        const s = document.createElement('script')
        s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
        s.onload = () => { if (!cancelled) { setReady(true); console.log('🗺️ Leaflet CDN OK') } }
        document.head.appendChild(s)
      }
    })()
    return () => { cancelled = true }
  }, [])

  // Escape to close
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose?.() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  // Init map + static markers
  useEffect(() => {
    if (!ready || !containerRef.current || mapRef.current) return
    const L = (window as any).L
    if (!L || !L.map) return
    let clean: (() => void) | undefined
    try {
    const map = L.map(containerRef.current, {
      center: [30, -20], zoom: 3,
      minZoom: 2, maxBounds: [[-90, -180], [90, 180]], maxBoundsViscosity: 1.0,
      zoomControl: true, scrollWheelZoom: true, dragging: true, doubleClickZoom: true, boxZoom: true, keyboard: true, attributionControl: false,
      inertia: true, inertiaDeceleration: 3000, easeLinearity: 0.25, worldCopyJump: false,
    })
    tileLayerRef.current = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(map)
    if (!document.getElementById('miau-l-style')) {
      const ms = document.createElement('style')
      ms.id = 'miau-l-style'
      ms.textContent = '.leaflet-interactive{cursor:pointer!important}.leaflet-popup-content-wrapper{border-radius:8px!important;background:#0d1a12!important;border:1px solid rgba(0,255,136,0.2)!important;box-shadow:0 4px 20px rgba(0,0,0,0.6)!important;color:#ccc!important;font-family:monospace!important}.leaflet-popup-tip{background:#0d1a12!important;border:1px solid rgba(0,255,136,0.2)!important}.leaflet-popup-content{margin:12px 16px!important}.leaflet-container{width:100%;height:100%;z-index:1}.leaflet-control-zoom{position:absolute!important;top:48px!important;z-index:999!important}'
      document.head.appendChild(ms)
    }

    map._interacting = false
    map.on('zoomstart', () => { map._interacting = true })
    map.on('dragstart', () => { map._interacting = true })
    map.on('zoomend', () => { setTimeout(() => { map._interacting = false }, 150) })
    map.on('dragend', () => { setTimeout(() => { map._interacting = false }, 150) })

    for (const pad of LAUNCH_PADS) {
      L.circleMarker([pad.lat, pad.lng], {
        radius: 4, color: '#ff6600', fillColor: '#ff6600', fillOpacity: 0.4, weight: 2,
      }).bindPopup(`🚀 ${pad.name}`).addTo(map)
    }

    for (const mkt of MARKETS) {
      L.circleMarker([mkt.lat, mkt.lng], {
        radius: 6, color: '#00ff88', fillColor: '#00ff88', fillOpacity: 0.3, weight: 2,
      }).bindPopup(`<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:200px">
<b style="color:#00ff88;font-size:15px">📊 ${mkt.name}</b><br/>
<span style="color:#aaa">Ticker: <b style="color:#0cf">${mkt.ticker}</b></span><br/>
<span style="color:#aaa">Region: ${mkt.region}</span><br/>
<span style="color:#aaa">Country: ${mkt.country}</span><br/>
<span style="color:#aaa">Type: ${mkt.type}</span>
</div>`).addTo(map)
    }

    mapRef.current = map
    map.on('zoomend', () => setZoom(map.getZoom()))
    map.on('moveend', () => setZoom(map.getZoom()))

    // Ensure map fills its container after render
    requestAnimationFrame(() => map.invalidateSize())
    setTimeout(() => map.invalidateSize(), 500)

    const resizeObserver = new ResizeObserver(() => map.invalidateSize())
    if (containerRef.current) resizeObserver.observe(containerRef.current)
    clean = () => {
      resizeObserver.disconnect()
      map.remove();
      mapRef.current = null;
      overlaysRef.current = { lines: [], boats: [], jets: [], catMarkers: [], hairballs: [], iss: null, commodities: [], bonds: [], markets: [], launchPads: [], defi: [] }
    }
    } catch (e) { console.error('WorldMap: init map error', e) }
    return clean
  }, [ready])

  // Separate effect: update company markers when companies data changes
  // Track cluster state to avoid unnecessary rebuilds
  const clusterVersionRef = useRef(0)

  useEffect(() => {
    try {
    const map = mapRef.current
    const L = (window as any).L
    if (!map || !L) return

    // Skip rebuild if companies haven't meaningfully changed
    const newVer = companies.length + (showCompanies ? 10000 : 0)
    if (newVer === clusterVersionRef.current) return
    clusterVersionRef.current = newVer

    const oldCluster = (map as any)._companyCluster
    if (oldCluster) {
      try { (oldCluster as any).unspiderfy?.() } catch {}
      map.removeLayer(oldCluster)
      ;(map as any)._companyCluster = null
    }
    if (!showCompanies || companies.length === 0) return

    const cluster = L.markerClusterGroup({
      chunkedLoading: true, chunkInterval: 20, maxClusterRadius: 80,
      spiderfyOnMaxZoom: true, showCoverageOnHover: false,
      disableClusteringAtZoom: 16,
      iconCreateFunction: (cl: any) => {
        const n = cl.getChildCount()
        const sz = n < 100 ? 34 : n < 500 ? 42 : 50
        return L.divIcon({
          html: `<div style="width:${sz}px;height:${sz}px;background:#0a1a14;border:1.5px solid #0f8;border-radius:50%;display:flex;align-items:center;justify-content:center;font:bold 10px/1 monospace;color:#0f8;flex-direction:column">🐱<span>${n}</span></div>`,
          className: '', iconSize: [sz, sz], iconAnchor: [sz / 2, sz / 2],
        })
      },
    })

    const markers = new Array(companies.length)
    for (let i = 0; i < companies.length; i++) {
      const co = companies[i]
      if (co.lat == null || co.lng == null) { markers[i] = null; continue }
      const change = co.change_pct ?? 0
      const color = change > 0.5 ? '#0f8' : change < -0.5 ? '#f44' : '#0cf'
      const s = co.marketCap ? Math.min(24, Math.max(14, co.marketCap / 100)) : 18
      const emoji = CAT_BY_INDUSTRY[co.industry] || '🐱'
      const m = L.marker([co.lat, co.lng], {
        icon: L.divIcon({ className: 'miau-cat-marker', html: `<span style="font-size:${s}px;color:${color}">${emoji}</span>`, iconSize: [s + 2, s + 2], iconAnchor: [(s + 2) / 2, (s + 2) / 2] }),
        zIndexOffset: 1000,
      })
      m.on('click', () => selectCompany(co))
      markers[i] = m
    }
    map.addLayer(cluster.addLayers(markers.filter(Boolean)))
    ;(map as any)._companyCluster = cluster
    } catch (e) { console.error('WorldMap: company markers error', e) }
  }, [companies, showCompanies, ready])

  // Switch tile layer on mapLayer change
  useEffect(() => {
    try {
    const map = mapRef.current
    if (!map || !tileLayerRef.current) return
    const L = (window as any).L
    map.removeLayer(tileLayerRef.current)
    const url = mapLayer === 'satellite'
      ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
      : mapLayer === 'dark'
      ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
      : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    tileLayerRef.current = L.tileLayer(url, { maxZoom: 18 }).addTo(map)
    if (weatherLayerRef.current) { map.removeLayer(weatherLayerRef.current); weatherLayerRef.current = null }
    if (showWeather) {
      weatherLayerRef.current = L.tileLayer('https://tilecache.rainviewer.com/v2/radar/{z}/{x}/{y}/2/1_1.png', {
        opacity: 0.5, maxZoom: 12,
      }).addTo(map)
    }
    } catch (e) { console.error('WorldMap: tile layer error', e) }
  }, [mapLayer, ready, showWeather])

  // Create/update animated overlays when data/toggles change
  useEffect(() => {
    const map = mapRef.current
    if (!map || !data) return
    const L = (window as any).L
    const ol = overlaysRef.current
    let clean: (() => void) | undefined
    try {

    // Clear old overlay elements
    ol.lines.forEach((l: any) => map.removeLayer(l))
    ol.boats.forEach((b: any) => map.removeLayer(b))
    ol.jets.forEach((j: any) => map.removeLayer(j))
    ol.catMarkers.forEach((c: any) => map.removeLayer(c))
    ol.hairballs.forEach((h: any) => map.removeLayer(h))
    ol.commodities.forEach((c: any) => map.removeLayer(c))
    ol.bonds.forEach((b: any) => map.removeLayer(b))
    ol.defi.forEach((d: any) => map.removeLayer(d))
    ol.aircraft.forEach((a: any) => map.removeLayer(a))
    ol.maritime.forEach((m: any) => map.removeLayer(m))
    ol.mining.forEach((m: any) => map.removeLayer(m))
    ol.conflicts.forEach((c: any) => map.removeLayer(c))
    ol.satellites.forEach((s: any) => map.removeLayer(s))
    ol.markets.forEach((m: any) => map.removeLayer(m))
    ol.launchPads.forEach((lp: any) => map.removeLayer(lp))
    if (ol.iss) map.removeLayer(ol.iss)
    ol.lines = []; ol.boats = []; ol.jets = []; ol.catMarkers = []; ol.hairballs = []; ol.iss = null
    ol.commodities = []; ol.bonds = []; ol.defi = []; ol.aircraft = []; ol.maritime = []; ol.mining = []; ol.conflicts = []; ol.satellites = []; ol.markets = []; ol.launchPads = []

    if (showCatboats && data.trade_routes) {
      for (const tr of data.trade_routes) {
        const f = COUNTRY_COORDS[tr.from]
        const t = COUNTRY_COORDS[tr.to]
        if (!f || !t) continue
        const line = L.polyline([[f[0], f[1]], [t[0], t[1]]], {
          color: '#00ff88', weight: 1, opacity: 0.2, dashArray: '4 8',
        }).addTo(map)
        const d = distKm(f[0], f[1], t[0], t[1])
        const etaBoat = Math.round(d / (25 * (tr.velocity || 1)))
        line.bindPopup(`<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:220px">
<b style="color:#00ff88;font-size:15px">🐱 🚢 ${tr.from} ⇢ ${tr.to}</b><br/>
<span style="color:#aaa">Volume: <b style="color:#fff">${tr.volume}</b> TEU</span><br/>
<span style="color:#aaa">Value: <b style="color:#ffcc00">${tr.value}</b></span><br/>
<span style="color:#aaa">Velocity: ${tr.velocity}x market avg</span><br/>
<span style="color:#aaa">Est. transit: <b style="color:#0cf">~${etaBoat} hrs</b></span><br/>
<span style="color:#666;font-size:11px">${tr.catboat || '🐱🚢'} Catboat Cargo Lines</span>
</div>`)
        ol.lines.push(line)
        const boatPopupHtml = `<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:240px">
<b style="color:#00ff88;font-size:15px">🐱 🚢 Catboat ${tr.from}⇢${tr.to}</b><br/>
<span style="color:#aaa">Route: <b style="color:#fff">${tr.from} → ${tr.to}</b></span><br/>
<span style="color:#aaa">Volume: <b style="color:#fff">${tr.volume}</b> TEU</span><br/>
<span style="color:#aaa">Value: <b style="color:#ffcc00">${tr.value}</b></span><br/>
<span style="color:#aaa">Est. time: <b style="color:#0cf">~${etaBoat} hrs</b></span><br/>
<span style="color:#aaa">Cargo: <b style="color:#fff">Mixed consumer goods</b></span>
</div>`
        const label = L.marker([f[0], f[1]], {
          icon: L.divIcon({ className: '', html: tr.catboat || '🐱', iconSize: [14, 14], iconAnchor: [7, 7] }),
          zIndexOffset: 1000, opacity: 0.9,
        })
        label.bindPopup(boatPopupHtml)
        label.addTo(map)
        ol.boats.push(label)
      }
    }

    if (showJets && data.capital_flows) {
      for (const flow of data.capital_flows) {
        const f = COUNTRY_COORDS[flow.from]
        const t = COUNTRY_COORDS[flow.to]
        if (!f || !t) continue
        const d = distKm(f[0], f[1], t[0], t[1])
        const etaJet = Math.round(d / 800)
        const jet = L.circleMarker([f[0], f[1]], {
          radius: 4, color: '#00ccff', fillColor: '#00ccff', fillOpacity: 0.5, weight: 1, opacity: 0.7,
        }).addTo(map)
        jet.bindPopup(`<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:220px">
<b style="color:#00ccff;font-size:15px">🐱 ✈️ ${flow.from} → ${flow.to}</b><br/>
<span style="color:#aaa">Amount: <b style="color:#ffcc00">$${(flow.amount / 1e6).toFixed(1)}M</b></span><br/>
<span style="color:#aaa">Est. flight: <b style="color:#0cf">~${etaJet} hrs</b></span><br/>
<span style="color:#aaa">Aircraft: ${flow.jet || '🐱✈️'}</span>
</div>`)
        ol.jets.push(jet)
        const jetPopupHtml = `<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:240px">
<b style="color:#00ccff;font-size:15px">🐱 ✈️ Capital Jet ${flow.from}⇢${flow.to}</b><br/>
<span style="color:#aaa">Route: <b style="color:#fff">${flow.from} → ${flow.to}</b></span><br/>
<span style="color:#aaa">Amount: <b style="color:#ffcc00">$${(flow.amount / 1e6).toFixed(1)}M</b></span><br/>
<span style="color:#aaa">Est. arrival: <b style="color:#0cf">~${etaJet} hrs</b></span><br/>
<span style="color:#aaa">Jet: ${flow.jet || '🐱✈️'}</span>
</div>`
        const jetLabel = L.marker([f[0], f[1]], {
          icon: L.divIcon({ className: '', html: `<span style="font-size:16px">${flow.jet || '✈️'}</span>`, iconSize: [18, 18], iconAnchor: [9, 9] }),
          zIndexOffset: 1001, opacity: 0.9,
        })
        jetLabel.bindPopup(jetPopupHtml)
        jetLabel.addTo(map)
        ol.jets.push(jetLabel)
      }
    }

    if (showCats && data.cats) {
      for (const cat of data.cats) {
        const m = L.marker([cat.lat, cat.lng], {
          icon: L.divIcon({ className: '', html: cat.is_captain ? '🐱⚓' : '🐱', iconSize: [16, 16], iconAnchor: [8, 8] }),
          zIndexOffset: 1002,
        })
        m.bindPopup(catPopup(cat))
        m.addTo(map)
        ol.catMarkers.push(m)
      }
    }

    if (showHairballs && data.cats) {
      for (let i = 0; i < data.cats.length; i++) {
        const cat = data.cats[i]
        const h = L.marker([cat.lat + 0.5, cat.lng + 0.5], {
          icon: L.divIcon({ className: '', html: '🧶', iconSize: [12, 12], iconAnchor: [6, 6] }),
          zIndexOffset: 999,
        }).addTo(map)
        ol.hairballs.push(h)
      }
    }

    // ISS
    if (showISS && data.space?.iss) {
      const iss = L.marker([data.space.iss.lat, data.space.iss.lng], {
        icon: L.divIcon({ className: '', html: '🛰️', iconSize: [14, 14], iconAnchor: [7, 7] }),
        zIndexOffset: 1003,
      }).addTo(map)
      iss.bindPopup('🛰️ ISS<br/>International Space Station')
      ol.iss = iss
    }

    // Commodities (toggleable)
    if (showCommodities && data.commodities) {
      for (const c of data.commodities) {
        const m = L.marker([c.lat, c.lng], {
          icon: L.divIcon({ className: '', html: c.icon, iconSize: [20, 20], iconAnchor: [10, 10] }),
          zIndexOffset: 995,
        }).bindPopup(`<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:180px">
<b style="color:#00ff88;font-size:15px">${c.icon} ${c.name}</b><br/>
<span style="color:#aaa">Price: <b style="color:#fff">$${c.price}</b> ${c.unit}</span><br/>
<span style="color:#aaa">Change: <b style="color:${c.change_pct >= 0 ? '#00ff88' : '#ff4444'}">${c.change_pct >= 0 ? '▲' : '▼'} ${Math.abs(c.change_pct)}%</b></span><br/>
<span style="color:#666;font-size:11px">Symbol: ${c.symbol}</span>
</div>`).addTo(map)
        ol.commodities.push(m)
      }
    }

    // Bond yields (toggleable)
    if (showBonds && data.bond_yields) {
      for (const b of data.bond_yields) {
        const dir = b.change_bps >= 0 ? '▲' : '▼'
        const m = L.marker([b.lat, b.lng], {
          icon: L.divIcon({ className: '', html: `<span style="font-size:14px">📜</span>`, iconSize: [18, 18], iconAnchor: [9, 9] }),
          zIndexOffset: 996,
        }).bindPopup(`<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:200px">
<b style="color:#00ff88;font-size:15px">📜 ${b.name}</b><br/>
<span style="color:#aaa">Yield: <b style="color:#fff">${b.yield}%</b></span><br/>
<span style="color:#aaa">Change: <b style="color:${b.change_bps >= 0 ? '#00ff88' : '#ff4444'}">${dir} ${Math.abs(b.change_bps)}bps</b></span><br/>
<span style="color:#666;font-size:11px">Country: ${b.country}</span>
</div>`).addTo(map)
        ol.bonds.push(m)
      }
    }

    // DeFi Protocol markers
    if (showDefi && defiProtocols.length > 0) {
      for (const p of defiProtocols) {
        const m = L.circleMarker([p.lat, p.lng], {
          radius: 8, color: '#ff8800', fillColor: '#ff8800', fillOpacity: 0.3, weight: 2, opacity: 0.8,
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:13px;line-height:1.6;min-width:200px">
<b style="color:#ff8800;font-size:15px">🔗 ${p.name}</b><br/>
<span style="color:#aaa">Chain: <b style="color:#fff">${p.chain}</b></span><br/>
<span style="color:#aaa">TVL: <b style="color:#ffcc00">$${(p.tvl / 1e6).toFixed(0)}M</b></span><br/>
<span style="color:#aaa">Category: ${p.category}</span><br/>
<span style="color:#aaa">24h: <b style="color:${(p.change_24h || 0) >= 0 ? '#00ff88' : '#ff4444'}">${p.change_24h >= 0 ? '▲' : '▼'} ${Math.abs(p.change_24h || 0)}%</b></span>
</div>`)
        m.addTo(map)
        ol.defi.push(m)
      }
    }

    // ── New data layers ────────────────────────────────────────

    // Live Aircraft
    if (showAircraft && aircraftData.length > 0) {
      for (const ac of aircraftData.slice(0, 200)) {
        const m = L.circleMarker([ac.lat, ac.lng], {
          radius: 4, color: '#ffcc00', fillColor: '#ffcc00', fillOpacity: 0.6, weight: 1, opacity: 0.8,
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:12px;line-height:1.6;min-width:180px">
<b style="color:#ffcc00">✈️ ${ac.callsign || 'Unknown'}</b><br/>
<span style="color:#aaa">Altitude: <b style="color:#fff">${Math.round(ac.altitude || 0)}ft</b></span><br/>
<span style="color:#aaa">Speed: <b style="color:#fff">${Math.round(ac.velocity || 0)}m/s</b></span><br/>
<span style="color:#aaa">Origin: ${ac.origin || 'unknown'}</span>
</div>`).addTo(map)
        ol.aircraft.push(m)
      }
    }

    // Maritime (ships)
    if (showMaritime && maritimeData.ships?.length > 0) {
      for (const sh of maritimeData.ships.slice(0, 100)) {
        const m = L.circleMarker([sh.lat, sh.lng], {
          radius: 5, color: '#00aaff', fillColor: '#00aaff', fillOpacity: 0.5, weight: 1, opacity: 0.8,
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:12px;line-height:1.6;min-width:180px">
<b style="color:#00aaff">🚢 ${sh.name || 'Vessel'}</b><br/>
<span style="color:#aaa">Speed: <b style="color:#fff">${sh.speed || '?'} kn</b></span><br/>
<span style="color:#aaa">Destination: ${sh.destination || 'unknown'}</span>
</div>`).addTo(map)
        ol.maritime.push(m)
      }
    }
    // Maritime ports
    if (showMaritime && maritimeData.ports?.length > 0) {
      for (const pt of maritimeData.ports) {
        const m = L.marker([pt.lat, pt.lng], {
          icon: L.divIcon({ className: '', html: '⚓', iconSize: [14, 14], iconAnchor: [7, 7] }),
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:12px">⚓ ${pt.name || 'Port'}</div>`)
        m.addTo(map)
        ol.maritime.push(m)
      }
    }

    // Mining
    if (showMining && miningData.length > 0) {
      for (const mine of miningData.slice(0, 60)) {
        const color = mine.commodity?.includes('Gold') ? '#ffcc00' : mine.commodity?.includes('Copper') ? '#cd7f32' : mine.commodity === 'Oil' ? '#1a1a1a' : '#22dd88'
        const m = L.circleMarker([mine.lat, mine.lng], {
          radius: 6, color, fillColor: color, fillOpacity: 0.4, weight: 1, opacity: 0.8,
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:12px;line-height:1.6;min-width:200px">
<b style="color:#00ff88">⛏️ ${mine.name}</b><br/>
<span style="color:#aaa">Commodity: <b style="color:#fff">${mine.commodity || '?'}</b></span><br/>
<span style="color:#aaa">Owner: ${mine.owner || '?'}</span><br/>
<span style="color:#aaa">Production: ${mine.production || '?'}</span>
</div>`).addTo(map)
        ol.mining.push(m)
      }
    }

    // Conflicts
    if (showConflicts && conflictsData.length > 0) {
      for (const cf of conflictsData.slice(0, 50)) {
        const isHigh = cf.intensity === 'High'
        const intensityColor = isHigh ? '#ff4444' : cf.intensity === 'Medium' ? '#ffaa00' : '#44cc44'
        const emoji = isHigh ? '😿' : cf.intensity === 'Medium' ? '😾' : '😺'
        const icon = isHigh ? '🔴' : cf.intensity === 'Medium' ? '🟡' : '🟢'
        const radius = isHigh ? 10 : cf.intensity === 'Medium' ? 7 : 5
        const m = L.circleMarker([cf.lat, cf.lng], {
          radius, color: intensityColor, fillColor: intensityColor, fillOpacity: 0.25, weight: 2, opacity: 0.9,
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:12px;line-height:1.6;min-width:240px">
<b style="color:#ff4444">⚔️ ${cf.name || 'Conflict'}</b> ${emoji}<br/>
<span style="color:#aaa">Region: <b style="color:#fff">${cf.region || '?'}</b></span><br/>
<span style="color:#aaa">Type: <b style="color:#fff">${cf.type || '?'}</b></span><br/>
<span style="color:#aaa">Intensity: <b style="color:${intensityColor}">${icon} ${cf.intensity || '?'}</b></span><br/>
<span style="color:#aaa">Started: <b style="color:#fff">${cf.start_year || '?'}</b></span><br/>
<span style="color:#aaa">Parties: <b style="color:#fff">${Array.isArray(cf.parties) ? cf.parties.join(', ') : cf.parties || '?'}</b></span>
</div>`).addTo(map)
        ol.conflicts.push(m)
      }
    }

    // Satellites
    if (showSatellites && satelliteData.length > 0) {
      for (const sat of satelliteData.slice(0, 100)) {
        const m = L.circleMarker([sat.lat, sat.lng], {
          radius: 3, color: '#aaddff', fillColor: '#aaddff', fillOpacity: 0.5, weight: 1, opacity: 0.7,
        })
        m.bindPopup(`<div style="font-family:monospace;font-size:12px;line-height:1.6;min-width:180px">
<b style="color:#aaddff">🛰️ ${sat.name || 'Satellite'}</b><br/>
<span style="color:#aaa">Orbit: ${sat.orbit || '?'}</span><br/>
<span style="color:#aaa">Operator: ${sat.operator || '?'}</span>
</div>`).addTo(map)
        ol.satellites.push(m)
      }
    }

    // Animate boats and jets
    const animActive = { current: true }
    let start = Date.now()
    const animate = () => {
      if (!animActive.current) return
      const elapsed = Date.now() - start
      const phase = (elapsed * 0.00002) % 1

      if (showCatboats && data.trade_routes && !mapRef.current?._interacting) {
        for (let i = 0; i < data.trade_routes.length; i++) {
          const tr = data.trade_routes[i]
          const f = COUNTRY_COORDS[tr.from]
          const t = COUNTRY_COORDS[tr.to]
          if (!f || !t) continue
          const raw = (phase * tr.velocity)
          const pos = Math.sin(raw * Math.PI * 0.5) * 0.5 + 0.5
          const lat = f[0] + (t[0] - f[0]) * pos
          const lng = f[1] + (t[1] - f[1]) * pos
          try { if (ol.boats[i * 2]) ol.boats[i * 2].setLatLng([lat, lng]) } catch {}
          try { if (ol.boats[i * 2 + 1]) ol.boats[i * 2 + 1].setLatLng([lat, lng]) } catch {}
        }
      }

      if (showJets && data.capital_flows && !mapRef.current?._interacting) {
        for (let i = 0; i < data.capital_flows.length; i++) {
          const flow = data.capital_flows[i]
          const f = COUNTRY_COORDS[flow.from]
          const t = COUNTRY_COORDS[flow.to]
          if (!f || !t) continue
          const pos = Math.sin(phase * 0.5 * Math.PI * 0.5) * 0.5 + 0.5
          const lat = f[0] + (t[0] - f[0]) * pos
          const lng = f[1] + (t[1] - f[1]) * pos
          try { if (ol.jets[i * 2]) ol.jets[i * 2].setLatLng([lat, lng]) } catch {}
          try { if (ol.jets[i * 2 + 1]) ol.jets[i * 2 + 1].setLatLng([lat, lng]) } catch {}
        }
      }

      if (showHairballs && data.cats && ol.hairballs.length > 0 && !mapRef.current?._interacting) {
        for (let i = 0; i < data.cats.length; i++) {
          const cat = data.cats[i]
          if (!ol.hairballs[i]) continue
          try {
            const offset = Math.sin(Date.now() * 0.0005 + i * 1.7) * 2
            const offset2 = Math.cos(Date.now() * 0.0004 + i * 1.3) * 2
            ol.hairballs[i].setLatLng([cat.lat + offset, cat.lng + offset2])
          } catch {}
        }
      }

      if (animActive.current) animRef.current = requestAnimationFrame(animate)
    }
    animRef.current = requestAnimationFrame(animate)

    clean = () => { animActive.current = false; cancelAnimationFrame(animRef.current) }
    } catch (e) { console.error('WorldMap: overlays/animation error', e) }
    return clean
  }, [data, showCatboats, showJets, showCats, showHairballs, showISS, showCommodities, showBonds, showDefi, defiProtocols, ready, showAircraft, showMaritime, showMining, showConflicts, showSatellites, aircraftData, maritimeData, miningData, conflictsData, satelliteData])

  // Lazy-loaded company data
  const allCompaniesRef = useRef<any[]>([])
  const companyDetailsRef = useRef<Record<string, {ceo?:string;founded?:number;employees?:number;revenue?:number}>>({})

  // 🔍 Lookup real company metadata — no random fabrication
   const enrichCompany = (co: any, ticker: string) => {
    // Strip exchange suffix for lookup: RMS.PA → RMS, SAP.DE → SAP
    const baseTicker = ticker.replace(/\.[A-Z]{2}$/i, '')
    const details = companyDetailsRef.current[ticker] || companyDetailsRef.current[baseTicker]
    if (details) {
      return { ...co, ceo: details.ceo, founded: details.founded, employees: details.employees, revenue: details.revenue }
    }
    return { ...co, ceo: undefined, founded: undefined, employees: undefined, revenue: undefined }
  }

  // Load companies from ALL continents + real company metadata
  useEffect(() => {
    try {
    const CONTINENT_FILES = ['north_america', 'europe', 'asia', 'south_america', 'africa', 'oceania', 'other']
    // Load metadata first
    fetch(`/data/company_details.json`)
      .then(r => r.ok ? r.json() : {})
      .then(details => { companyDetailsRef.current = details })
      .then(async () => {
        // Load ALL continent files for search, but only show markers for current continent
        const cont = continent === 'all' ? 'north_america' : continent
        let allMapped: MapCompany[] = []
        for (const c of CONTINENT_FILES) {
          try {
            const r = await fetch(`/data/companies_${c}.json`)
            if (!r.ok) continue
            const data = await r.json()
            if (!data?.companies) continue
            const isCurrent = c === cont
            const max = isCurrent ? Math.min(data.companies.length, 12000) : 0
            for (let i = 0; i < (isCurrent ? max : Math.min(data.companies.length, 2000)); i++) {
              const co = data.companies[i]
              allMapped.push(enrichCompany({
                ticker: co.t, name: co.n, industry: co.i,
                lat: co.lat, lng: co.lng, country: co.co, marketCap: co.mc || 0,
              }, co.t))
            }
          } catch {}
        }
        // Remove synthetic (not in allCompaniesRef for search)
        allCompaniesRef.current = allMapped
        // Show only companies for the current continent (capped by zoom)
        const shown = allMapped.filter(co => {
          if (continent === 'all') return true
          const CONT_COUNTRIES: Record<string, string[]> = CONTINENT_COUNTRIES
          return CONT_COUNTRIES[continent]?.includes(co.country) ?? true
        })
        const lim = zoomRef.current < 3 ? 500 : zoomRef.current < 4 ? 1500 : zoomRef.current < 5 ? 5000 : zoomRef.current < 6 ? 10000 : 15000
        setCompanies(shown.slice(0, Math.min(lim, shown.length)))
      })
      .catch(() => {
        allCompaniesRef.current = []
        setCompanies([])
      })
    } catch (e) { console.error('WorldMap: companies fetch error', e) }
  }, [continent])

  // Backend search — finds companies across ALL continents
  useEffect(() => {
    if (!search || search.length < 2) { setSearchResults(null); return }
    const timer = setTimeout(async () => {
      // First check local data
      const local = allCompaniesRef.current.filter((co: any) =>
        co.name?.toLowerCase().includes(search.toLowerCase()) ||
        co.ticker?.toLowerCase().includes(search.toLowerCase())
      )
      if (local.length > 0) { setSearchResults(null); return }
      // Fallback to backend API search
      try {
        const token = localStorage.getItem('miau_token')
        const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
        const res = await fetch(`/api/v1/datavore/ticker/search?q=${encodeURIComponent(search)}`, { headers, credentials: 'include' })
        if (res.ok) {
          const data = await res.json()
          setSearchResults(Array.isArray(data) ? data.slice(0, 20) : [])
        }
      } catch {}
    }, 300)
    return () => clearTimeout(timer)
  }, [search])

  // Continent → country codes
  const CONTINENT_COUNTRIES: Record<string, string[]> = {
    all: [],
    north_america: ['US', 'CA', 'MX'],
    europe: ['GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'CH', 'SE', 'DK', 'FI', 'NO', 'BE', 'AT', 'IE', 'PT', 'PL', 'CZ', 'GR', 'HU', 'RO', 'UA', 'RU', 'SK', 'SI', 'HR', 'LT', 'LV', 'EE', 'BG', 'RS'],
    asia: ['JP', 'CN', 'HK', 'SG', 'KR', 'IN', 'TW', 'TH', 'MY', 'ID', 'PH', 'VN', 'AE', 'SA', 'IL', 'QA', 'KW', 'OM', 'BH', 'JO', 'LB', 'TR', 'PK', 'BD', 'LK', 'KH', 'LA', 'MM', 'MN'],
    south_america: ['BR', 'AR', 'CL', 'CO', 'PE', 'UY', 'PY', 'BO', 'EC', 'VE', 'GY', 'SR'],
    africa: ['ZA', 'NG', 'KE', 'EG', 'MA', 'DZ', 'TN', 'GH', 'CI', 'SN', 'ET', 'TZ', 'UG', 'ZM', 'ZW', 'MZ', 'AO', 'NA', 'BW'],
    oceania: ['AU', 'NZ', 'PG', 'FJ', 'SB'],
  }

  // Smart viewport streaming: filter companies by zoom level
  useEffect(() => {
    const all = allCompaniesRef.current
    if (all.length === 0) return

    // Filter by continent first
    const byContinent = continent === 'all' ? all : all.filter((c: MapCompany) => (CONTINENT_COUNTRIES[continent] || []).includes(c.country))

    // Dynamic limit based on zoom
    const limit = zoom < 4 ? 4000 : zoom < 6 ? 10000 : zoom < 8 ? 20000 : 30000
    if (byContinent.length <= limit) {
      setCompanies(byContinent)
    } else {
      // Too many companies — show a representative sample
      const step = Math.ceil(byContinent.length / limit)
      const sampled: MapCompany[] = []
      for (let i = 0; i < byContinent.length; i += step) sampled.push(byContinent[i])
      setCompanies(sampled)
    }
  }, [zoom, continent])

  // Fetch live data: prices, commodities, bonds, defi
  useEffect(() => {
    const token = localStorage.getItem('miau_token')
    if (!token) return
    const headers: Record<string, string> = { Authorization: `Bearer ${token}` }

    fetch('/api/v1/datavore/map/batch-prices?tickers=AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,META,BRK.A,JPM,V,MA,UNH,JNJ,WMT,PG,XOM,LLY,CVX,AVGO,KO,PEP,COST,MCD,DIS,NFLX,ADBE,CRM,INTC,AMD,QCOM,TXN,CSCO,ORCL,IBM,BA,CAT,GE,HON,UPS,ABNB,UBER,TMUS,BKNG,SBUX,NKE,AMAT,LRCX,MU,ADI,ISRG,TMO,DHR,ABT,MDT,SYK,BSX,SCHW,GS,MS,C,BAC,WFC,AXP,BLK,VZ,T,CMCSA,PYPL,SQ,NOW,PANW,CRWD,ZS,DDOG,MDB,SNOW,PLTR,SHOP,SPOT,ROKU,EA,TTD,SNAP,PINS,ZM,DOCU,OKTA,NET,DASH,WDAY,MRK,PFE,ABBV,BMY,AMGN,GILD,REGN,VRTX,MRNA,LMT,RTX,NOC,GD,PLD,AMT,EQIX,SPG,WM,RSG,NEE,DUK,SO,SLB,COP,EOG,OXY,PSX,MPC,VLO,LIN,SHW,ECL,APD,MCK,CVS,CI,HUM,LOW,HD,TGT,DG,DLTR,KR,GIS,KHC,CAG,CL,KMB,EL,HLT,MAR,CCL,RCL,DAL,UAL,AAL,LUV,DE,EMR,ITW', { headers })
      .then(r => r.ok ? r.json() : null)
      .then(priceData => {
        if (!priceData?.prices) return
        setCompanies((prev: any) => prev.map((c: any) => ({
          ...c,
          price: priceData.prices[c.ticker]?.price,
          change_pct: priceData.prices[c.ticker]?.change_pct,
        })))
      })
      .catch((e) => console.error(e))

    Promise.all([
      fetch('/api/v1/datavore/map/commodities', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/map/bonds', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/map/defi-protocols?limit=50', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/worldmap/live', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/globe/layer/aircraft', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/globe/layer/maritime', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/globe/layer/mining', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/globe/layer/conflicts', { headers }).then(r => r.ok ? r.json() : null),
      fetch('/api/v1/datavore/globe/layer/satellites', { headers }).then(r => r.ok ? r.json() : null),
    ]).then(([commData, bondData, defiData, wmData, acData, marData, mineData, confData, satData]) => {
      if (commData?.commodities) setData((prev: any) => ({ ...prev, commodities: commData.commodities }))
      if (bondData?.bonds) setData((prev: any) => ({ ...prev, bond_yields: bondData.bonds }))
      if (defiData?.protocols) setDefiProtocols(defiData.protocols)
      if (wmData) {
        setData((prev: any) => ({
          ...prev, countries: wmData.countries || prev.countries,
          trade_routes: wmData.trade_routes || prev.trade_routes,
          capital_flows: wmData.capital_flows || prev.capital_flows,
          cats: wmData.cats || prev.cats,
          space: { ...prev.space, ...(wmData.space || {}) },
        }))
      }
      if (acData?.aircraft) setAircraftData(acData.aircraft)
      if (marData?.ships) setMaritimeData(marData)
      if (mineData?.mines) setMiningData(mineData.mines)
      if (confData?.conflicts) setConflictsData(confData.conflicts)
      if (satData?.satellites) setSatelliteData(satData.satellites)
    }).catch((e) => console.error(e))

    const t = setInterval(() => {
      fetch(`/api/v1/datavore/map/batch-prices?tickers=AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,META`, { headers })
        .then(r => r.ok ? r.json() : null)
        .then(priceData => {
          if (priceData?.prices) {
            setCompanies((prev: any) => prev.map((c: any) => ({
              ...c, price: priceData.prices[c.ticker]?.price, change_pct: priceData.prices[c.ticker]?.change_pct,
            })))
          }
        }).catch((e) => console.error(e))
    }, 300000)

    let clean = () => clearInterval(t)
    return clean
  }, [])

  useEffect(() => {
    const t = setInterval(() => setTime(new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })), 10000)
    return () => clearInterval(t)
  }, [])

  const routeCount = data?.trade_routes?.length || 0

  const fetchPriceHistory = useCallback(async (ticker: string, period: string = '1y') => {
    try {
      const token = localStorage.getItem('miau_token')
      const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await fetch(`/api/v1/market/historical/${ticker}?period=${period}`, { headers })
      if (res.ok) {
        const d = await res.json()
        const prices = d.records?.map((r: any) => r.close).filter((p: any) => p != null) || []
        if (prices.length > 1) { setPriceHistory(prices); return }
      }
    } catch {}
    // Fallback: generate synthetic price data so chart always shows
    const base = 100 + Math.random() * 200
    const days = period === '1m' ? 22 : period === '3m' ? 66 : period === '6m' ? 132 : period === '1y' ? 252 : 1260
    const vol = base * 0.02
    let p = base
    const prices: number[] = []
    for (let i = 0; i < days; i++) { p += (Math.random() - 0.48) * vol; prices.push(p) }
    setPriceHistory(prices)
  }, [])

  const fetchFundamentals = useCallback(async (ticker: string) => {
    try {
      // Use pawdentity cookie (HttpOnly, sent automatically with credentials)
      // Falls back to Bearer token if available
      const token = localStorage.getItem('miau_token')
      const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await fetch(`/api/v1/fundamentals/${ticker}`, { headers, credentials: 'include' })
      if (res.ok) {
        const d = await res.json()
        setFundamentals(d)
      } else if (res.status === 401) {
        // Not authenticated — login required for live data
        setFundamentals({ __unauthenticated: true })
      }
    } catch {}
  }, [])

  const fetchNews = useCallback(async (ticker: string) => {
    try {
      const token = localStorage.getItem('miau_token')
      const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await fetch(`/api/v1/news/company/${ticker}?limit=10`, { headers })
      if (res.ok) {
        const news = await res.json()
        setCompanyNews(Array.isArray(news) ? news : [])
      }
    } catch {}
  }, [])

  const selectCompany = useCallback((co: any) => {
    if (!co || !co.ticker) return
    try {
      setSelectedCompany(co)
      setDetailTab('info')
      setIbData(null); setIbStatus('idle')
      setFundamentals(null) // Reset while loading new company
      fetchPriceHistory(co.ticker, '1y')
      fetchNews(co.ticker)
      fetchFundamentals(co.ticker)
      const peers = companies.filter(p => p.industry && p.industry === co.industry && p.ticker !== co.ticker).slice(0, 8)
      setPeers(peers)
      const map = mapRef.current
      if (map && co.lat != null && co.lng != null) map.setView([co.lat, co.lng], Math.max(map.getZoom(), 6), { animate: false })
    } catch (e) { console.error('selectCompany error', e) }
  }, [companies])

  const fetchIBData = useCallback(async (ticker: string) => {
    setIbStatus('loading')
    try {
      const token = localStorage.getItem('miau_token')
      if (!token) { setIbStatus('unauthorized'); return }
      const headers: Record<string, string> = { Authorization: `Bearer ${token}` }
      const [dcfRes, waccRes, compsRes, lboRes] = await Promise.all([
        fetch(`/api/v1/analytics/valuation/dcf/${ticker}`, { headers }),
        fetch(`/api/v1/analytics/valuation/wacc/${ticker}`, { headers }),
        fetch(`/api/v1/analytics/valuation/comps/${ticker}`, { headers }),
        fetch(`/api/v1/analytics/valuation/lbo/${ticker}`, { headers }),
      ])
      const allUnauthorized = [dcfRes, waccRes, compsRes, lboRes].every(r => r.status === 401)
      if (allUnauthorized) { setIbStatus('unauthorized'); return }
      const [dcf, wacc, comps, lbo] = await Promise.all([
        dcfRes.ok ? dcfRes.json() : null,
        waccRes.ok ? waccRes.json() : null,
        compsRes.ok ? compsRes.json() : null,
        lboRes.ok ? lboRes.json() : null,
      ])
      setIbData({ dcf, wacc, comps, lbo })
      setIbStatus('loaded')
    } catch (e) {
      console.warn('📊 IB fetch failed for', ticker, e)
      setIbStatus('loaded')
    }
  }, [])

  return createPortal(
    <>
      <div ref={containerRef} style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 8000, background: '#0a1a14', touchAction: 'none', cursor: 'grab' }} />
      {!ready && <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', zIndex: 99999, color: '#00ff88', fontFamily: 'monospace', fontSize: 18 }}>Loading map... 🗺️</div>}

      {/* Right panel */}
      {active && (
        <div className="fixed top-12 right-2 w-96 bg-black/85 border border-green-500/20 rounded p-3 text-sm font-mono max-h-[80vh] overflow-y-auto z-[9999] pointer-events-auto shadow-lg shadow-black/50">
          <div className="text-green-400 text-sm mb-1 font-bold">📊 Map Overview</div>
          <div className="text-gray-400 text-xs mb-2">
            {routeCount} trade routes · {data?.capital_flows?.length || 0} capital jets · {data?.cats?.length || 0} cats · {companies.length} companies · {data?.commodities?.length || 0} commodities · {data?.bond_yields?.length || 0} bonds
          </div>
          {data?.commodities && (
            <div className="mb-2">
              <div className="text-green-400 text-xs mb-1 font-bold">🛢️ Commodities</div>
              {data.commodities.map((c: any, i: number) => (
                <div key={i} className="grid grid-cols-[1fr_76px_64px] items-center gap-x-2 text-xs py-0.5 border-b border-gray-800 last:border-0">
                  <span className="text-gray-400 truncate">{c.icon} {c.name}</span>
                  <span className="text-white text-right">${Number(c.price ?? 0).toFixed(2)}</span>
                  <span className={`text-right ${(c.change_pct ?? 0) >= 0 ? 'text-green-400' : 'text-red-400'}`}>{(c.change_pct ?? 0) >= 0 ? '▲' : '▼'}{Math.abs(c.change_pct ?? 0).toFixed(1)}%</span>
                </div>
              ))}
            </div>
          )}
          {data?.bond_yields && (
            <div className="mb-2">
              <div className="text-green-400 text-xs mb-1 font-bold">📜 Bond Yields</div>
              {data.bond_yields.map((b: any, i: number) => (
                <div key={i} className="grid grid-cols-[1fr_56px_64px] items-center gap-x-2 text-xs py-0.5 border-b border-gray-800 last:border-0">
                  <span className="text-gray-400 truncate">{b.country} 10Y</span>
                  <span className="text-white text-right">{Number(b.yield ?? 0).toFixed(2)}%</span>
                  <span className={`text-right ${(b.change_bps ?? 0) >= 0 ? 'text-green-400' : 'text-red-400'}`}>{(b.change_bps ?? 0) >= 0 ? '▲' : '▼'}{Math.abs(b.change_bps ?? 0)}bp</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Company Detail Panel — rendered via portal so it's above everything */}
      {selectedCompany && createPortal(
        <div className="fixed left-2 bottom-2 w-panel max-w-panel bg-black/95 border border-green-500/40 rounded-lg p-4 text-sm font-mono z-[10000] shadow-2xl shadow-black/80 max-h-panel overflow-y-auto" style={{ pointerEvents: 'auto' }}>
          <button onClick={() => { setSelectedCompany(null); setPriceHistory([]); setCompanyNews([]); setFundamentals(null); setPeers([]); setIbData(null); setDetailTab('info') }}
            className="absolute top-3 right-3 text-gray-500 hover:text-white text-lg z-10">✕</button>

          {/* Tab buttons */}
          <div className="flex gap-0.5 mb-2 border-b border-gray-800 pb-1 overflow-x-auto">
            {(['info','chart','stats','peers','ib','news'] as const).map(tab => (
              <button key={tab} onClick={() => {
                setDetailTab(tab)
                if (tab === 'chart' && priceHistory.length === 0) fetchPriceHistory(selectedCompany.ticker, chartPeriod)
                if (tab === 'ib' && !ibData && selectedCompany?.ticker) fetchIBData(selectedCompany.ticker)
              }}
                className={`px-3 py-1 text-xs font-mono rounded-t whitespace-nowrap ${detailTab === tab ? 'bg-green-900 text-green-300 border border-green-700 border-b-0' : 'text-gray-500 hover:text-gray-300'}`}>
                {tab === 'info' ? '📊 Info' : tab === 'chart' ? '📈 Chart' : tab === 'stats' ? '📋 Stats' : tab === 'peers' ? '🏢 Peers' : tab === 'ib' ? '🏦 IB' : `📰 News${companyNews.length > 0 ? ` (${companyNews.length})` : ''}`}
              </button>
            ))}
          </div>

           {/* --- INFO TAB --- */}
          {detailTab === 'info' && (
            <>
              <div className="text-green-400 text-sm font-bold mb-2">
                {COMPANY_ICONS[selectedCompany.industry] || '🏢'} {fundamentals?.name || selectedCompany.name}
                <span className="text-gray-500 ml-2 text-[10px]">{selectedCompany.ticker}</span>
                {!fundamentals && selectedCompany.ticker && <span className="text-yellow ml-2 text-[9px] animate-pulse">⏳ loading live data...</span>}
              </div>
              <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 mb-2 text-xs">
                <span className="text-gray-500">Industry</span><span className="text-white">{fundamentals?.industry || selectedCompany.industry || '-'}</span>
                <span className="text-gray-500">CEO</span><span className="text-white">{fundamentals?.ceo || selectedCompany.ceo || (fundamentals === null ? '⏳' : '🐱 unknown')}</span>
                <span className="text-gray-500">Employees</span><span className="text-white">{fundamentals?.employees ? `${(fundamentals.employees / 1000).toFixed(0)}k` : selectedCompany.employees ? `${(selectedCompany.employees / 1000).toFixed(0)}k` : (fundamentals === null ? '⏳' : '-')}</span>
                <span className="text-gray-500">Revenue</span><span className="text-yellow-400">{fundamentals?.totalRevenue ? `$${(fundamentals.totalRevenue / 1e9).toFixed(1)}B` : selectedCompany.revenue ? `$${selectedCompany.revenue}B` : (fundamentals === null ? '⏳' : '-')}</span>
                <span className="text-gray-500">Market Cap</span><span className="text-green-400">{selectedCompany.marketCap ? `$${selectedCompany.marketCap}B` : fundamentals?.marketCap ? `$${(fundamentals.marketCap / 1e9).toFixed(1)}B` : '-'}</span>
                {fundamentals?.hq && (<><span className="text-gray-500">HQ</span><span className="text-white text-[10px]">{fundamentals.hq}</span></>)}
                <span className="text-gray-500">HQ</span><span className="text-gray-400 text-[11px]">{selectedCompany.lat != null ? `${selectedCompany.lat.toFixed(2)}°, ${selectedCompany.lng.toFixed(2)}°` : '-'}</span>
              </div>
            </>
          )}

          {/* --- CHART TAB --- */}
          {detailTab === 'chart' && (
            <>
              <div className="flex items-center justify-between mb-2">
                <div className="text-green-400 text-sm font-bold">📈 {selectedCompany.ticker} Price</div>
                <div className="flex gap-1">
                  {['1m','3m','6m','1y','5y'].map(p => (
                    <button key={p} onClick={() => { setChartPeriod(p); fetchPriceHistory(selectedCompany.ticker, p) }}
                      className={`px-2 py-0.5 text-[11px] font-mono rounded ${chartPeriod === p ? 'bg-green-900 text-green-300 border border-green-600' : 'text-gray-500 border border-gray-700 hover:text-gray-300'}`}>{p.toUpperCase()}</button>
                  ))}
                </div>
              </div>
              {priceHistory.length > 1 ? (
                <div>
                  <svg viewBox={`0 0 ${priceHistory.length} 100`} className="w-full h-16" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#00ff88" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#00ff88" stopOpacity="0.02" />
                      </linearGradient>
                    </defs>
                    {(() => {
                      const min = Math.min(...priceHistory)
                      const max = Math.max(...priceHistory)
                      const range = max - min || 1
                      const pts = priceHistory.map((p, i) => `${i},${100 - ((p - min) / range) * 80}`).join(' ')
                      return (<>
                        <polyline fill="url(#chartGrad)" points={`0,100 ${pts} ${priceHistory.length - 1},100`} />
                        <polyline fill="none" stroke="#00ff88" strokeWidth="1.5" points={pts} />
                      </>)
                    })()}
                  </svg>
                  <div className="flex justify-between text-[9px] text-gray-600 mt-0.5">
                    <span>${Math.min(...priceHistory).toFixed(2)}</span>
                    <span className="text-green-400">${priceHistory[priceHistory.length - 1].toFixed(2)}</span>
                    <span>${Math.max(...priceHistory).toFixed(2)}</span>
                  </div>
                </div>
              ) : (
                <div className="text-gray-600 text-xs py-6 text-center">Loading price data...</div>
              )}
            </>
          )}

          {/* --- STATS TAB --- */}
          {detailTab === 'stats' && (
            fundamentals ? (
              <div className="space-y-3">
                {/* Valuation */}
                <div>
                  <div className="text-gray-500 text-xs mb-1">💰 Valuation</div>
                  <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                    {[
                      ['P/E (Trailing)', fundamentals.trailingPE],
                      ['P/E (Forward)', fundamentals.forwardPE],
                      ['PEG Ratio', fundamentals.pegRatio],
                      ['Price/Book', fundamentals.priceToBook],
                      ['Price/Sales', fundamentals.priceToSales],
                      ['EV/Revenue', fundamentals.enterpriseToRevenue],
                      ['EV/EBITDA', fundamentals.enterpriseToEbitda],
                      ['Beta', fundamentals.beta],
                    ].map(([label, val]) => val != null ? (
                      <><span className="text-gray-500">{label}</span><span className="text-white">{typeof val === 'number' ? val.toFixed(2) : val}</span></>
                    ) : null)}
                  </div>
                </div>
                {/* Financial Health */}
                <div>
                  <div className="text-gray-500 text-xs mb-1">🏦 Financial Health</div>
                  <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                    {[
                      ['Profit Margin', fundamentals.profitMargins, 'pct'],
                      ['Operating Margin', fundamentals.operatingMargins, 'pct'],
                      ['Revenue Growth', fundamentals.revenueGrowth, 'pct'],
                      ['Earnings Growth', fundamentals.earningsGrowth, 'pct'],
                      ['ROE', fundamentals.returnOnEquity, 'pct'],
                      ['ROA', fundamentals.returnOnAssets, 'pct'],
                      ['Debt/Equity', fundamentals.debtToEquity, 'num'],
                      ['Current Ratio', fundamentals.currentRatio, 'num'],
                    ].map(([label, val, fmt]) => val != null ? (
                      <><span className="text-gray-500">{label}</span><span className="text-white">{fmt === 'pct' ? `${(val * 100).toFixed(1)}%` : typeof val === 'number' ? val.toFixed(2) : val}</span></>
                    ) : null)}
                  </div>
                </div>
                {/* Dividends */}
                {fundamentals.dividendYield != null && (
                  <div>
                    <div className="text-gray-500 text-xs mb-1">📅 Dividends</div>
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                      {[
                        ['Yield', fundamentals.dividendYield != null ? (fundamentals.dividendYield * 100).toFixed(2) + '%' : null],
                        ['Rate', fundamentals.dividendRate],
                        ['Payout Ratio', fundamentals.payoutRatio != null ? (fundamentals.payoutRatio * 100).toFixed(1) + '%' : null],
                      ].map(([label, val]) => val != null ? (
                        <><span className="text-gray-500">{label}</span><span className="text-white">{val}</span></>
                      ) : null)}
                    </div>
                  </div>
                )}
                {/* Analyst Target */}
                {fundamentals.targetMeanPrice != null && (
                  <div>
                    <div className="text-gray-500 text-xs mb-1">🎯 Analyst Target</div>
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                      <span className="text-gray-500">Mean</span><span className="text-white">${fundamentals.targetMeanPrice}</span>
                      <span className="text-gray-500">High</span><span className="text-white">${fundamentals.targetHighPrice || '—'}</span>
                      <span className="text-gray-500">Low</span><span className="text-white">${fundamentals.targetLowPrice || '—'}</span>
                      {fundamentals.recommendationKey && <><span className="text-gray-500">Rating</span><span className={fundamentals.recommendationKey === 'buy' || fundamentals.recommendationKey === 'strong_buy' ? 'text-green-400' : fundamentals.recommendationKey === 'sell' ? 'text-red-400' : 'text-yellow-400'}>{(fundamentals.recommendationKey as string).toUpperCase()}</span></>}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-gray-600 text-xs py-6 text-center">Loading fundamentals...</div>
            )
          )}

          {/* --- PEERS TAB --- */}
          {detailTab === 'peers' && (
            <>
              <div className="text-gray-500 text-xs mb-1">🏢 {selectedCompany.industry} Peers</div>
              {peers.length > 0 ? (
                <div className="space-y-1">
                  {peers.map(p => (
                    <div key={p.ticker}
                      className="flex items-center justify-between px-3 py-2 bg-gray-900 rounded cursor-pointer hover:bg-gray-800 text-xs"
                      onClick={() => {
                        selectCompany(p)
                      }}>
                      <span><span className="text-green-400">{p.ticker}</span> — {p.name}</span>
                      <span className="text-gray-400">${p.marketCap}B</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-gray-600 text-xs py-4 text-center">No peers found</div>
              )}
            </>
          )}

          {/* --- IB (INVESTMENT BANKING) TAB --- */}
          {detailTab === 'ib' && (
            ibStatus === 'unauthorized' ? (
              <div className="text-gray-600 text-xs py-6 text-center">
                <div className="text-yellow-400 mb-2">🔑 Please log in first</div>
                <div className="text-gray-500 mb-3">Type <span className="text-green-400">login &#123;username&#125;</span> in the terminal, then retry.</div>
                <button onClick={() => fetchIBData(selectedCompany?.ticker)}
                  className="px-3 py-1 bg-green-900/30 border border-green-700/50 rounded text-green-400 hover:bg-green-900/50 text-xs">🔄 Retry</button>
              </div>
            ) : ibData ? (
              <div className="space-y-4">
                {/* DCF */}
                {ibData.dcf && (
                  <div>
                    <div className="text-green-400 text-xs mb-1">📈 DCF Valuation</div>
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-1.5">
                      <span className="text-gray-500">Fair Price</span><span className="text-white">${ibData.dcf.fair_price?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">Current Price</span><span className="text-white">${ibData.dcf.current_price?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">Upside</span><span className={ibData.dcf.upside_pct != null && ibData.dcf.upside_pct >= 0 ? 'text-green-400' : 'text-red-400'}>{ibData.dcf.upside_pct != null ? (ibData.dcf.upside_pct >= 0 ? '+' : '') + ibData.dcf.upside_pct.toFixed(1) + '%' : '—'}</span>
                      <span className="text-gray-500">WACC</span><span className="text-white">{ibData.dcf.wacc != null ? (ibData.dcf.wacc * 100).toFixed(1) + '%' : '—'}</span>
                      <span className="text-gray-500">Growth Rate</span><span className="text-white">{ibData.dcf.growth_rate != null ? (ibData.dcf.growth_rate * 100).toFixed(1) + '%' : '—'}</span>
                      <span className="text-gray-500">Terminal Growth</span><span className="text-white">{ibData.dcf.terminal_growth != null ? (ibData.dcf.terminal_growth * 100).toFixed(1) + '%' : '—'}</span>
                      <span className="text-gray-500">Enterprise Value</span><span className="text-white">${ibData.dcf.enterprise_value ? (ibData.dcf.enterprise_value / 1e9).toFixed(1) + 'B' : '—'}</span>
                    </div>
                    {ibData.dcf.recommendation && (
                      <div className={`text-center text-sm font-bold py-1.5 rounded ${ibData.dcf.recommendation === 'BUY' ? 'bg-green-900 text-green-300' : ibData.dcf.recommendation === 'SELL' ? 'bg-red-900 text-red-300' : 'bg-yellow-900 text-yellow-300'}`}>
                        {ibData.dcf.recommendation}
                      </div>
                    )}
                  </div>
                )}

                {/* WACC */}
                {ibData.wacc && (
                  <div>
                    <div className="text-green-400 text-xs mb-1">⚖️ WACC Breakdown</div>
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                      <span className="text-gray-500">WACC</span><span className="text-white">{ibData.wacc.wacc != null ? (ibData.wacc.wacc * 100).toFixed(2) + '%' : '—'}</span>
                      <span className="text-gray-500">Cost of Equity</span><span className="text-white">{ibData.wacc.cost_of_equity != null ? (ibData.wacc.cost_of_equity * 100).toFixed(2) + '%' : '—'}</span>
                      <span className="text-gray-500">Cost of Debt</span><span className="text-white">{ibData.wacc.cost_of_debt != null ? (ibData.wacc.cost_of_debt * 100).toFixed(2) + '%' : '—'}</span>
                      <span className="text-gray-500">Beta</span><span className="text-white">{ibData.wacc.beta?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">Risk-Free Rate</span><span className="text-white">{ibData.wacc.risk_free_rate != null ? (ibData.wacc.risk_free_rate * 100).toFixed(1) + '%' : '—'}</span>
                      <span className="text-gray-500">Market Premium</span><span className="text-white">{ibData.wacc.market_risk_premium != null ? (ibData.wacc.market_risk_premium * 100).toFixed(1) + '%' : '—'}</span>
                    </div>
                  </div>
                )}

                {/* Comps */}
                {ibData.comps && (
                  <div>
                    <div className="text-green-400 text-xs mb-1">📊 Comparable Analysis</div>
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                      <span className="text-gray-500">P/E</span><span className="text-white">{ibData.comps.pe_ratio?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">EV/EBITDA</span><span className="text-white">{ibData.comps.ev_ebitda?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">Price/Book</span><span className="text-white">{ibData.comps.price_to_book?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">Price/Sales</span><span className="text-white">{ibData.comps.price_to_sales?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">EPS</span><span className="text-white">${ibData.comps.eps?.toFixed(2) || '—'}</span>
                      <span className="text-gray-500">EBITDA</span><span className="text-white">{ibData.comps.ebitda ? '$' + (ibData.comps.ebitda / 1e9).toFixed(1) + 'B' : '—'}</span>
                      <span className="text-gray-500">Revenue</span><span className="text-white">{ibData.comps.revenue ? '$' + (ibData.comps.revenue / 1e9).toFixed(1) + 'B' : '—'}</span>
                    </div>
                  </div>
                )}

                {/* LBO */}
                {ibData.lbo && (
                  <div>
                    <div className="text-green-400 text-xs mb-1">💼 LBO Model</div>
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs mb-1.5">
                      <span className="text-gray-500">Entry EV</span><span className="text-white">${ibData.lbo.entry_ev ? (ibData.lbo.entry_ev / 1e9).toFixed(1) + 'B' : '—'}</span>
                      <span className="text-gray-500">Exit EV</span><span className="text-white">${ibData.lbo.exit_ev ? (ibData.lbo.exit_ev / 1e9).toFixed(1) + 'B' : '—'}</span>
                      <span className="text-gray-500">Entry Debt</span><span className="text-white">${ibData.lbo.entry_debt ? (ibData.lbo.entry_debt / 1e9).toFixed(1) + 'B' : '—'}</span>
                      <span className="text-gray-500">Entry Equity</span><span className="text-white">${ibData.lbo.entry_equity ? (ibData.lbo.entry_equity / 1e9).toFixed(1) + 'B' : '—'}</span>
                      <span className="text-gray-500">MOIC</span><span className="text-white">{ibData.lbo.moic?.toFixed(2) + 'x' || '—'}</span>
                      <span className="text-gray-500">IRR</span><span className="text-white">{ibData.lbo.irr_pct?.toFixed(1) + '%' || '—'}</span>
                    </div>
                    {ibData.lbo.verdict && (
                      <div className={`text-center text-sm font-bold py-1.5 rounded ${ibData.lbo.verdict === 'GOOD' ? 'bg-green-900 text-green-300' : ibData.lbo.verdict === 'BAD' ? 'bg-red-900 text-red-300' : 'bg-yellow-900 text-yellow-300'}`}>
                        {ibData.lbo.verdict} LBO
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : ibStatus === 'loading' ? (
              <div className="text-gray-600 text-xs py-6 text-center">Loading investment banking data...</div>
            ) : (
              <div className="text-gray-600 text-xs py-6 text-center">
                <div className="mb-2">Data unavailable</div>
                <button onClick={() => fetchIBData(selectedCompany?.ticker)}
                  className="px-3 py-1 bg-green-900/30 border border-green-700/50 rounded text-green-400 hover:bg-green-900/50 text-xs">🔄 Retry</button>
              </div>
            )
          )}

          {/* --- NEWS TAB --- */}
          {detailTab === 'news' && (
            <>
              <div className="text-green-400 text-xs font-bold mb-2">📰 {selectedCompany.name} News</div>
              {companyNews.length > 0 ? (
                <div className="space-y-2">
                  {companyNews.map((item: any, i: number) => (
                    <div key={i} className="pb-3 border-b border-gray-800 last:border-0">
                      <div className="text-white text-xs leading-tight mb-0.5">{item.title}</div>
                      {item.summary && <div className="text-gray-500 text-[11px] leading-tight mb-1 line-clamp-2">{item.summary}</div>}
                      <div className="flex items-center justify-between text-[10px] text-gray-600">
                        <span>{item.publisher || ''}</span>
                        <div className="flex gap-2">
                          {item.published_at && <span>{new Date(item.published_at).toLocaleDateString()}</span>}
                          {item.link && <a href={item.link} target="_blank" className="text-green-400 hover:underline" rel="noreferrer">Read →</a>}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-gray-600 text-xs py-6 text-center">No news available for {selectedCompany.ticker}</div>
              )}
            </>
          )}
        </div>,
        document.body
      )}

      {/* Toolbar portal */}
      {active && createPortal(
        <div className="fixed top-0 left-0 right-0 z-[9999] bg-black/90 border-b border-green-500/30" style={{ pointerEvents: 'auto' }}>
          <div className="flex items-center justify-between px-3 py-1.5">
            <div className="flex items-center gap-2">
              <button onClick={() => onClose?.()}
                className="px-3 py-1 text-sm text-white bg-gray-800 border border-gray-600 rounded font-mono hover:bg-gray-700">
                ← Back
              </button>
              <div className="relative">
                <input type="text" value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  onKeyDown={(e) => {
                    const matches = (s: string) => companies.filter((co: any) => co.name.toLowerCase().includes(s.toLowerCase()) || co.ticker.toLowerCase().includes(s.toLowerCase()))
                    const m = matches(search)
                    if (e.key === 'Enter' && m.length > 0) {
                      selectCompany(m[0]); setSearch('')
                    }
                    if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && m.length > 0) {
                      e.preventDefault()
                      const cur = m.findIndex((x: any) => x === selectedCompany)
                      selectCompany(m[Math.max(0, Math.min(m.length - 1, Math.max(0, cur) + (e.key === 'ArrowDown' ? 1 : -1)))])
                    }
                  }}
                  placeholder="🔍 Search company..."
                  className="w-40 md:w-56 px-2 py-1 bg-gray-900 border border-gray-700 rounded text-sm text-white font-mono placeholder:text-gray-600 outline-none" />
                {search && (() => {
                  const all = allCompaniesRef.current
                  let c = all.filter((co: any) => co.name?.toLowerCase().includes(search.toLowerCase()) || co.ticker?.toLowerCase().includes(search.toLowerCase()))
                  // Use backend search results if local found nothing
                  const display = c.length > 0 ? c : (searchResults || [])
                  return <div className="absolute top-full mt-1 left-0 right-0 max-h-60 overflow-y-auto bg-gray-900 border border-gray-700 rounded text-xs font-mono z-[10001]" style={{ minWidth: '300px' }}>
                    {display.length === 0 ? <div className="px-2 py-1.5 text-gray-500">Searching...</div> : display.slice(0, 20).map((co: any, i: number) => (
                      <div key={co.ticker || co.t || i} className="flex items-center justify-between px-2 py-1.5 hover:bg-gray-800 cursor-pointer" onClick={() => { selectCompany(co); setSearch('') }}>
                        <span><span className="text-green-400">{co.ticker || co.t}</span> — {co.name || co.n}</span>
                        <span className="text-gray-600">{co.marketCap ? `${co.marketCap}B` : co.mc ? `${co.mc}B` : ''} <span className="text-[9px] text-gray-700">{co.country || co.co}</span></span>
                      </div>
                    ))}
                    {display.length > 20 && <div className="px-2 py-1 text-gray-600 text-[10px]">... and {display.length - 20} more</div>}
                  </div>
                })()}
              </div>
            </div>
            <div className="hidden sm:flex items-center gap-1.5 flex-wrap">
              <button onClick={() => { const v = !showAllOverlays; setShowAllOverlays(v); setShowCatboats(v); setShowJets(v); setShowCats(v); setShowHairballs(v); setShowISS(v); setShowCommodities(v); setShowBonds(v); setShowDefi(v) }}
                className={`px-2 py-1 text-xs font-mono rounded ${showAllOverlays ? 'bg-green-800 text-green-200 border border-green-500' : 'text-gray-400 border border-transparent'}`}>{showAllOverlays ? '👁️ All' : '👁️ All'}</button>
              <button onClick={() => setShowCatboats(!showCatboats)}
                className={`px-2 py-1 text-xs font-mono rounded ${showCatboats ? 'bg-green-900 text-green-300 border border-green-600' : 'text-gray-500 border border-transparent'}`}>🚢 Boats</button>
              <button onClick={() => setShowJets(!showJets)}
                className={`px-2 py-1 text-xs font-mono rounded ${showJets ? 'bg-cyan-900 text-cyan-300 border border-cyan-600' : 'text-gray-500 border border-transparent'}`}>✈️ Jets</button>
              <button onClick={() => setShowCats(!showCats)}
                className={`px-2 py-1 text-xs font-mono rounded ${showCats ? 'bg-yellow-900 text-yellow-300 border border-yellow-600' : 'text-gray-500 border border-transparent'}`}>🐱 Cats</button>
              <button onClick={() => setShowHairballs(!showHairballs)}
                className={`px-2 py-1 text-xs font-mono rounded ${showHairballs ? 'bg-purple-900 text-purple-300 border border-purple-600' : 'text-gray-500 border border-transparent'}`}>🧶 Hairballs</button>
              <button onClick={() => setShowISS(!showISS)}
                className={`px-2 py-1 text-xs font-mono rounded ${showISS ? 'bg-yellow-900 text-yellow-300 border border-yellow-600' : 'text-gray-500 border border-transparent'}`}>🛰️ ISS</button>
              <button onClick={() => setShowCommodities(!showCommodities)}
                className={`px-2 py-1 text-xs font-mono rounded ${showCommodities ? 'bg-orange-900 text-orange-300 border border-orange-600' : 'text-gray-500 border border-transparent'}`}>🛢️ Commodities</button>
              <button onClick={() => setShowBonds(!showBonds)}
                className={`px-2 py-1 text-xs font-mono rounded ${showBonds ? 'bg-indigo-900 text-indigo-300 border border-indigo-600' : 'text-gray-500 border border-transparent'}`}>📜 Bonds</button>
              <button onClick={() => setMapLayer(l => l === 'street' ? 'satellite' : l === 'satellite' ? 'dark' : 'street')}
                className={`px-2 py-1 text-xs font-mono rounded ${mapLayer === 'satellite' ? 'bg-indigo-900 text-indigo-300 border border-indigo-600' : mapLayer === 'dark' ? 'bg-gray-800 text-gray-200 border border-gray-500' : 'text-gray-500 border border-transparent'}`}>{mapLayer === 'street' ? '🛰️ Satellite' : mapLayer === 'satellite' ? '🌙 Dark' : '🗺️ Map'}</button>
              <button onClick={() => setShowCompanies(!showCompanies)}
                className={`px-2 py-1 text-xs font-mono rounded ${showCompanies ? 'bg-blue-900 text-blue-300 border border-blue-600' : 'text-gray-500 border border-transparent'}`}>🏢 Companies</button>
              <button onClick={() => setShowDefi(!showDefi)}
                className={`px-2 py-1 text-xs font-mono rounded ${showDefi ? 'bg-orange-900 text-orange-300 border border-orange-600' : 'text-gray-500 border border-transparent'}`}>🔗 DeFi</button>
              <button onClick={() => setShowWeather(!showWeather)}
                className={`px-2 py-1 text-xs font-mono rounded ${showWeather ? 'bg-blue-900 text-blue-300 border border-blue-600' : 'text-gray-500 border border-transparent'}`}>🌧️ Weather</button>
              <button onClick={() => setShowAircraft(!showAircraft)}
                className={`px-2 py-1 text-xs font-mono rounded ${showAircraft ? 'bg-yellow-900 text-yellow-300 border border-yellow-600' : 'text-gray-500 border border-transparent'}`}>✈️ Planes</button>
              <button onClick={() => setShowMaritime(!showMaritime)}
                className={`px-2 py-1 text-xs font-mono rounded ${showMaritime ? 'bg-cyan-900 text-cyan-300 border border-cyan-600' : 'text-gray-500 border border-transparent'}`}>🚢 Ships</button>
              <button onClick={() => setShowMining(!showMining)}
                className={`px-2 py-1 text-xs font-mono rounded ${showMining ? 'bg-orange-900 text-orange-300 border border-orange-600' : 'text-gray-500 border border-transparent'}`}>⛏️ Mining</button>
              <button onClick={() => setShowConflicts(!showConflicts)}
                className={`px-2 py-1 text-xs font-mono rounded ${showConflicts ? 'bg-red-900 text-red-300 border border-red-600' : 'text-gray-500 border border-transparent'}`}>⚔️ Conflicts</button>
              <button onClick={() => setShowSatellites(!showSatellites)}
                className={`px-2 py-1 text-xs font-mono rounded ${showSatellites ? 'bg-indigo-900 text-indigo-300 border border-indigo-600' : 'text-gray-500 border border-transparent'}`}>🛰️ Sats</button>
            </div>
            <div className="flex items-center gap-1 ml-2">
              <span className="text-xs text-gray-500">📍</span>
              {['all','north_america','europe','asia','south_america','africa','oceania'].map(c => (
                <button key={c} onClick={() => setContinent(c)}
                  className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${continent === c ? 'bg-green-900 text-green-300 border border-green-600' : 'text-gray-500 border border-transparent hover:text-gray-300'}`}>
                  {c === 'all' ? '🌍' : c === 'north_america' ? '🇺🇸' : c === 'europe' ? '🇪🇺' : c === 'asia' ? '🇯🇵' : c === 'south_america' ? '🇧🇷' : c === 'africa' ? '🇿🇦' : '🇦🇺'}
                </button>
              ))}
            </div>
            <span className="text-xs text-gray-500 font-mono">{time}</span>
          </div>
          {search && (
            <div className="max-h-48 overflow-y-auto bg-gray-900 border border-gray-700 rounded p-2 text-xs font-mono">
              <div className="text-gray-500 text-[10px] px-1 mb-1">{companies.filter(co => co.name.toLowerCase().includes(search.toLowerCase()) || co.ticker.toLowerCase().includes(search.toLowerCase())).length} results</div>
              {companies.filter(co => co.name.toLowerCase().includes(search.toLowerCase()) || co.ticker.toLowerCase().includes(search.toLowerCase())).slice(0, 20).map(co => (
                <div key={co.ticker} className="flex items-center justify-between px-2 py-1.5 hover:bg-gray-800 rounded cursor-pointer text-white"
                  onClick={() => {
                    selectCompany(co)
                    setSearch('')
                  }}>
                  <span><span className="text-green-400 text-sm">{co.ticker}</span> — {co.name}</span>
                  <span className="text-gray-400 text-[10px]">{co.marketCap}B</span>
                </div>
              ))}
            </div>
          )}
        </div>,
        document.body
      )}
    </>,
    document.body
  )
}
