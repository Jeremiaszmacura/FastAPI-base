from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from routers import users

app = FastAPI()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(users.router)
app.include_router(users.token_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
