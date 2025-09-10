# What3Words Open Source Clone

This repository is an open-source educational implementation of a What3Words-style geocoding system.  
It demonstrates a complete, small stack: a FastAPI backend and a Next.js frontend with an interactive map.

## Overview

The project translates latitude/longitude pairs into deterministic three-word addresses and back.  
It's intended for learning and experimentation, not production use.

## Features

- Convert latitude/longitude -> three-word phrase
- Convert three-word phrase -> latitude/longitude
- Interactive map (click to get words)
- FastAPI backend with Pydantic validation
- Next.js frontend (React + Leaflet)
- SQLite local datastore
- Unit tests for backend utilities

## Architecture

Frontend (Next.js) <-> Backend (FastAPI) <-> SQLite Database

## Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer and npm
- git

## Ports used in development

- Frontend: 3000  
- Backend: 8081 (recommended in this repo to avoid local port conflicts)  
- Alternative backend: 8000 (if available)

## Quick start (recommended)

1. Clone the repository:

   git clone <repo-url>
   cd What3Words-Open-Source

2. Backend setup

   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Start the backend (recommended: 127.0.0.1:8081)

   # foreground (use for debugging)
   uvicorn backend.main:app --host 127.0.0.1 --port 8081 --log-level debug

   # background (write logs to file)
   nohup uvicorn backend.main:app --host 127.0.0.1 --port 8081 --log-level debug > ../backend_server_8081.log 2>&1 &

   Note: The repository also contains convenience commands used during development.

4. Frontend setup

   cd ../frontend
   npm ci

5. Start the frontend

   # default (dev)
   npm run dev

   The frontend will be available at http://localhost:3000

   By default the frontend expects the backend at http://127.0.0.1:8081.  
   To point the frontend to a different backend, set:

   NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8081 npm run dev

## Environment variables

- NEXT_PUBLIC_API_BASE_URL — base URL the frontend will call (default: http://127.0.0.1:8081)  
- Use a .env file or set variables on the command line for local development.

## API endpoints

- POST /convert-coords  
  Request body: { "latitude": number, "longitude": number }  
  Response: { "word1": str, "word2": str, "word3": str }

- POST /convert-words  
  Request body: { "word1": str, "word2": str, "word3": str }  
  Response: { "latitude": number, "longitude": number }

- GET / returns simple health message {"message":"What3Words Clone API"}

Example curl:

curl -s -X POST http://127.0.0.1:8081/convert-coords -H "Content-Type: application/json" -d '{"latitude":51.5,"longitude":-0.12}'

## Database

- The project uses SQLite for simplicity.
- The SQLite file is created automatically: what3words.db in the project root or backend folder.
- The schema is defined in [`backend/models.py`](backend/models.py:1)

## Tests

- Backend unit tests live in the backend/ directory.
- Run tests:

   cd backend
   source venv/bin/activate
   pytest

## Logs

- Backend logs (when run with nohup) are written to files like backend_server.log or backend_server_8081.log
- Frontend dev logs are written to frontend_server.log when started with nohup

## Development notes

- The backend entrypoint is [`backend.main:app`](backend/main.py:1)
- The frontend page with fetch calls is [`frontend/src/app/page.tsx`](frontend/src/app/page.tsx:1)
- Leaflet marker icons were fixed to load from CDN to avoid 404s in Next.js

## Troubleshooting

- If the frontend cannot reach the backend:
  - Ensure backend is running on the configured host/port
  - Try setting NEXT_PUBLIC_API_BASE_URL to the backend host
  - Check firewall or local security tools that may block loopback ports (e.g., Little Snitch)

- If you see frequent backend restarts:
  - Uvicorn's reload watcher may be monitoring frontend/node_modules; start uvicorn with --reload-dir backend only or exclude frontend paths.

## Contributing

- Fork, create a feature branch, make changes, add tests, open a PR

## License

This project is licensed under MIT - see the LICENSE file.

## About this implementation

This is an educational, simplified reimplementation of What3Words:
- Limited word list (see [`backend/geocoding.py`](backend/geocoding.py:1))
- Simple deterministic grid mapping (not production-grade)
- Use for learning, experiments and demos only

If you'd like, run the app locally and explore adjusting the mapping algorithm or integrating a larger wordlist.

End.