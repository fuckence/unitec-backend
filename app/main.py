from fastapi import FastAPI
from .config import apply_cors
from .db import init_db
from .routers import auth, users, test_endpoints

app = FastAPI(
    title="Unitec FastAPI Backend", version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": 0}
)


apply_cors(app)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(test_endpoints.router)


@app.on_event("startup")
def on_startup():
    init_db()