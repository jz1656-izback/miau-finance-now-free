import { useState, useEffect } from 'react'

interface Invoice {
  id: string
  amount: number
  currency: string
  status: string
  period_start: string
  period_end: string
  paid_at: string | null
  pdf_url: string | null
}

export default function InvoiceList() {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchInvoices = async () => {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
      try {
        const res = await fetch('/api/v1/billing/invoices', { headers })
        if (res.ok) {
          const data = await res.json()
          setInvoices(data.invoices || [])
        }
      } catch { /* ignore */ }
      setLoading(false)
    }
    fetchInvoices()
  }, [])

  if (loading) return <div className="p-4 text-dim">Loading invoices...</div>

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">💰 Billing History</h2>

      {invoices.length === 0 ? (
        <p className="text-dim text-sm">No invoices yet. Invoices appear after your first paid billing period.</p>
      ) : (
        <table className="w-full text-xs">
          <thead>
            <tr className="text-dim border-b border-gray-700">
              <th className="text-left py-1">Period</th>
              <th className="text-right py-1">Amount</th>
              <th className="text-center py-1">Status</th>
              <th className="text-right py-1">Paid</th>
              <th className="text-right py-1">Invoice</th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((inv, i) => (
              <tr key={i} className="border-b border-gray-800">
                <td className="py-1 text-dim">
                  {inv.period_start ? new Date(inv.period_start).toLocaleDateString() : ''}
                  {' — '}
                  {inv.period_end ? new Date(inv.period_end).toLocaleDateString() : ''}
                </td>
                <td className="text-right py-1 text-white">
                  ${(inv.amount / 100).toFixed(2)} {inv.currency?.toUpperCase()}
                </td>
                <td className="text-center py-1">
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    inv.status === 'paid' ? 'bg-green-900 text-green' :
                    inv.status === 'open' ? 'bg-yellow-900 text-yellow' :
                    'bg-red-900 text-red'
                  }`}>
                    {inv.status}
                  </span>
                </td>
                <td className="text-right py-1 text-dim">
                  {inv.paid_at ? new Date(inv.paid_at).toLocaleDateString() : '-'}
                </td>
                <td className="text-right py-1">
                  {inv.pdf_url ? (
                    <a href={inv.pdf_url} target="_blank" rel="noopener noreferrer"
                      className="text-cyan hover:text-white text-xs">PDF</a>
                  ) : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
