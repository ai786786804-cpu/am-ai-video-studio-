from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import projects, scenes, assets, jobs, providers

app = FastAPI(title="A M AI Studio", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api")
app.include_router(scenes.router, prefix="/api")
app.include_router(assets.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(providers.router, prefix="/api")

@app.on_event("startup")
def startup_event() -> None:
    init_db()

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": "A M AI Studio"}
