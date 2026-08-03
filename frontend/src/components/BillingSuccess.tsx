export default function BillingSuccess() {
  return (
    <div className="min-h-screen flex items-center justify-center crt scanline" style={{ background: '#0a0a0a' }}>
      <div className="text-center max-w-md p-8">
        <div className="text-6xl mb-4">🐱✅</div>
        <h1 className="text-2xl font-bold text-green mb-2">Payment Successful!</h1>
        <p className="text-dim mb-6">Your subscription is active. The cat purrs with approval.</p>
        <div className="p-4 bg-gray-800 rounded-xl mb-6 text-left text-sm space-y-2">
          <p className="text-green">✓ Unlimited requests to the terminal</p>
          <p className="text-green">✓ AI advisor commands unlocked</p>
          <p className="text-green">✓ Priority support (the cat responds faster)</p>
          <p className="text-green">✓ All data providers at your paw-tips</p>
          <p className="text-dim mt-2">🐱 "Thank you for your tuna. The cat is pleased."</p>
        </div>
        <a
          href="/"
          className="inline-block px-6 py-3 bg-green-800 text-green rounded-lg hover:bg-green-700 transition-colors font-mono text-sm"
        >
          → Return to Terminal
        </a>
      </div>
    </div>
  )
}
