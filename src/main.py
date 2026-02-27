from fastapi import FastAPI
import uvicorn
from src.routes import workers_router, db_router

app = FastAPI()
app.include_router(workers_router)
app.include_router(db_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)