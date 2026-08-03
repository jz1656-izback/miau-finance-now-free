// ConnectionDot — connection status indicator for Terminal
export function ConnectionDot({ connected }: { connected: boolean }) {
  const color = connected ? '#00ff88' : '#ff4444'
  return (
    <span
      className="inline-block rounded-full"
      style={{
        width: 6, height: 6, background: color,
        boxShadow: `0 0 4px ${color}`,
        transition: 'background 0.3s, box-shadow 0.3s',
      }}
    />
  )
}
