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

## How It Works: Internal Logic and Algorithm

This system maps the entire Earth's surface to a grid of approximately 3x3 meter squares and assigns a unique three-word address to each square. The process is entirely deterministic, meaning a specific location will always convert to the same three words, and those three words will always convert back to the same location.

### 1. The Grid System

- The Earth is modeled as a sphere with a radius of `6,371,008.8` meters.
- The total surface area is divided into `56.7` trillion 3x3 meter squares.
- To manage this vast number of squares, a grid is created with a 2:1 aspect ratio, resulting in `266,432` latitude cells and `532,864` longitude cells.
- This grid forms the basis for converting geographic coordinates into a single, unique number (`grid_index`).

### 2. Word List and Permutations

- A predefined list of words is loaded from `backend/words.txt` and other files in `backend/wordlists`.
- The system requires a minimum vocabulary size to ensure there are enough unique three-word combinations to cover all grid squares.
- If the word list is too small, the system will programmatically generate additional "synthetic" words to meet the minimum requirement.
- The total number of unique three-word permutations is calculated as `n * (n-1) * (n-2)`, where `n` is the size of the word list.

### 3. Geocoding Algorithm (Coordinates to Words)

The conversion from latitude and longitude to three words follows these steps:

1.  **Input Validation:** The `lat_lng_to_words` function first checks if the input latitude is between -90 and 90 and the longitude is between -180 and 180.
2.  **Grid Calculation:** The geographic coordinates are mapped to the grid to determine the corresponding `lat_grid` and `lng_grid` cell numbers.
3.  **Unique Index:** These grid numbers are combined to produce a single, unique `grid_index` for that square.
4.  **Permutation Mapping:** The `grid_index` is mathematically converted into a unique combination of three distinct indices from the word list. This is done without generating all possible permutations, making the process highly efficient.
5.  **Word Selection:** The three indices are used to look up the corresponding words in the sorted word list, forming the three-word address.

### 4. Reverse Geocoding Algorithm (Words to Coordinates)

The conversion from three words back to latitude and longitude is the reverse process:

1.  **Input Validation:** The `words_to_lat_lng` function ensures that three unique, alphabetic words are provided.
2.  **Word-to-Index Mapping:** Each word is looked up in a pre-computed `WORD_TO_INDEX` dictionary to get its index in the word list.
3.  **Index Reconstruction:** The three-word indices are used to mathematically reconstruct the original `grid_index`.
4.  **Coordinate Calculation:** The `grid_index` is then converted back into `lat_grid` and `lng_grid` numbers.
5.  **Final Coordinates:** These grid numbers are used to calculate the final latitude and longitude, with the coordinates centered in the middle of the square for accuracy.

## How to Add a New Dictionary or Language

Adding a new wordlist or language is a straightforward process. The system is designed to be extensible, and you can add new `.txt` files to the `backend/wordlists` directory.

### Steps to Add a New Word List:

1.  **Create a Word List File:**
    - Create a new text file (e.g., `my_custom_words.txt`).
    - Add one word per line.
    - Words should be lowercase and contain only alphabetic characters (a-z).
    - Ensure the file is saved with UTF-8 encoding.

2.  **Add the File to the Wordlists Directory:**
    - Place your new `.txt` file inside the `backend/wordlists/` directory.
    - Any `.txt` file in this directory will be automatically loaded and merged with the existing word lists when the application starts.

3.  **Special Mode for "India-Only" Words:**
    - If you want to create a word list for a specific region (e.g., India), you can place it in `backend/wordlists/india_only/`.
    - This mode can be activated by setting the environment variable `INDIA_ONLY_WORDS` to `"1"`, `"true"`, `"yes"`, or `"on"`.
    - When this mode is active, only the word lists from the `india_only` directory will be loaded.

### Files to Update:

-   **Primary:** No code changes are required if you are simply adding a new `.txt` file to the `backend/wordlists/` directory.
-   **Optional:** If you want to add a new "mode" (like the "india" mode), you will need to update the `load_word_list` function in [`backend/geocoding.py`](backend/geocoding.py:1) to handle the new mode.

By following these steps, you can easily extend the system's vocabulary or adapt it to new languages and regions.

End.