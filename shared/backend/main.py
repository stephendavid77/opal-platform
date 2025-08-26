from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OpalSuite Shared Backend",
    description="This is the shared backend service for OpalSuite.",
    version="1.0.0",
)

# CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tools")
async def get_tools():
    return [
        {
            "name": "BuildPilot",
            "description": "Automate your build processes.",
            "path": "/buildpilot",
        },
        {
            "name": "CalMind",
            "description": "Manage your calendar and tasks.",
            "path": "/calmind",
        },
        {
            "name": "MonitorIQ",
            "description": "Monitor your system's performance.",
            "path": "/monitoriq",
        },
        {
            "name": "RegressionInsight",
            "description": "Analyze regression test results.",
            "path": "/regressioninsight",
        },
        {
            "name": "StandupBot",
            "description": "Automate your daily standups.",
            "path": "/standupbot",
        },
        {
            "name": "XrayQC",
            "description": "Perform quality checks on X-ray images.",
            "path": "/xrayqc",
        },
    ]


@app.get("/")
async def read_root():
    return {"message": "Welcome to the OpalSuite Shared Backend"}
