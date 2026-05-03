import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gripforce_admin:ChangeMe2026@localhost:5432/gripforce_db")
SECRET_KEY = os.getenv("SECRET_KEY", "gripforce-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8h

USERS = {
    "trex": {"full_name": "Trex", "password": "TrexGrip2026!"},
    "mmk": {"full_name": "MMK", "password": "MMKGrip2026!"}
}
