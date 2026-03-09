from fastapi import FastAPI
import uvicorn
from workers.routes import router as workers_router
from resumes.routes import router as resumes_router
from contextlib import asynccontextmanager
from core.database import db_context


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_context.create_tables()
    yield
    print("Работа процесса завершена")


app = FastAPI(lifespan=lifespan)  # lifespan=lifespan
app.include_router(workers_router)
app.include_router(resumes_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
