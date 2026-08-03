import os

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "superset_secret_key_change_me")

SQLALCHEMY_DATABASE_URI = os.getenv(
    "SUPERSET_DATABASE_URL",
    "sqlite:////app/superset_home/superset.db",
)

FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
}

ROW_LIMIT = 5000

SUPERSET_WEBSERVER_PORT = 8088

TALISMAN_ENABLED = False

WTF_CSRF_ENABLED = False

ALERT_REPORTS_NOTIFICATION_DRY = True

WEBDRIVER_BASEURL = "http://superset:8088/"
