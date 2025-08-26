from fastapi import FastAPI

from auth_service.api import auth_routes

app = FastAPI(title="OpalSuite Auth Service")

app.include_router(auth_routes.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "OpalSuite Auth Service"}
