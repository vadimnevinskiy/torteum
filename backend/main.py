from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers import users_router
from config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


settings.avatars_dir.mkdir(parents=True, exist_ok=True)
app.mount(
    "/static",
    StaticFiles(directory=settings.STATIC_DIR),
    name="static",
)

app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
