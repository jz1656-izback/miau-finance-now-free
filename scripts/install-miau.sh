#!/bin/bash
# 🐱 Miau Finance — Production Installer
# Generates all passwords, prompts for API keys, creates .env
#
# Usage:
#   bash scripts/install-miau.sh
#   bash scripts/install-miau.sh --auto   # Auto-generate everything (no prompts)
#   bash scripts/install-miau.sh --validate  # Validate existing .env only

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

ENV_FILE="/home/jevgeniz/Projekte/miau-finance/.env"
MODE="${1:-interactive}"

echo ""
echo -e "${CYAN}🐱 Miau Finance — Production Installer${NC}"
echo -e "${CYAN}══════════════════════════════════════${NC}"
echo ""

gen_pass() { python3 -c "import secrets; print(secrets.token_urlsafe($1))"; }
gen_fernet() { python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"; }

if [ "$MODE" = "--validate" ]; then
  echo -e "${YELLOW}🔍 Validating existing .env...${NC}"
  ERRORS=0
  for var in POSTGRES_PASSWORD REDIS_PASSWORD SECRET_KEY JWT_SECRET_KEY; do
    VAL=$(grep "^${var}=" "$ENV_FILE" 2>/dev/null | cut -d= -f2)
    if [ -z "$VAL" ] || [ "$VAL" = "CHANGE_ME" ]; then
      echo -e "  ${RED}❌ $var is not set${NC}"
      ERRORS=$((ERRORS+1))
    else
      echo -e "  ${GREEN}✅ $var ${VAL:0:8}...${NC}"
    fi
  done
  for var in FINNHUB_API_KEY TWELVEDATA_API_KEY FRED_API_KEY; do
    VAL=$(grep "^${var}=" "$ENV_FILE" 2>/dev/null | cut -d= -f2)
    if [ -z "$VAL" ]; then
      echo -e "  ${YELLOW}⚠️  $var is empty (optional for dev)${NC}"
    else
      echo -e "  ${GREEN}✅ $var ${VAL:0:8}...${NC}"
    fi
  done
  if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ $ERRORS critical vars missing. Run installer without --validate${NC}"
    exit 1
  fi
  echo -e "${GREEN}✅ .env validation passed${NC}"
  exit 0
fi

if [ "$MODE" = "--auto" ]; then
  echo -e "${YELLOW}⚡ Auto-generating all credentials (no prompts)...${NC}"
  AUTO=true
else
  AUTO=false
  echo -e "This script generates production credentials and prompts for API keys."
  echo -e "Press Enter to accept auto-generated passwords, or type your own."
  echo ""
fi

# ── Backup existing .env ──
if [ -f "$ENV_FILE" ]; then
  cp "$ENV_FILE" "${ENV_FILE}.bak.$(date +%s)"
  echo -e "${GREEN}✅ Existing .env backed up${NC}"
fi

# ── Helper: prompt or auto ──
prompt_or_auto() {
  local var="$1" default="$2" prompt_msg="$3" url="$4"
  if [ "$AUTO" = true ]; then
    echo "${var}=${default}"
    return
  fi
  if [ -n "$url" ]; then
    echo -e "${CYAN}  📝 $var${NC}"
    echo -e "     Get it at: ${YELLOW}$url${NC}"
  fi
  read -p "  ${var} [$default]: " input
  echo "${var}=${input:-$default}"
}

# ── Generate .env ──
{
  echo "# 🐱 MIAU FINANCE — PRODUCTION ENVIRONMENT"
  echo "# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "#"
  echo ""
  echo "# === ENVIRONMENT ==="
  echo "ENVIRONMENT=production"
  echo "FRONTEND_URL=https://miau.finance"
  echo "BACKEND_URL=https://api.miau.finance"
  echo "CORS_ORIGINS=https://miau.finance,https://app.miau.finance"
  echo ""
  echo "# === DATABASE (REQUIRED) ==="
  prompt_or_auto "POSTGRES_PASSWORD" "$(gen_pass 32)"
  prompt_or_auto "POSTGRES_USER" "miau"
  prompt_or_auto "POSTGRES_DB" "miau"
  echo "DATABASE_URL=postgresql+asyncpg://miau:\${POSTGRES_PASSWORD}@postgres:5432/miau"
  echo "DATABASE_URL_SYNC=postgresql+psycopg2://miau:\${POSTGRES_PASSWORD}@postgres:5432/miau"
  echo ""
  echo "# === REDIS ==="
  prompt_or_auto "REDIS_PASSWORD" "$(gen_pass 32)"
  echo "REDIS_URL=redis://default:\${REDIS_PASSWORD}@redis:6379"
  echo ""
  echo "# === SECURITY (REQUIRED — change these!) ==="
  prompt_or_auto "SECRET_KEY" "$(gen_pass 32)"
  prompt_or_auto "JWT_SECRET_KEY" "$(gen_pass 32)"
  echo "JWT_ALGORITHM=HS256"
  echo "ACCESS_TOKEN_EXPIRE_MINUTES=60"
  prompt_or_auto "KEY_VAULT_MASTER_KEY" "$(gen_fernet)"
  echo ""
  echo "# === DEMO LOGIN ==="
  echo "DEMO_USERNAME=$(openssl rand -hex 4)"
  echo "DEMO_PASSWORD=$(openssl rand -base64 12 | tr -d '/+=')"
  echo ""
  echo "# === API KEYS (fill these in for full provider coverage) ==="
  prompt_or_auto "FINNHUB_API_KEY" "" "" "https://finnhub.io/register"
  prompt_or_auto "TWELVEDATA_API_KEY" "" "" "https://twelvedata.com/"
  prompt_or_auto "FRED_API_KEY" "" "" "https://fred.stlouisfed.org/docs/api/api_key.html"
  prompt_or_auto "EIA_API_KEY" "" "" "https://www.eia.gov/opendata/register.php"
  prompt_or_auto "BLS_API_KEY" "" "" "https://www.bls.gov/developers/"
  prompt_or_auto "NEWS_API_KEY" "" "" "https://newsapi.org/"
  prompt_or_auto "ALPHA_VANTAGE_API_KEY" "" "" "https://www.alphavantage.co/"
  prompt_or_auto "COINPAPRIKA_API_KEY" "" ""
  prompt_or_auto "ETHERSCAN_API_KEY" "" "" "https://etherscan.io/register"
  prompt_or_auto "HFDATA_API_KEY" "" "" "https://hfdata.io/"
  prompt_or_auto "MOBULA_API_KEY" "" "" "https://mobula.io/"
  echo ""
  echo "# === EDUCATION ==="
  prompt_or_auto "EDUCATION_API_KEY" "$(gen_pass 24)"
  echo ""
  echo "# === STRIPE (REQUIRED for billing) ==="
  prompt_or_auto "STRIPE_SECRET_KEY" "" "" "https://dashboard.stripe.com/apikeys"
  prompt_or_auto "STRIPE_WEBHOOK_SECRET" "" "" "https://dashboard.stripe.com/webhooks"
  prompt_or_auto "STRIPE_PRO_PRICE_ID" "" "" "Create in Stripe dashboard → Products"
  prompt_or_auto "STRIPE_ENTERPRISE_PRICE_ID" "" ""
  echo ""
  echo "# === INFRASTRUCTURE ==="
  prompt_or_auto "MINIO_ACCESS_KEY" "miauadmin"
  prompt_or_auto "MINIO_SECRET_KEY" "$(gen_pass 32)"
  echo "MINIO_ENDPOINT=http://minio:9000"
  prompt_or_auto "CUBEJS_API_SECRET" "$(gen_pass 32)"
  echo "CUBEJS_API_URL=http://cube:4000"
  prompt_or_auto "SUPERSET_SECRET_KEY" "$(gen_pass 32)"
  prompt_or_auto "SUPERSET_ADMIN_USERNAME" "superset_admin"
  prompt_or_auto "SUPERSET_ADMIN_PASSWORD" "$(gen_pass 16)"
  prompt_or_auto "GRAFANA_USERNAME" "admin"
  prompt_or_auto "GRAFANA_PASSWORD" "$(gen_pass 16)"
  prompt_or_auto "AIRFLOW_USERNAME" "admin"
  prompt_or_auto "AIRFLOW_PASSWORD" "$(gen_pass 16)"
  echo ""
  echo "# === RATE LIMITING ==="
  echo "RATE_LIMIT_PER_MINUTE=30"
  echo "RATE_LIMIT_PER_HOUR=1000"
  echo ""
  echo "# === RATE LIMITING (Per-Tier Defaults) ==="
  echo "# Free: 30 req/min, Pro: 300 req/min, Enterprise: 10000 req/min"
} > "$ENV_FILE"

echo ""
echo -e "${GREEN}✅ .env generated${NC}"
echo ""

# ── Summary ──
echo -e "${CYAN}══════════════════════════════════════${NC}"
echo -e "${CYAN}📋  INSTALLATION SUMMARY${NC}"
echo -e "${CYAN}══════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}Auto-generated passwords:${NC}"
for var in POSTGRES_PASSWORD REDIS_PASSWORD SECRET_KEY JWT_SECRET_KEY KEY_VAULT_MASTER_KEY MINIO_SECRET_KEY CUBEJS_API_SECRET SUPERSET_SECRET_KEY EDUCATION_API_KEY; do
  VAL=$(grep "^${var}=" "$ENV_FILE" | cut -d= -f2)
  echo -e "    ${GREEN}✅${NC} ${var}: ${VAL:0:12}..."
done
echo ""
echo -e "  ${YELLOW}API Keys (set: ✅ / empty: ⚠️):${NC}"
for var in FINNHUB_API_KEY TWELVEDATA_API_KEY FRED_API_KEY EIA_API_KEY BLS_API_KEY NEWS_API_KEY ALPHA_VANTAGE_API_KEY; do
  VAL=$(grep "^${var}=" "$ENV_FILE" | cut -d= -f2)
  if [ -n "$VAL" ]; then
    echo -e "    ${GREEN}✅${NC} ${var}: ${VAL:0:8}..."
  else
    echo -e "    ${YELLOW}⚠️${NC} ${var}: ${RED}NOT SET${NC}"
  fi
done
echo ""
echo -e "  ${YELLOW}Stripe:${NC}"
for var in STRIPE_SECRET_KEY STRIPE_WEBHOOK_SECRET STRIPE_PRO_PRICE_ID STRIPE_ENTERPRISE_PRICE_ID; do
  VAL=$(grep "^${var}=" "$ENV_FILE" | cut -d= -f2)
  if [ -n "$VAL" ]; then
    echo -e "    ${GREEN}✅${NC} ${var}: ${VAL:0:12}..."
  else
    echo -e "    ${YELLOW}⚠️${NC} ${var}: ${RED}NOT SET — billing disabled${NC}"
  fi
done
echo ""
echo -e "  ${YELLOW}Next steps:${NC}"
echo -e "    1. ${CYAN}Register API keys${NC} at the URLs above"
echo -e "    2. ${CYAN}nano ${ENV_FILE}${NC} and paste your keys"
echo -e "    3. ${CYAN}docker compose -f docker-compose.prod.yml up -d${NC}"
echo ""

# ── Validate ──
echo -e "${CYAN}🔍 Running self-test...${NC}"
bash "$0" --validate && echo "" && echo -e "${GREEN}✅${NC} 🐱${GREEN} Miau Finance is ready for production!${NC}" || echo -e "${RED}❌ Validation failed — fix the errors above${NC}"
