import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from shared.common.auth.auth import router as auth_router, get_current_user
from shared.database_base.models.user import User


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)
logging.getLogger("shared.common.auth").setLevel(logging.DEBUG)


app = FastAPI(title="OpalSuite Shared Backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/api/v1/")
async def read_root():
    return {"message": "OpalSuite Shared Backend API v1"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "OpalSuite Shared Backend API"}


@app.get("/tools")
async def get_tools(current_user: User = Depends(get_current_user)):
    tools_list = [
        {"name": "BuildPilot", "description": "Automate your build processes.", "path": "/buildpilot", "required_role": "user"},
        {"name": "CalMind", "description": "Manage your calendar and mind.", "path": "/calmind", "required_role": "user"},
        {"name": "MonitorIQ", "description": "Intelligent monitoring and alerts.", "path": "/monitoriq", "required_role": "user"},
        {"name": "RegressionInsight", "description": "Gain insights into your test regressions.", "path": "/regressioninsight", "required_role": "user"},
        {"name": "StandupBot", "description": "Automate daily standup meetings.", "path": "/standupbot", "required_role": "user"},
        {"name": "XrayQC", "description": "Quality control for X-ray images.", "path": "/xrayqc", "required_role": "user"},
        {"name": "UserManagement", "description": "Manage users and roles.", "path": "/manage/users", "required_role": "super_user"},
    ]

    filtered_tools = [
        tool for tool in tools_list
        if current_user.roles == "super_user" or tool["required_role"] == "user"
    ]
    return filtered_tools


@app.get("/test-route")
async def test_route():
    return {"message": "Test route is working!"}
