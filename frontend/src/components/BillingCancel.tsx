export default function BillingCancel() {
  return (
    <div className="min-h-screen flex items-center justify-center crt scanline" style={{ background: '#0a0a0a' }}>
      <div className="text-center max-w-md p-8">
        <div className="text-6xl mb-4">🐱💤</div>
        <h1 className="text-2xl font-bold text-yellow mb-2">Checkout Cancelled</h1>
        <p className="text-dim mb-6">No problem. The cat is patient. Your trial is always available.</p>
        <div className="p-4 bg-gray-800 rounded-xl mb-6 text-left text-sm">
          <p className="text-dim">You can always come back and subscribe later:</p>
          <ul className="mt-2 space-y-1">
            <li className="text-green">• Type <code className="bg-gray-700 px-1 rounded">pricing</code> in the terminal</li>
            <li className="text-green">• Or click <code className="bg-gray-700 px-1 rounded">Subscribe</code> on the Pro plan</li>
          </ul>
          <p className="text-dim mt-3">🐱 "The cat doesn't judge. But the cat remembers."</p>
        </div>
        <a
          href="/"
          className="inline-block px-6 py-3 bg-gray-800 text-dim rounded-lg hover:bg-gray-700 transition-colors font-mono text-sm"
        >
          ← Return to Terminal
        </a>
      </div>
    </div>
  )
}
