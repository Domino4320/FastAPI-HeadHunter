from fastapi import FastAPI
import uvicorn
from workers.routes import router as workers_router
from resumes.routes import router as resumes_router
from vacancies.routes import router as vacancies_router
from users.routes import router as users_router
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Работа процесса начата")
    yield
    print("Работа процесса завершена")


app = FastAPI(lifespan=lifespan)  # lifespan=lifespan
app.include_router(workers_router)
app.include_router(resumes_router)
app.include_router(vacancies_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
