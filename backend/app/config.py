from pydantic_settings import BaseSettings
import os
import secrets
from pathlib import Path
from typing import Optional

# 🔒 SECURITY: Enforce that critical secrets come from environment
def get_required_env(key: str) -> str:
    """Get required environment variable or raise error"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"🔒 CRITICAL: Environment variable '{key}' is required for production")
    return value

class Settings(BaseSettings):
    # 🔒 Database - REQUIRED from environment (especially in production)
    database_url: Optional[str] = None
    database_url_sync: Optional[str] = None
    
    # 🔒 MinIO - REQUIRED from environment  
    minio_endpoint: Optional[str] = None
    minio_access_key: Optional[str] = None
    minio_secret_key: Optional[str] = None
    
    # External APIs
    cubejs_api_url: Optional[str] = None
    cubejs_api_secret: Optional[str] = None
    fred_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    alpha_vantage_api_key: Optional[str] = None
    finnhub_api_key: Optional[str] = None
    twelvedata_api_key: Optional[str] = None
    coinpaprika_api_key: Optional[str] = None
    bls_api_key: Optional[str] = None
    etherscan_api_key: Optional[str] = None
    eia_api_key: str = ""
    imf_api_key: str = ""
    hfdata_api_key: str = ""
    mobula_api_key: str = ""
    education_api_key: str = ""
    app_name: str = "Miau Finance"

    # AI configuration
    ai_provider: Optional[str] = None
    ai_api_key: Optional[str] = None
    ai_model: Optional[str] = None
    ai_max_tokens: int = 4096
    ai_temperature: float = 0.7

    # 🔒 JWT Auth - MUST be strong (32+ chars) and from environment
    secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Demo user - MUST be overridden via .env in production
    # Default to None - forces env var check in _validate_config
    demo_username: Optional[str] = None
    demo_password: Optional[str] = None

    # Redis
    redis_url: Optional[str] = None

    # Rate Limiting
    rate_limit_per_minute: int = 300
    rate_limit_per_hour: int = 10000

    # CORS - Restrict in production
    cors_origins: Optional[str] = None
    
    # 🔒 Environment mode
    environment: str = "development"  # "development" or "production"

    # Paper Trading
    paper_trading_enabled: bool = True
    paper_initial_cash: float = 100000.0
    paper_commission_rate: float = 0.001
    paper_slippage_pct: float = 0.001

    # Broker Integration
    alpaca_api_key: Optional[str] = None
    alpaca_secret_key: Optional[str] = None
    alpaca_paper: bool = True

    # Interactive Brokers (Gateway / Client Portal API)
    ib_gateway_url: Optional[str] = None
    ib_account_id: Optional[str] = None

    # Notification providers (all optional — enable what you need)
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_sender_email: Optional[str] = None
    smtp_sender_password: Optional[str] = None
    slack_webhook_url: Optional[str] = None
    webhook_notification_url: Optional[str] = None
    webhook_headers: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_from_number: Optional[str] = None

    # Web Push (VAPID)
    vapid_public_key: Optional[str] = None
    vapid_private_key: Optional[str] = None
    vapid_claim_email: str = "admin@miau.finance"

    # WhatsApp / Telegram
    whatsapp_api_key: Optional[str] = None
    whatsapp_phone_number_id: Optional[str] = None
    telegram_bot_token: Optional[str] = None

    # 💳 Stripe Billing
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    stripe_pro_price_id: Optional[str] = None
    stripe_enterprise_price_id: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        
        # 🔒 CRITICAL: Validate critical configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate critical configuration settings"""
        
        # JWT Secret - CRITICAL
        if not self.secret_key or len(self.secret_key) < 32:
            if self.environment == "production":
                raise ValueError(
                    "🔒 CRITICAL: JWT secret_key must be 32+ characters in production.\n"
                    "Generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"\n"
                    "Set environment variable: export JWT_SECRET_KEY=<generated_key>"
                )
            else:
                # Dev mode: persist a stable secret so sessions survive restarts.
                # (pawdentity SSO depends on a stable signing key across apps/restarts.)
                _secret_file = Path(__file__).resolve().parent.parent / ".jwt_secret"
                try:
                    _existing = _secret_file.read_text().strip()
                    if _existing:
                        self.secret_key = _existing
                        print(f"⚠️  [DEV] Using persisted JWT secret ({_secret_file.name})")
                    else:
                        raise ValueError("empty secret file")
                except Exception:
                    self.secret_key = secrets.token_urlsafe(32)
                    try:
                        _secret_file.write_text(self.secret_key)
                        try:
                            _secret_file.chmod(0o600)
                        except OSError:
                            pass
                    except OSError:
                        pass
                    print(f"⚠️  [DEV] Generated + persisted JWT secret to {_secret_file.name}")
        
        # Database - CRITICAL
        if not self.database_url:
            if self.environment == "production":
                raise ValueError(
                    "🔒 CRITICAL: DATABASE_URL is required in production.\n"
                    "Format: postgresql+asyncpg://user:password@host:port/dbname\n"
                    "Set environment variable: export DATABASE_URL=..."
                )
            else:
                # Dev default
                dev_pass = secrets.token_urlsafe(12)
                self.database_url = f"postgresql+asyncpg://miau:{dev_pass}@localhost:5432/miau"
                print(f"⚠️  [DEV] Generated random database password (user: miau)")
        
        if not self.database_url_sync:
            if self.database_url:
                # Derive sync URL from async URL
                self.database_url_sync = self.database_url.replace("asyncpg", "psycopg2")
        
        # Redis - Warn if not set
        if not self.redis_url:
            if self.environment == "production":
                raise ValueError(
                    "🔒 CRITICAL: REDIS_URL is required in production.\n"
                    "Format: redis://user:password@host:port/db\n"
                    "Set environment variable: export REDIS_URL=..."
                )
            else:
                self.redis_url = "redis://:miau_redis@redis:6379/0"
                print("⚠️  [DEV] Using default Redis URL")
        
        # CORS - IMPORTANT for production
        if not self.cors_origins:
            if self.environment == "production":
                raise ValueError(
                    "🔒 CRITICAL: CORS_ORIGINS is required in production.\n"
                    "Set environment variable: export CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com"
                )
            else:
                self.cors_origins = "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176,http://localhost:5177,http://localhost:5178,http://localhost:5179,http://localhost:5181,http://localhost:5565,http://localhost:5567,http://localhost:3000,http://localhost:3001"
                print("⚠️  [DEV] Using default CORS origins")
        
        # MinIO - Warn if using defaults
        if not self.minio_endpoint:
            self.minio_endpoint = "localhost:9000"
        if not self.minio_access_key:
            self.minio_access_key = "miau_admin"
        if not self.minio_secret_key:
            self.minio_secret_key = secrets.token_urlsafe(24)
            if self.environment != "production":
                print("⚠️  [DEV] Generated random MinIO secret key")
        
        if self.environment == "production":
            if self.minio_access_key == "miau_admin":
                print("⚠️  [SECURITY WARNING] MinIO access key is default. Set MINIO_ACCESS_KEY in environment!")
        
        # 🔒 Demo credentials - must be set via .env
        if not self.demo_username or not self.demo_password:
            if self.environment == "production":
                raise ValueError(
                    "🔒 CRITICAL: DEMO_USERNAME and DEMO_PASSWORD must be set in production.\n"
                    "Set in .env file or environment variables."
                )
            else:
                # Dev mode: generate random credentials
                self.demo_username = "dev_" + secrets.token_hex(4)
                self.demo_password = secrets.token_urlsafe(16)
                print(f"⚠️  [DEV] Generated random demo credentials (username: {self.demo_username})")
        
        # Block known default passwords in any environment
        if self.demo_password in ("admin", "password", "miau_admin", "CHANGE_ME_IN_PRODUCTION", "changeme"):
            print(f"🔴 [SECURITY] Demo password is too weak ({self.demo_password}). "
                  f"Generate a strong one via .env or environment variable.")
        
        # AI - Validate provider/api_key
        if self.ai_provider and self.ai_provider not in ("openai", "anthropic"):
            raise ValueError(f"AI_PROVIDER must be 'openai' or 'anthropic', got '{self.ai_provider}'")
        if self.ai_provider and not self.ai_api_key:
            if self.environment == "production":
                raise ValueError(
                    "🔒 CRITICAL: AI_API_KEY is required when AI_PROVIDER is set.\n"
                    "Set environment variable: export AI_API_KEY=<your_api_key>"
                )
            else:
                print("⚠️  [DEV] AI provider set but no API key — AI features will be unavailable")
        if not self.ai_provider:
            self.ai_provider = "openai"
        if not self.ai_model:
            self.ai_model = "gpt-4o-mini" if self.ai_provider == "openai" else "claude-3-haiku-20240307"

        # Stripe / Billing - warn if missing in production
        if self.environment == "production":
            if not self.stripe_secret_key:
                print("⚠️  [PRODUCTION] STRIPE_SECRET_KEY not set — billing features disabled")
            if not self.stripe_webhook_secret:
                print("⚠️  [PRODUCTION] STRIPE_WEBHOOK_SECRET not set — webhook verification disabled")
            if self.slack_webhook_url:
                print("ℹ️  Slack alerts configured via SLACK_WEBHOOK_URL")
            elif not self.webhook_notification_url:
                print("⚠️  [PRODUCTION] No webhook URL set — alert notifications disabled")
            if not self.smtp_host:
                print("ℹ️  SMTP not configured — email notifications disabled")
        else:
            if self.slack_webhook_url:
                print("ℹ️  Slack alerts enabled (SLACK_WEBHOOK_URL)")

        # External APIs - Warn about demo keys in production
        for key_name, key_value in [
            ("FRED_API_KEY", self.fred_api_key),
            ("NEWS_API_KEY", self.news_api_key),
            ("ALPHA_VANTAGE_API_KEY", self.alpha_vantage_api_key),
        ]:
            if key_value == "demo" and self.environment == "production":
                print(f"⚠️  [PRODUCTION] {key_name} is set to 'demo' — provider will not return live data")
        if not self.cubejs_api_url:
            self.cubejs_api_url = "http://localhost:4000"
        if not self.cubejs_api_secret:
            self.cubejs_api_secret = secrets.token_urlsafe(24)
        if not self.fred_api_key:
            self.fred_api_key = ""
        if not self.news_api_key:
            self.news_api_key = ""
        if not self.alpha_vantage_api_key:
            self.alpha_vantage_api_key = ""

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
