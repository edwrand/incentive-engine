# incentive-engine-api/api/main.py

from fastapi import FastAPI
from api.db.database import init_db
from api.routes.reward import router as reward_router
from api.routes.accounts import router as accounts_router

app = FastAPI(title="Incentive Engine API")

@app.on_event("startup")
async def on_startup():
    """
    Initialize the database tables before handling any requests.
    """
    await init_db()

# Mount the reward and accounts routers
app.include_router(reward_router)
app.include_router(accounts_router)
