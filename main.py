from fastapi import FastAPI
import uvicorn
from workers.routes import router as workers_router
from database import router as db_router

app = FastAPI()
app.include_router(workers_router)
app.include_router(db_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
