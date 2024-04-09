#!/bin/bash
source /home/gabi/venv/silent-rave/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 2
