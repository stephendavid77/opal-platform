#!/bin/bash

# Run the OpalSuite Shared Backend API
uvicorn backend.main:app --reload --port 8000