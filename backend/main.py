from fastapi import FastAPI

from OpalSuite.shared.common.auth.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/api/v1/")
async def read_root():
    return {"message": "OpalSuite Shared Backend API v1"}
