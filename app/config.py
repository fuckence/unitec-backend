# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# load_dotenv(override=False)

# APP_ID = os.getenv("APP_ID", "")
# AITU_API_SECRET = os.getenv("AITU_API_SECRET", "")
# JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
# JWT_ALG = "HS256"
# ACCESS_TOKEN_TTL_MIN = int(os.getenv("ACCESS_TOKEN_TTL_MIN", "1440"))
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "mysql+pymysql://root:password@localhost:3306/unitec?charset=utf8mb4",
# )

# def apply_cors(app: FastAPI) -> None:
#     app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#         "https://*.ngrok-free.app",
#         "https://*.ngrok.io",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=False)

APP_ID = os.getenv("APP_ID", "")
AITU_API_SECRET = os.getenv("AITU_API_SECRET", "")
JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
JWT_ALG = "HS256"
ACCESS_TOKEN_TTL_MIN = int(os.getenv("ACCESS_TOKEN_TTL_MIN", "1440"))

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "unitec")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}?charset=utf8mb4"

def apply_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://*.ngrok-free.app",
            "https://*.ngrok.io",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )