from fastapi import FastAPI, Depends

from dependencies import get_query_token
from routers import users

app = FastAPI()


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
