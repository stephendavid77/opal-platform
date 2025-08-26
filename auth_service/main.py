import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth_service.api import auth_routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)


app = FastAPI(title="OpalSuite Auth Service")

# Configure CORS
# In a production environment, you should restrict origins to your frontend's domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth_routes.router, prefix="/auth")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "OpalSuite Auth Service"}
