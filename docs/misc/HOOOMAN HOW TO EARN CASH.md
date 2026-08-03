# 🐱💰 HOOOMAN HOW TO EARN CASH — MIAU FINANCE GO-LIVE CHECKLIST

```
   ╱|、
  (˚ˎ 。7     "The code is written. The cats are ready. The tuna is waiting."
   |、˜〵      "You have €20. You need infinite tuna. Here is the plan."
   じしˍ,)ノ    "Follow it exactly. Do not skip steps. The cat is watching."
```

**Last updated:** 2026-05-21
**Budget:** €20
**Goal:** Recurring revenue before the cat gets impatient

---

## ✅ ALREADY DONE (You Can Skip These)

The following is already built and working:

| Item | Status |
|------|--------|
| Registration API (`POST /api/v1/auth/register`) | ✅ Working |
| Login API (`POST /api/v1/auth/token`) | ✅ Working |
| Stripe checkout endpoint (`POST /api/v1/billing/checkout`) | ✅ Dev mode OK |
| Pricing page in terminal (`pricing` command) | ✅ €99 Pro / €396 Enterprise |
| Revenue tracking (`revenue` command) | ✅ 20/80 split |
| Bloomberg vs Miau comparison | ✅ on ecosystem site |
| All 8 services (5173-5181, 8000) | ✅ All running |
| Frontend + Backend tests | ✅ 120+ passing |
| Cat sounds via WebAudio | ✅ meow, purr, chirp, hiss |
| `cats`, `miau`, `joke`, `purr` commands | ✅ Implemented |
| Go-live health check script | `scripts/go-live.sh` |

---

## 💳 STEP 1: Get Your Stripe Account (FREE — 10 min)

Stripe is how customers pay you. No monthly fee. They take 2.9% + €0.25 per transaction.

### What to do:

