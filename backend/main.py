from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from routers import users_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