1. Go to https://dashboard.stripe.com/register
2. Sign up with your email (use the project email, not personal)
3. Verify your email
4. Click "Activate your account" → fill in your details
   - You don't need a real company yet — sole proprietor works
   - You don't need a website URL yet — put `miau.finance` as placeholder
   - Bank account: you can add this later (payouts won't work without it)
5. Once activated, go to **Developers → API Keys**
6. Copy the **Publishable key** (starts with `pk_live_` or `pk_test_`)
7. Copy the **Secret key** (starts with `sk_live_` or `sk_test_`)

### Create Products in Stripe

1. In Stripe Dashboard → **Products** → **Add Product**
2. **Product 1: Miau Finance Pro**
   - Name: `Miau Finance Pro`
   - Description: `300 req/min, AI advisor, 3D charts, all providers, priority support`
   - Pricing: **Recurring → Monthly → €99**
   - Save → copy the `price_xxx` ID
3. **Product 2: Miau Finance Enterprise**
   - Name: `Miau Finance Enterprise`
   - Description: `10k req/min, all features, custom deployment, SLA, dedicated support`
   - Pricing: **Recurring → Monthly → €396**
   - Save → copy the `price_xxx` ID

### Wire Everything Into `.env`

Open `.env` and add/replace these lines:

```bash
# Stripe — REAL LIVE KEYS (get from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxx

# Stripe Price IDs (from Products page)
STRIPE_PRO_PRICE_ID=price_xxxxxxxxxxxxxxxxx    # €99/mo
STRIPE_ENTERPRISE_PRICE_ID=price_xxxxxxxxxxxxxxxxx  # €396/mo
```

### Restart Backend

```bash
docker compose restart backend
```

### Test the Payment Flow

```bash
# 1. Open terminal at localhost:5173
# 2. Login (if needed):
login admin miau2026

# 3. Open the pricing page:
pricing

# 4. Upgrade to Pro:
billing upgrade

# 5. This opens Stripe Checkout. Pay with test card:
#    Card number: 4242 4242 4242 4242
#    Any future expiry date
#    Any CVC

# 6. After payment, check your revenue:
revenue

# You should see:
#   📈  TOTAL REVENUE      €99.00
#   🧑  Your 20%:          €19.80
#   🐟  Project 80%:       €79.20
```

### Total cost: €0

---

## 🌐 STEP 2: Make It Publicly Accessible (€0)

Your terminal is on `localhost:5173`. Nobody can pay you if they can't reach it.

The easiest way: **ngrok** — creates a public URL that tunnels to your localhost. Free tier works fine.

### Install & auth ngrok:

```bash
# Install (if not already):
sudo apt install ngrok

# Or download manually:
# curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
# echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
# sudo apt update && sudo apt install ngrok

# Authenticate (REQUIRED — sign up at https://dashboard.ngrok.com/signup first):
ngrok authtoken YOUR_NGROK_AUTH_TOKEN

# Start tunnel to the terminal:
ngrok http 5173
```

After running `ngrok http 5173`, you'll see:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:5173
```

**Share that URL.** Anyone with the link can access your terminal, see the pricing, and upgrade to Pro.

### Alternative: Cheap VPS (€4/mo)

If you want a permanent URL:

```bash
# 1. Sign up at hetzner.com (CX22 = €4/month)
# 2. Deploy Ubuntu 24.04
# 3. Install Docker
# 4. Clone the repo
# 5. docker compose up -d
# 6. Point your domain to the VPS IP
```

**Total cost: €0 (ngrok) or €4/mo (VPS)**

---

## 📢 STEP 3: Get Your First Customer (€0 — 30 min)

Everything is built. Now you need ONE person to pay.

### Ready-made marketing posts

The repo already has complete marketing content in `marketing/`:

| File | Platform | What to do |
|------|----------|-----------|
| `marketing/twitter_thread.md` | X/Twitter | Copy-paste the 10-tweet thread |
| `marketing/linkedin_post.md` | LinkedIn | Post as a professional launch announcement |
| `marketing/producthunt.md` | Product Hunt | Submit as a launch |
| `marketing/hacker_news.md` | Hacker News | Post as "Show HN" |
| `marketing/reddit.md` | Reddit | Tailored for r/algotrading, r/SideProject, r/coolgithubprojects |
| `marketing/press_release.md` | Any | Formal press release |
| `marketing/taglines.md` | Any | 30+ taglines + bios for every platform |
| `marketing/meme_templates.md` | Social | 8 meme templates (Bloomberg vs Miau, Drake, etc.) |

### Quick pitch (copy-paste this anywhere):

> 🐱 I built a Bloomberg terminal. For cats. And humans.
>
> 188 commands. AI advisor. 3D charts. Paper trading. Real-time markets.
> Bloomberg costs $24k/year. Miau costs €0–€99/month.
>
> Try it free: https://your-ngrok-url.ngrok-free.app
> Type `help` to start. Your cat will thank you.

### Total cost: €0

---

## 💰 STEP 4: Track Your Money

Once payments come in:

```bash
# Personal dashboard
status

# Revenue overview (shows your 20%)
revenue

# Mark payout when you want to withdraw
revenue payout
```

Revenue is stored in the `revenue_splits` table. Your 20% accumulates automatically. When you want to withdraw:

```bash
revenue payout    # Marks unpaid balance as "paid to founder"
```

Then transfer from Stripe to your bank account.

### Total cost: €0

---

## 🚀 STEP 5: Run the Go-Live Check

After you've added Stripe keys and started ngrok:

```bash
cd /home/jevgeniz/Projekte/miau-finance
bash scripts/go-live.sh
```

This checks:
- ✅ Stripe keys configured
- ✅ Registration endpoint working
- ✅ Checkout endpoint responding
- ✅ ngrok tunnel active
- ✅ All 9 services running

---

## 💸 THE MATH

| Scenario | Users | Monthly Revenue | **Your 20%** |
|----------|-------|----------------|--------------|
| 1 friend | 1 | €99 | **€19.80** |
| 5 friends | 5 | €495 | **€99** |
| Reddit front page | 10 | €990 | **€198** |
| Product Hunt #1 | 50 | €4,950 | **€990** |
| Viral tweet | 100 | €9,900 | **€1,980** |
| The cat takes over | 500 | €49,500 | **€9,900** |

### Budget breakdown:

| Item | Cost | Notes |
|------|------|-------|
| Stripe account | €0 | Free to create |
| ngrok free tier | €0 | Tunneling |
| Domain (miau.finance) | €8/year | Optional |
| VPS (Hetzner CX22) | €4/mo | Only if you want 24/7 |
| Stripe fees | 2.9% + €0.25 | Per transaction |
| **Total to start** | **€0–€12** | **You keep €8–€20 for emergencies** |

---

## 🐱 QUICK START (For the Impatient)

```bash
# 1. If you already have Stripe keys, add them NOW:
nano .env
# → add STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET
# → add STRIPE_PRO_PRICE_ID, STRIPE_ENTERPRISE_PRICE_ID

# 2. Restart backend:
docker compose restart backend

# 3. Expose your terminal:
ngrok http 5173
# → share the ngrok URL

# 4. Post on Reddit:
# → copy marketing/reddit.md
# → paste into r/algotrading

# 5. Wait for first payment:
revenue
```

```
   ╱|、
  (˚ˎ 。7     "The plan is complete. The tools are ready."
   |、˜〵      "The only thing missing is YOUR first customer."
   じしˍ,)ノ    "Go get them, hooman. The cat believes in you."


  🐟 .  🐟 .  🐟 .  🐟 .  🐟 .  🐟 .  🐟 .  🐟
  "Every sale is a tuna in the bank."
  "Every customer is a cat who trusts you."
  "Every euro is a step closer to infinite tuna."
  🐟 .  🐟 .  🐟 .  🐟 .  🐟 .  🐟 .  🐟 .  🐟
```
